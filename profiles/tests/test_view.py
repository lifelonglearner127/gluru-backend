import json
from django.urls import reverse
from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APITestCase
from profiles.models import User, Company, Membership, Invitation
from info.models import UserRole
from gluru_backend.utils import generate_hash


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

        # Create Invitation
        Invitation.objects.create(
            email=self.community_user.email,
            invited_by=self.company_admin,
            company=self.company,
            role=self.role_user,
            activation_key=generate_hash(self.community_user.email)
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
                "role": self.role_named.id
            }
        }

        self.invalid_invite_payload = {
            "invitation": {
                "email": "",
                "role": self.role_named.id
            }
        }

        self.valid_remove_user_member_payload = {
            "user_id": self.company_user.id
        }

        self.valid_remove_named_member_payload = {
            "user_id": self.company_named.id
        }

        self.valid_remove_admin_member_paylod = {
            "user_id": self.company_admin.id
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

        self.valid_accept_invite_payload = {
            "activationKey": generate_hash(self.community_user.email)
        }

        self.invalid_accept_invite_payload = {
            "activationKey": 'afdafdafda'
        }

    def test_create_company(self):
        """
         - create company info by user
         - create valid company info by manager
         - create invalid company info by manager
        """
        # create company by user
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.post(
            reverse('profiles:company-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # create valid company info by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.post(
            reverse('profiles:company-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # create invalid company info by manager
        response = self.client.post(
            reverse('profiles:company-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_company(self):
        """
         - update company info by user
         - update valid company info by manager
         - update invalid company info by manager
         - update non-existing company info by manager
        """
        # update company info by user
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.put(
            reverse('profiles:company-detail', kwargs={'pk': self.company.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # update valid company info by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.put(
            reverse('profiles:company-detail', kwargs={'pk': self.company.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # update invalid company info by manager
        response = self.client.put(
            reverse('profiles:company-detail', kwargs={'pk': self.company.id}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # update non-existing company info by manager
        response = self.client.put(
            reverse('profiles:company-detail', kwargs={'pk': 0}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_company(self):
        """
         - retrieve company info by user
         - retrieve non-existing company by user
        """
        # retrieve company info by user
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.get(
            reverse('profiles:company-detail', kwargs={'pk': self.company.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # retrieve non-existing company by user
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.get(
            reverse('profiles:company-detail', kwargs={'pk': 0}),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_destroy_company(self):
        """
         - delete company info by user
         - delete valid company by manager
         - delete non-existing company by manager
        """
        # delete company info by user
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.delete(
            reverse('profiles:company-detail', kwargs={'pk': self.company.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # delete valid company by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.delete(
            reverse('profiles:company-detail', kwargs={'pk': self.company.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # delete non-existing company by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.delete(
            reverse('profiles:company-detail', kwargs={'pk': 0}),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_company_users(self):
        """
         - retrieve company users by unauthenticated user
         - retrieve company users by community user
         - retrieve non-existing company users by community user
        """
        # retrieve company users by unauthenticated user
        response = self.client.get(
            reverse('profiles:company-users', kwargs={'pk': self.company.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # retrieve company users by community user
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.get(
            reverse('profiles:company-users', kwargs={'pk': self.company.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # retrieve non-existing company users by community user
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.get(
            reverse('profiles:company-users', kwargs={'pk': 0}),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invite_user(self):
        """
         - invite user by community user
         - invite user by company user
         - invite user by company named
         - invite user by company admin
         - invite user by staff
         - invite user by manager
        """
        # invite user by community user
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.post(
            reverse('profiles:company-invite', kwargs={'pk': self.company.id}),
            data=json.dumps(self.valid_invite_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # invite user by company user
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_user.token
        )
        response = self.client.post(
            reverse('profiles:company-invite', kwargs={'pk': self.company.id}),
            data=json.dumps(self.valid_invite_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # inviteuser by company named
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_named.token
        )
        response = self.client.post(
            reverse('profiles:company-invite', kwargs={'pk': self.company.id}),
            data=json.dumps(self.valid_invite_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # invite user by company admin
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_admin.token
        )
        response = self.client.post(
            reverse('profiles:company-invite', kwargs={'pk': self.company.id}),
            data=json.dumps(self.valid_invite_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # invite user by staff
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.staff.token
        )
        response = self.client.post(
            reverse('profiles:company-invite', kwargs={'pk': self.company.id}),
            data=json.dumps(self.valid_invite_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        msg = '{} already invited {} as {} in {}'.format(
            self.company_admin.email,
            self.valid_invite_payload['invitation']['email'],
            self.role_named.name, self.company.name
        )
        self.assertEqual(response.data[0], msg)

        # invite user by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.post(
            reverse('profiles:company-invite', kwargs={'pk': self.company.id}),
            data=json.dumps(self.valid_invite_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        msg = '{} already invited {} as {} in {}'.format(
            self.company_admin.email,
            self.valid_invite_payload['invitation']['email'],
            self.role_named.name, self.company.name
        )
        self.assertEqual(response.data[0], msg)

    def test_accept_invite(self):
        """
         - accept invite by invited user with invalid activation key
         - accept invite by invited user with valid activation key
         - accept invite by invited user twice
        """
        # accept invite by invited user with invalid activation key
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-accept-invite',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.invalid_accept_invite_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # accept invite by invited user with valid activation key
        response = self.client.post(
            reverse(
                'profiles:company-accept-invite',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_accept_invite_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # accept invite by invited user twice
        response = self.client.post(
            reverse(
                'profiles:company-accept-invite',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_accept_invite_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], 'You already accepted invitation')

    def test_revoke_inite(self):
        """
         - revoke invite by community user
         - revoke invite by company user
         - revoke invite by company named
         - revoke invite by company admin
         - revoke invite by staff
         - revoke invite by manager
        """
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

        # revoke invite by company user
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

        # revoke invite by company named
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

        # revoke invite by company admin
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

        # revoke invite by manager
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

        # revoke invite by staff
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

    def test_remove_member(self):
        """
         - remove member by community user
         - remove member by company user
         - remove member by company named
         - remove member by company admin
         - remove member by staff
         - remove member by manager
         - remove member byself
        """
        # remove member by community user
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.community_user.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-remove-member',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_remove_user_member_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # remove member by company user
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_user.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-remove-member',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_remove_user_member_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # remove member by company named
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_named.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-remove-member',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_remove_user_member_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # remove member by company admin
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_admin.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-remove-member',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_remove_user_member_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # remove member by staff
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.staff.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-remove-member',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_remove_named_member_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # remove member by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.post(
            reverse(
                'profiles:company-remove-member',
                kwargs={'pk': self.company.id}
            ),
            data=json.dumps(self.valid_remove_named_member_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # remove member byself
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

    def test_leave_company(self):
        """
         - non-company user leave company
         - company user leave company
         - company named leave company
         - company admin leave company
        """
        # non-company user leave company
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

        # company user leave company
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.company_user.token
        )
        response = self.client.get(
            reverse(
                'profiles:company-leave-company',
                kwargs={'pk': self.company.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # company named leave company
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

        # company admin leave company
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

    def test_change_role(self):
        """
         - change role by communty user
         - change role by company user
         - change role by company named
         - change role by company admin
         - change role by staff
         - change role by manager
         - change role by manager invalid
         - change role byself
        """
        # change role by communty user
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

        # change role by company user
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

        # change role by company named
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

        # change role by company admin
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

        # change role by staff
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

        # change role by manager
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

        # change role by manager invalid
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

        # change role byself
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
