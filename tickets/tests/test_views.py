import json
from django.urls import reverse
from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APITestCase
from info.models import UserRole
from profiles.models import User, Company, Membership
from tickets.models import Ticket, Answer


class TicketViewSetTest(APITestCase):

    def setUp(self):

        call_command('loaddata', 'data', verbosity=0)

        # Create Users; manager, staff, company user, community user
        self.manager = User.objects.create_superuser(
            email='manager@gluu.org',
            password='manager'
        )

        self.staff = User.objects.create_user(
            email='staff@gluu.org',
            password='staff'
        )
        self.staff.is_staff = True
        self.staff.save()

        self.company_admin = User.objects.create_user(
            email='admin@gluu.org',
            password='levan'
        )

        self.company_named = User.objects.create_user(
            email='named@gluu.org',
            password='levan'
        )

        self.company_user = User.objects.create_user(
            email='user@gluu.org',
            password='levan'
        )

        self.community_user = User.objects.create_user(
            email='user@gmail.com',
            password='levan'
        )

        # Create Company
        self.company = Company.objects.create(
            name='Gluu'
        )

        # Create Permission and UserRole
        self.role_admin = UserRole.objects.get(name='admin')
        self.role_named = UserRole.objects.get(name='named')
        self.role_user = UserRole.objects.get(name='user')

        # Create Membership
        Membership.objects.create(
            company=self.company, user=self.company_admin, role=self.role_admin
        )
        Membership.objects.create(
            company=self.company, user=self.company_named, role=self.role_named
        )
        Membership.objects.create(
            company=self.company, user=self.company_user, role=self.role_user
        )

        # Create Tickets; Community Ticket, Admin Ticket, Company Ticket
        self.ticket_by_community_user = Ticket.objects.create(
            title='title', body='body', status_id=1, category_id=1,
            issue_type_id=1, gluu_server_id=1, os_id=1,
            created_by=self.community_user
        )

        self.ticket_by_company_admin = Ticket.objects.create(
            title='title', body='body', status_id=1, category_id=1,
            issue_type_id=1, gluu_server_id=1, os_id=1,
            created_by=self.company_admin, company_association=self.company,
            created_for=self.company_named
        )

        self.ticket_by_staff_for_company = Ticket.objects.create(
            title='title', body='body', status_id=1, category_id=1,
            issue_type_id=1, gluu_server_id=1, os_id=1,
            created_by=self.staff, company_association=self.company,
            created_for=self.company_named
        )

        self.valid_payload = {
            "ticket": {
                "title": "title",
                "body": "body",
                "issueType": 1,
                "status": 1,
                "category": 1,
                "gluuServer": 1,
                "os": 1
            }
        }

        self.invalid_payload = {
            "ticket": {
                "title": "aaa",
                "body": "body",
                "issueType": 1,
                "status": 1,
                "category": 1,
                "gluuServer": 1,
                "os": 0
            }
        }

        self.valid_company_ticket_payload = {
            "ticket": {
                "title": "title",
                "body": "body",
                "issueType": 1,
                "status": 1,
                "category": 1,
                "gluuServer": 1,
                "os": 1,
                "company_association": self.company.id,
                "created_for": self.company_named.id
            }
        }

        self.invalid_company_ticket_payload = {
            "ticket": {
                "title": "title",
                "body": "body",
                "issueType": 1,
                "status": 1,
                "category": 1,
                "gluuServer": 1,
                "os": 1,
                "company_association": self.company.id,
                "created_for": self.community_user.id
            }
        }

    def test_create_ticket(self):
        """
        1. Create Ticket by unauthenticated user
        2. Create Valid Ticket by community user
        3. Create InValid Ticket by community user
        """
        # Create Ticket by unauthenticated user
        response = self.client.post(
            reverse('tickets:ticket-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Create Valid Ticket
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.post(
            reverse('tickets:ticket-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create Invalid Ticket
        response = self.client.post(
            reverse('tickets:ticket-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_company_ticket(self):
        """
        1. Create Company Ticket by Community User
        2. Create Company Ticket by Company User
        3. Create Company Ticket by Company Named
        4. Create Company Ticket by Company Named Invalid
        5. Create Company Ticket by Company Admin
        6. Create Company Ticket by Manager
        7. Create Company Ticket by Staff
        """
        # Create Company Ticket by Community User
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.post(
            reverse('tickets:ticket-list'),
            data=json.dumps(self.valid_company_ticket_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Create Company Ticket by Company User
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_user.token
        )
        response = self.client.post(
            reverse('tickets:ticket-list'),
            data=json.dumps(self.valid_company_ticket_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Create Company Ticket by Company Named
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_named.token
        )
        response = self.client.post(
            reverse('tickets:ticket-list'),
            data=json.dumps(self.valid_company_ticket_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create Company Ticket by Company Named Invalid
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_named.token
        )
        response = self.client.post(
            reverse('tickets:ticket-list'),
            data=json.dumps(self.invalid_company_ticket_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Create Company Ticket by Company Admin
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_admin.token
        )
        response = self.client.post(
            reverse('tickets:ticket-list'),
            data=json.dumps(self.valid_company_ticket_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create Company Ticket by Manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.post(
            reverse('tickets:ticket-list'),
            data=json.dumps(self.valid_company_ticket_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create Company Ticket by Staff
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.staff.token
        )
        response = self.client.post(
            reverse('tickets:ticket-list'),
            data=json.dumps(self.valid_company_ticket_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_ticket(self):
        """
        1. Update Ticket by unauthenticated user.
        2. Update Non-exisiting ticket by community user
        3. Update Valid Ticket by community user
        4. Update Invalid Ticket by community user
        """
        # Update Ticket by unauthenticated user.
        response = self.client.put(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_community_user.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Update Non-exisiting ticket by community user
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.put(
            reverse('tickets:ticket-detail', kwargs={'pk': 0}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Update Valid Ticket by community user
        response = self.client.put(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_community_user.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Update Invalid Ticket by community user
        response = self.client.put(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_community_user.id}
            ),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_community_ticket(self):
        """
        1. Update Community ticket by company user
        2. Update Community ticket by company named
        3. Update Community ticket by company admin
        4. Update Community ticket by manager
        5. Update Community ticket by staff
        """
        # Update Community ticket by company user
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_user.token
        )
        response = self.client.put(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_community_user.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Update Community ticket by company named
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_named.token
        )
        response = self.client.put(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_community_user.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Update Community ticket by company admin
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_admin.token
        )
        response = self.client.put(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_community_user.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Update Community ticket by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.put(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_community_user.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Update Community ticket by staff
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.staff.token
        )
        response = self.client.put(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_community_user.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_company_ticket(self):
        """
        1. Update Company ticket by Community user
        2. Update Company ticket by Company user
        3. Update Company ticket by Company named
        4. Update Company ticket by Company admin
        5. Update Company ticket by manager
        5. Update Company ticket by staff
        """
        # Update Company ticket by Community user
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.put(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_company_admin.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Update Company ticket by Company user
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_user.token
        )
        response = self.client.put(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_company_admin.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.put(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_staff_for_company.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Update Company ticket by Company named
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_named.token
        )
        response = self.client.put(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_company_admin.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_staff_for_company.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Update Company ticket by Company admin
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_admin.token
        )
        response = self.client.put(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_company_admin.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_staff_for_company.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Update Company ticket by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.put(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_company_admin.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_staff_for_company.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Update Company ticket by staff
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.staff.token
        )
        response = self.client.put(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_company_admin.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_staff_for_company.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_ticket(self):
        """
        1. Retrieve Community Ticket by unauthenticated user.
        2. Retrieve Company Ticket by unauthenticated user.
        3. Retrieve Non-existing Ticket by community user
        """
        # Retrieve Community Ticket by unauthenticated user.
        response = self.client.get(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_community_user.id}
            ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Retrieve Company Ticket by unauthenticated user.
        response = self.client.get(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_company_admin.id}
            ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Retrieve Non-existing Ticket
        response = self.client.get(
            reverse('tickets:ticket-detail', kwargs={'pk': 0}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_company_ticket(self):
        """
        1. Retrieve company ticket by community user
        2. Retrieve company ticket by company user
        3. Retrieve company ticket by company named
        4. Retrieve company ticket by company admin
        5. Retrieve company ticket by manager
        6. Retrieve company ticket by staff
        """
        # Retrieve company ticket by community user
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.get(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_company_admin.id}
            ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Retrieve company ticket by company user
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_user.token
        )
        response = self.client.get(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_company_admin.id}
            ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Retrieve company ticket by company named
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_named.token
        )
        response = self.client.get(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_company_admin.id}
            ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Retrieve company ticket by company admin
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_admin.token
        )
        response = self.client.get(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_company_admin.id}
            ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Retrieve company ticket by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.get(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_company_admin.id}
            ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Retrieve company ticket by staff
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.staff.token
        )
        response = self.client.get(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_company_admin.id}
            ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_ticket(self):
        """
        1. Delete ticket by unauthenticated user
        2. Delete ticket
        3. Delete non-existing ticket
        """
        # Delete ticket by unauthenticated user
        response = self.client.delete(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_community_user.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Delete ticket by community user
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.delete(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_community_user.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Delete non-existing ticket
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.delete(
            reverse('tickets:ticket-detail',kwargs={'pk': 0})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_company_ticket(self):
        """
        1. Delete company ticket by community user
        2. Delete company ticket by company user
        3. Delete company ticket by company named
        4. Delete company ticket by company admin
        5. Delete company ticket by company manager
        6. Delete company ticket by company staff
        """
        # Delete company ticket by community user
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.delete(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_company_admin.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Delete company ticket by company user
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_user.token
        )
        response = self.client.delete(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_company_admin.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Delete company ticket by company named
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_named.token
        )
        response = self.client.delete(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_company_admin.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Delete company ticket by company admin
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_admin.token
        )
        response = self.client.delete(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_staff_for_company.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Delete company ticket by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.delete(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_company_admin.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Delete company ticket by staff
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.staff.token
        )
        response = self.client.delete(
            reverse(
                'tickets:ticket-detail',
                kwargs={'pk': self.ticket_by_company_admin.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AnswerViewSetTest(APITestCase):

    def setUp(self):
        call_command('loaddata', 'data', verbosity=0)

        # Create Users; manager, staff, company user, community user
        self.manager = User.objects.create_superuser(
            email='manager@gluu.org',
            password='manager'
        )

        self.staff = User.objects.create_user(
            email='staff@gluu.org',
            password='staff'
        )
        self.staff.is_staff = True
        self.staff.save()

        self.company_user1 = User.objects.create_user(
            email='levan01@gluu.org',
            password='levan'
        )

        self.company_user2 = User.objects.create_user(
            email='levan02@gluu.org',
            password='levan'
        )

        self.community_user = User.objects.create_user(
            email='miranda@gluu.org',
            password='miranda'
        )

        # Create Company
        self.company = Company.objects.create(
            name='Gluu'
        )

        # Create Permission and UserRole
        self.read_permission = Permission.objects.get(pk=5)
        self.write_permission = Permission.objects.get(pk=6)
        self.respond_permission = Permission.objects.get(pk=7)
        self.user_role = UserRole.objects.create(
            name='custom'
        )
        self.user_role.permissions.add(self.read_permission)
        self.user_role.permissions.add(self.write_permission)
        self.user_role.permissions.add(self.respond_permission)

        # Create Membership
        Membership.objects.create(
            company=self.company, user=self.company_user1, role=self.user_role
        )
        Membership.objects.create(
            company=self.company, user=self.company_user2, role=self.user_role
        )

        # Create Tickets; Community Ticket, Admin Ticket, Company Ticket
        self.community_ticket = Ticket.objects.create(
            title='title', body='body', status_id=1, category_id=1,
            issue_type_id=1, gluu_server_id=1, os_id=1,
            created_by=self.community_user
        )

        self.manager_ticket = Ticket.objects.create(
            title='title', body='body', status_id=1, category_id=1,
            issue_type_id=1, gluu_server_id=1, os_id=1, created_by=self.manager
        )

        self.staff_ticket = Ticket.objects.create(
            title='title', body='body', status_id=1, category_id=1,
            issue_type_id=1, gluu_server_id=1, os_id=1, created_by=self.staff
        )

        self.company_ticket = Ticket.objects.create(
            title='title', body='body', status_id=1, category_id=1,
            issue_type_id=1, gluu_server_id=1, os_id=1,
            created_by=self.company_user1, company_association=self.company,
            created_for=self.company_user2
        )

        # Create Answer; Answer for community ticket,
        # admin ticket, company ticket
        self.community_ticket_answer = Answer.objects.create(
            body='body', ticket=self.community_ticket, created_by=self.manager
        )

        self.manager_ticket_answer = Answer.objects.create(
            body='body', ticket=self.manager_ticket, created_by=self.manager
        )

        self.company_ticket_answer = Answer.objects.create(
            body='body', ticket=self.company_ticket,
            created_by=self.company_user2
        )

        self.valid_payload = {
            "answer": {
                "body": "body"
            }
        }

        self.invalid_payload = {
            "answer": {
                "body": ""
            }
        }

    def test_create_answer_by_unauthroized_user(self):
        response = self.client.post(
            reverse(
                'tickets:ticket-answers-list',
                kwargs={'ticket_pk': self.ticket_by_community_user.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_answer_valid(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.post(
            reverse(
                'tickets:ticket-answers-list',
                kwargs={'ticket_pk': self.ticket_by_community_user.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_answer_invalid(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.post(
            reverse(
                'tickets:ticket-answers-list',
                kwargs={'ticket_pk': self.ticket_by_community_user.id}
            ),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_answer_by_permission_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_user2.token
        )
        response = self.client.post(
            reverse(
                'tickets:ticket-answers-list',
                kwargs={'ticket_pk': self.company_ticket.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_answer_by_non_permission_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.post(
            reverse(
                'tickets:ticket-answers-list',
                kwargs={'ticket_pk': self.company_ticket.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_answer_by_unauthorized_user(self):
        response = self.client.put(
            reverse(
                'tickets:ticket-answers-detail',
                kwargs={
                    'ticket_pk': self.ticket_by_community_user.id,
                    'pk': self.community_ticket_answer.id
                }
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_answer_by_non_permission_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.put(
            reverse(
                'tickets:ticket-answers-detail',
                kwargs={
                    'ticket_pk': self.company_ticket.id,
                    'pk': self.company_ticket_answer.id
                }
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_answer_valid_by_permission_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_user1.token
        )
        response = self.client.put(
            reverse(
                'tickets:ticket-answers-detail',
                kwargs={
                    'ticket_pk': self.company_ticket.id,
                    'pk': self.company_ticket_answer.id
                }
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_answer_by_unauthorized_user(self):
        response = self.client.get(
            reverse(
                'tickets:ticket-answers-detail',
                kwargs={
                    'ticket_pk': self.ticket_by_community_user.id,
                    'pk': self.community_ticket_answer.id
                }
            ),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_answer_by_permission_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_user1.token
        )
        response = self.client.get(
            reverse(
                'tickets:ticket-answers-detail',
                kwargs={
                    'ticket_pk': self.company_ticket.id,
                    'pk': self.company_ticket_answer.id
                }
            ),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_answer_by_non_permission_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.get(
            reverse(
                'tickets:ticket-answers-detail',
                kwargs={
                    'ticket_pk': self.company_ticket.id,
                    'pk': self.company_ticket_answer.id
                }
            ),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_answer_by_unauthorized_user(self):
        response = self.client.delete(
            reverse(
                'tickets:ticket-answers-detail',
                kwargs={
                    'ticket_pk': self.company_ticket.id,
                    'pk': self.company_ticket_answer.id
                }
            ),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_answer_non_existing(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.delete(
            reverse(
                'tickets:ticket-answers-detail',
                kwargs={
                    'ticket_pk': self.ticket_by_community_user.id,
                    'pk': 30
                }
            ),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_answer_by_permission_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_user1.token
        )
        response = self.client.delete(
            reverse(
                'tickets:ticket-answers-detail',
                kwargs={
                    'ticket_pk': self.company_ticket.id,
                    'pk': self.company_ticket_answer.id
                }
            ),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_answer_by_non_permission_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.delete(
            reverse(
                'tickets:ticket-answers-detail',
                kwargs={
                    'ticket_pk': self.company_ticket.id,
                    'pk': self.company_ticket_answer.id
                }
            ),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
