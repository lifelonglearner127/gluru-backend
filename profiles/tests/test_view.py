import json
from django.urls import reverse
from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APITestCase
from profiles.models import User, Company, Membership, UserRole, Permission


class CompanyViewSetTest(APITestCase):

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

        self.valid_payload = {
            "company": {
                "name": "OpenIAM"
            }
        }

        self.invalid_payload = {
            "company": {
                "name": ""
            }
        }

        self.valid_invite_payload = {
            "invitation": {
                "email": "gibupjo127@gmail.com",
                "role": 1
            }
        }
        
        self.invalid_invite_payload = {
            "invitation": {
                "email": "",
                "role": 1
            }
        }

    def test_create_company_by_not_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.post(
            reverse('profiles:company-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_company_by_manager_valid(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.post(
            reverse('profiles:company-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_company_by_manager_invalid(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.post(
            reverse('profiles:company-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_company_by_not_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.put(
            reverse('profiles:company-detail', kwargs={'pk': self.company.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_company_by_manager_valid(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.put(
            reverse('profiles:company-detail', kwargs={'pk': self.company.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_company_by_manager_invalid(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.put(
            reverse('profiles:company-detail', kwargs={'pk': self.company.id}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invite_user_by_permission_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.post(
            reverse('profiles:company-invite', kwargs={'pk': self.company.id}),
            data=json.dumps(self.valid_invite_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invite_user_by_non_permission_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.post(
            reverse('profiles:company-invite', kwargs={'pk': self.company.id}),
            data=json.dumps(self.valid_invite_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_revoke_invite_by_permission_user(self):
        pass

    def test_revoke_invite_by_non_permission_user(self):
        pass

    def test_accept_invite_by_invited_user(self):
        pass

    def test_accept_invite_by_not_invited_user(self):
        pass

    def test_remove_user_by_permission_user(self):
        pass

    def test_remove_user_by_non_permission_user(self):
        pass


class UserViewSetTest(APITestCase):
    pass
