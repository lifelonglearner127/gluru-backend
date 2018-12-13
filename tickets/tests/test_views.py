import json
from django.urls import reverse
from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APITestCase
from profiles.models import User, Company, Membership, UserRole, Permission
from tickets.models import Ticket


class TicketViewSetTest(APITestCase):
    """
    Test module for ticket api.

    1. Test Creating Ticket.
        - Un-authroized user cannot create a ticket
        - Create a ticket with valid payload
        - Create a ticket with invalid payload
        - Create a ticket on behalf of company
            = Community user cannot create a ticket on behalf of company
            = User with create permission can create a ticket
              on behalf of user from company
            = User with create permission cannot create a ticket
              on behalf of user who is not in company

    2. Test Updating Ticket.
        - Un-authroized user cannot update the ticket
        - Community user can update his ticket
        - Update the ticket with valid payload
        - Update the ticket with invalid payload
        - Update non-existing ticket
        - Update the ticket on behalf of company
            = User with create permission can update a ticket
              associated with company

    3. Test Retrieving Ticket
        - Un-authroized user cannot retrieve the ticket
        - Retrieve the ticket
        - Retrieve non-existing ticket
        - Retrieve the ticket created on behalf of company

    3. Test Deleting Ticket.
        - Un-authroized user cannot delete a ticket
        - Delete the ticket
        - Delete non-existing ticket
        - Delete the ticket created on behalf of the company

    """
    def setUp(self):

        call_command('loaddata', 'data', verbosity=0)

        # Create Users
        self.admin = User.objects.create_superuser(
            email='admin@gluu.org',
            password='admin'
        )

        self.staff = User.objects.create_user(
            email='staff@gluu.org',
            password='staff'
        )
        self.staff.is_staff = True
        self.staff.save()

        self.gluu_user1 = User.objects.create_user(
            email='levan01@gluu.org',
            password='levan'
        )

        self.gluu_user2 = User.objects.create_user(
            email='levan02@gluu.org',
            password='levan'
        )

        self.user = User.objects.create_user(
            email='miranda@gluu.org',
            password='miranda'
        )

        # Create Company
        self.gluu = Company.objects.create(
            name='Gluu'
        )

        # Create Permission and UserRole
        # self.permission = Permission.objects.create(
        #     app_name='tickets', model_name='Ticket',
        #     actions='create'
        # )
        self.permission = Permission.objects.get(pk=6)
        self.user_role = UserRole.objects.create(
            name='custom'
        )
        self.user_role.permissions.add(self.permission)

        # Create Membership
        Membership.objects.create(
            company=self.gluu, user=self.gluu_user1, role=self.user_role
        )
        Membership.objects.create(
            company=self.gluu, user=self.gluu_user2, role=self.user_role
        )

        self.ticket1 = Ticket.objects.create(
            title='title', body='body', status_id=1, category_id=1,
            issue_type_id=1, gluu_server_id=1, os_id=1, created_by=self.user
        )

        self.ticket2 = Ticket.objects.create(
            title='title', body='body', status_id=1, category_id=1,
            issue_type_id=1, gluu_server_id=1, os_id=1, created_by=self.admin
        )

        self.ticket3 = Ticket.objects.create(
            title='title', body='body', status_id=1, category_id=1,
            issue_type_id=1, gluu_server_id=1, os_id=1,
            created_by=self.gluu_user1, company_association=self.gluu,
            created_for=self.gluu_user2
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
                "company_association": self.gluu.id,
                "created_for": self.gluu_user2.id
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
                "company_association": self.gluu.id,
                "created_for": self.user.id
            }
        }

    def test_create_ticket_by_unauthorized_user(self):
        """
        Un-authroized user cannot create a ticket
        """
        response = self.client.post(
            reverse('tickets:ticket-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_ticket_valid(self):
        """
        Create a ticket with valid payload
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.post(
            reverse('tickets:ticket-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_ticket_invalid(self):
        """
        Create a ticket with invalid payload
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.post(
            reverse('tickets:ticket-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_ticket_by_community_user_for_company(self):
        """
        Community user cannot create a ticket on behalf of company
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.post(
            reverse('tickets:ticket-list'),
            data=json.dumps(self.valid_company_ticket_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_ticket_by_permission_user_for_user_from_company(self):
        """
        User with create permission can create a ticket
        on behalf of user from company
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.gluu_user1.token
        )
        response = self.client.post(
            reverse('tickets:ticket-list'),
            data=json.dumps(self.valid_company_ticket_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_ticket_by_permission_user_for_user_not_from_company(self):
        """
        User with create permission cannot create a ticket
        on behalf of user who is not in company
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.gluu_user1.token
        )
        response = self.client.post(
            reverse('tickets:ticket-list'),
            data=json.dumps(self.invalid_company_ticket_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_ticket_by_unauthorized_user(self):
        """
        Un-authroized user cannot update the ticket
        """
        response = self.client.put(
            reverse('tickets:ticket-detail', kwargs={'pk': self.ticket1.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_ticket_by_community_user(self):
        """
        Community user can only update his ticket
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.put(
            reverse('tickets:ticket-detail', kwargs={'pk': self.ticket2.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_ticket_valid(self):
        """
        Update the ticket with valid payload
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.put(
            reverse('tickets:ticket-detail', kwargs={'pk': self.ticket1.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_ticket_invalid(self):
        """
        Update the ticket with invalid payload
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.put(
            reverse('tickets:ticket-detail', kwargs={'pk': self.ticket1.id}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_ticket_non_existing(self):
        """
        Update non-existing ticket
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.put(
            reverse('tickets:ticket-detail', kwargs={'pk': 30}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_ticket_permission_user(self):
        """
        User with create permission can update a ticket
        associated with company
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.gluu_user2.token
        )
        response = self.client.put(
            reverse('tickets:ticket-detail', kwargs={'pk': self.ticket3.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
