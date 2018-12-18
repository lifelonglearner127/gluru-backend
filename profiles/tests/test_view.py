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

        self.valid_change_role_payload = {
            "changeRole": {
                "userId": self.company_user.id,
                "role": self.role_named.id
            }
        }

        self.valid_change_role_by_self_payload = {
            "changeRole": {
                "userId": self.company_admin.id,
                "role": self.role_named.id
            }
        }

        self.invalid_change_role_payload = {
            "changeRole": {
                "userId": self.company_user.id,
                "role": ""
            }
        }

        self.valid_revoke_payload = {
            "inviteId": 1
        }

        self.invalid_revoke_payload = {
            "inviteId": 0
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

    def test_destroy_company_by_manager_valid(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.delete(
            reverse('profiles:company-detail', kwargs={'pk': self.company.id}),
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_company_by_manager_invalid(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.delete(
            reverse('profiles:company-detail', kwargs={'pk': 0}),
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_destroy_company_by_not_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_admin.token
        )
        response = self.client.delete(
            reverse('profiles:company-detail', kwargs={'pk': self.company.id}),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_comany_valid(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.get(
            reverse('profiles:company-detail', kwargs={'pk': self.company.id}),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_comany_invalid(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.get(
            reverse('profiles:company-detail', kwargs={'pk': 0}),
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_valid_company_users_by_authenticated_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.get(
            reverse('profiles:company-users', kwargs={'pk': self.company.id}),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_valid_company_users_by_unauthenticated_user(self):
        response = self.client.get(
            reverse('profiles:company-users', kwargs={'pk': self.company.id}),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_invalid_company_users_by_authenticated_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.get(
            reverse('profiles:company-users', kwargs={'pk': 0}),
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invite_user_by_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.post(
            reverse('profiles:company-invite', kwargs={'pk': self.company.id}),
            data=json.dumps(self.valid_invite_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invite_user_by_staff(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.staff.token
        )
        response = self.client.post(
            reverse('profiles:company-invite', kwargs={'pk': self.company.id}),
            data=json.dumps(self.valid_invite_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invite_by_company_admin(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_admin.token
        )
        response = self.client.post(
            reverse('profiles:company-invite', kwargs={'pk': self.company.id}),
            data=json.dumps(self.valid_invite_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invite_by_company_named(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_named.token
        )
        response = self.client.post(
            reverse('profiles:company-invite', kwargs={'pk': self.company.id}),
            data=json.dumps(self.valid_invite_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invite_by_company_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_user.token
        )
        response = self.client.post(
            reverse('profiles:company-invite', kwargs={'pk': self.company.id}),
            data=json.dumps(self.valid_invite_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invite_by_community_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.post(
            reverse('profiles:company-invite', kwargs={'pk': self.company.id}),
            data=json.dumps(self.valid_invite_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_revoke_invite_by_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-revoke-invite',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_revoke_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_revoke_invite_by_staff(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.staff.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-revoke-invite',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_revoke_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_revoke_invite_by_company_admin(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_admin.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-revoke-invite',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_revoke_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_revoke_invite_by_company_named(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_named.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-revoke-invite',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_revoke_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_revoke_invite_by_company_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_user.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-revoke-invite',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_revoke_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_revoke_invite_by_community_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-revoke-invite',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_revoke_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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

    def test_leave_company_by_company_admin(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_admin.token
        )
        response = self.client.get(
            reverse(
                'profiles:company-leave-company',
                kwargs={'pk': self.company.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_leave_company_by_company_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_named.token
        )
        response = self.client.get(
            reverse(
                'profiles:company-leave-company',
                kwargs={'pk': self.company.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_leave_company_by_non_company_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.get(
            reverse(
                'profiles:company-leave-company',
                kwargs={'pk': self.company.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_company_role_valid_by_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-change-role',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_change_role_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_company_role_valid_by_staff(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.staff.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-change-role',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_change_role_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_company_role_valid_by_admin(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_admin.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-change-role',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_change_role_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_company_role_valid_by_named(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_named.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-change-role',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_change_role_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_change_company_role_valid_by_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_user.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-change-role',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_change_role_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_change_company_role_valid_by_community_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-change-role',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_change_role_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_change_company_role_invalid_by_admin(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_admin.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-change-role',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.invalid_change_role_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_company_role_by_admin_self(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_admin.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-change-role',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_change_role_by_self_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserViewSetTest(APITestCase):
    pass
