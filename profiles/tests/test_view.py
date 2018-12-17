import json
from django.urls import reverse
from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APITestCase
from profiles.models import User, Company, Membership
from info.models import UserRole


class CompanyViewSetTest(APITestCase):

    def setUp(self):
        call_command('loaddata', 'data', verbosity=0)

        # Create Users; manager, staff, company user, community user
        self.manager = User.objects.create_superuser(
            email='manager@gmail.com',
            password='manager'
        )

        self.staff = User.objects.create_user(
            email='staff@gmail.com',
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

        self.valid_remove_member_payload = {
            "user_id": self.company_user.id
        }

        self.valid_remove_member_by_self_payload = {
            "user_id": self.company_admin.id
        }

        self.invalid_remove_member_payload = {
            "user_id": ""
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

    def test_remove_member_by_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-remove-member',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_remove_member_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_member_by_staff(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.staff.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-remove-member',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_remove_member_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_member_by_company_admin(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_admin.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-remove-member',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_remove_member_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_member_by_company_named(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_named.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-remove-member',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_remove_member_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_member_by_non_permission_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-remove-member',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_remove_member_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_member_by_self(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_admin.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-remove-member',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_remove_member_by_self_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserViewSetTest(APITestCase):
    pass
