import json
from django.urls import reverse
from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APITestCase
from profiles.models import User
from info.models import (
    GluuServer, GluuOS, GluuProduct,
    TicketCategory, TicketIssueType, TicketStatus, UserRole, Permission
)


class GluuServerViewSetTest(APITestCase):

    def setUp(self):
        self.manager = User.objects.create_superuser(
            email='manager@gmail.com',
            password='manager'
        )

        self.user = User.objects.create_user(
            email='user@gmail.org',
            password='user'
        )

        self.valid_payload = {
            "server": {
                "name": "3.4.1"
            }
        }

        self.invalid_payload = {
            "server": {
                "name": ""
            }
        }

        self.server = GluuServer.objects.create(name='3.4.5')

    def test_create_info(self):
        """
         - create info by user
         - create valid info by manager
         - create invalid info by manager
        """
        # create info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.post(
            reverse('info:server-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # create valid info by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.post(
            reverse('info:server-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # create invalid info by manager
        response = self.client.post(
            reverse('info:server-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_info(self):
        """
         - update info by user
         - update valid info by manager
         - update invalid info by manager
         - update non-existing info by manager
        """
        # update info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.put(
            reverse('info:server-detail', kwargs={'pk': self.server.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # update valid info by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.put(
            reverse('info:server-detail', kwargs={'pk': self.server.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # update invalid info by manager
        response = self.client.put(
            reverse('info:server-detail', kwargs={'pk': self.server.id}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # update non-existing info by manager
        response = self.client.put(
            reverse('info:server-detail', kwargs={'pk': 0}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_info(self):
        """
         - retrieve info by user
         - retrieve non-existing info by user
        """
        # retrieve info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.get(
            reverse('info:server-detail', kwargs={'pk': self.server.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # retrieve non-existing info by user
        response = self.client.get(
            reverse('info:server-detail', kwargs={'pk': 0})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_info(self):
        """
         - delete info by user
         - delete valid info by manager
         - delete non-existing info by manager
        """
        # delete info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.delete(
            reverse('info:server-detail', kwargs={'pk': self.server.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # delete valid info by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.delete(
            reverse('info:server-detail', kwargs={'pk': self.server.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # delete non-existing info by manager
        response = self.client.delete(
            reverse('info:server-detail', kwargs={'pk': 0}),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GluuOSViewSetTest(APITestCase):

    def setUp(self):
        self.manager = User.objects.create_superuser(
            email='manager@gmail.com',
            password='manager'
        )

        self.user = User.objects.create_user(
            email='user@gmail.org',
            password='user'
        )

        self.valid_payload = {
            "os": {
                "name": "CentOS7"
            }
        }

        self.invalid_payload = {
            "os": {
                "name": ""
            }
        }

        self.os = GluuOS.objects.create(name='Ubuntu')

    def test_create_info(self):
        """
         - create info by user
         - create valid info by manager
         - create invalid info by manager
        """
        # create info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.post(
            reverse('info:os-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # create valid info by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.post(
            reverse('info:os-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # create invalid info by manager
        response = self.client.post(
            reverse('info:os-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_info(self):
        """
         - update info by user
         - update valid info by manager
         - update invalid info by manager
         - update non-existing info by manager
        """
        # update info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.put(
            reverse('info:os-detail', kwargs={'pk': self.os.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # update valid info by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.put(
            reverse('info:os-detail', kwargs={'pk': self.os.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # update invalid info by manager
        response = self.client.put(
            reverse('info:os-detail', kwargs={'pk': self.os.id}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # update non-existing info by manager
        response = self.client.put(
            reverse('info:os-detail', kwargs={'pk': 0}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_info(self):
        """
         - retrieve info by user
         - retrieve non-existing info by user
        """
        # retrieve info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.get(
            reverse('info:os-detail', kwargs={'pk': self.os.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # retrieve non-existing info by user
        response = self.client.get(
            reverse('info:os-detail', kwargs={'pk': 0})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_info(self):
        """
         - delete info by user
         - delete valid info by manager
         - delete non-existing info by manager
        """
        # delete info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.delete(
            reverse('info:os-detail', kwargs={'pk': self.os.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # delete valid info by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.delete(
            reverse('info:os-detail', kwargs={'pk': self.os.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # delete non-existing info by manager
        response = self.client.delete(
            reverse('info:os-detail', kwargs={'pk': 0}),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GluuProductViewsetTest(APITestCase):

    def setUp(self):
        self.manager = User.objects.create_superuser(
            email='manager@gmail.com',
            password='manager'
        )

        self.user = User.objects.create_user(
            email='user@gmail.org',
            password='user'
        )

        self.valid_payload = {
            "product": {
                "name": "Super Gluu"
            }
        }

        self.invalid_payload = {
            "product": {
                "name": ""
            }
        }

        self.product = GluuProduct.objects.create(name='Oxd')

    def test_create_info(self):
        """
         - create info by user
         - create valid info by manager
         - create invalid info by manager
        """
        # create info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.post(
            reverse('info:product-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # create valid info by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.post(
            reverse('info:product-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # create invalid info by manager
        response = self.client.post(
            reverse('info:product-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_info(self):
        """
         - update info by user
         - update valid info by manager
         - update invalid info by manager
         - update non-existing info by manager
        """
        # update info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.put(
            reverse('info:product-detail', kwargs={'pk': self.product.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # update valid info by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.put(
            reverse('info:product-detail', kwargs={'pk': self.product.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # update invalid info by manager
        response = self.client.put(
            reverse('info:product-detail', kwargs={'pk': self.product.id}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # update non-existing info by manager
        response = self.client.put(
            reverse('info:product-detail', kwargs={'pk': 0}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_info(self):
        """
         - retrieve info by user
         - retrieve non-existing info by user
        """
        # retrieve info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.get(
            reverse('info:product-detail', kwargs={'pk': self.product.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # retrieve non-existing info by user
        response = self.client.get(
            reverse('info:product-detail', kwargs={'pk': 0})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_info(self):
        """
         - delete info by user
         - delete valid info by manager
         - delete non-existing info by manager
        """
        # delete info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.delete(
            reverse('info:product-detail', kwargs={'pk': self.product.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # delete valid info by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.delete(
            reverse('info:product-detail', kwargs={'pk': self.product.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # delete non-existing info by manager
        response = self.client.delete(
            reverse('info:product-detail', kwargs={'pk': 0}),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TicketCategoryViewSetTest(APITestCase):

    def setUp(self):
        self.manager = User.objects.create_superuser(
            email='manager@gmail.com',
            password='manager'
        )

        self.user = User.objects.create_user(
            email='user@gmail.org',
            password='user'
        )

        self.valid_payload = {
            "ticket_category": {
                "name": "Super Gluu"
            }
        }

        self.invalid_payload = {
            "ticket_category": {
                "name": ""
            }
        }

        self.category = TicketCategory.objects.create(name='Oxd')

    def test_create_info(self):
        """
         - create info by user
         - create valid info by manager
         - create invalid info by manager
        """
        # create info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.post(
            reverse('info:category-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # create valid info by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.post(
            reverse('info:category-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # create invalid info by manager
        response = self.client.post(
            reverse('info:category-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_info(self):
        """
         - update info by user
         - update valid info by manager
         - update invalid info by manager
         - update non-existing info by manager
        """
        # update info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.put(
            reverse('info:category-detail', kwargs={'pk': self.category.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # update valid info by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.put(
            reverse('info:category-detail', kwargs={'pk': self.category.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # update invalid info by manager
        response = self.client.put(
            reverse('info:category-detail', kwargs={'pk': self.category.id}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # update non-existing info by manager
        response = self.client.put(
            reverse('info:category-detail', kwargs={'pk': 0}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_info(self):
        """
         - retrieve info by user
         - retrieve non-existing info by user
        """
        # retrieve info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.get(
            reverse('info:category-detail', kwargs={'pk': self.category.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # retrieve non-existing info by user
        response = self.client.get(
            reverse('info:category-detail', kwargs={'pk': 0})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_info(self):
        """
         - delete info by user
         - delete valid info by manager
         - delete non-existing info by manager
        """
        # delete info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.delete(
            reverse('info:category-detail', kwargs={'pk': self.category.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # delete valid info by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.delete(
            reverse('info:category-detail', kwargs={'pk': self.category.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # delete non-existing info by manager
        response = self.client.delete(
            reverse('info:category-detail', kwargs={'pk': 0}),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TicketIssueTypeViewSetTest(APITestCase):

    def setUp(self):
        self.manager = User.objects.create_superuser(
            email='manager@gmail.com',
            password='manager'
        )

        self.user = User.objects.create_user(
            email='user@gmail.org',
            password='user'
        )

        self.valid_payload = {
            "ticket_issue_type": {
                "name": "Pre-Production Issue"
            }
        }

        self.invalid_payload = {
            "ticket_issue_type": {
                "name": ""
            }
        }

        self.type = TicketIssueType.objects.create(name='New Issue')

    def test_create_info(self):
        """
         - create info by user
         - create valid info by manager
         - create invalid info by manager
        """
        # create info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.post(
            reverse('info:type-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # create valid info by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.post(
            reverse('info:type-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # create invalid info by manager
        response = self.client.post(
            reverse('info:type-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_info(self):
        """
         - update info by user
         - update valid info by manager
         - update invalid info by manager
         - update non-existing info by manager
        """
        # update info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.put(
            reverse('info:type-detail', kwargs={'pk': self.type.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # update valid info by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.put(
            reverse('info:type-detail', kwargs={'pk': self.type.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # update invalid info by manager
        response = self.client.put(
            reverse('info:type-detail', kwargs={'pk': self.type.id}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # update non-existing info by manager
        response = self.client.put(
            reverse('info:type-detail', kwargs={'pk': 0}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_info(self):
        """
         - retrieve info by user
         - retrieve non-existing info by user
        """
        # retrieve info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.get(
            reverse('info:type-detail', kwargs={'pk': self.type.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # retrieve non-existing info by user
        response = self.client.get(
            reverse('info:type-detail', kwargs={'pk': 0})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_info(self):
        """
         - delete info by user
         - delete valid info by manager
         - delete non-existing info by manager
        """
        # delete info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.delete(
            reverse('info:type-detail', kwargs={'pk': self.type.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # delete valid info by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.delete(
            reverse('info:type-detail', kwargs={'pk': self.type.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # delete non-existing info by manager
        response = self.client.delete(
            reverse('info:type-detail', kwargs={'pk': 0}),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TicketStatusViewSetTest(APITestCase):

    def setUp(self):
        self.manager = User.objects.create_superuser(
            email='manager@gmail.com',
            password='manager'
        )

        self.user = User.objects.create_user(
            email='user@gmail.org',
            password='user'
        )

        self.valid_payload = {
            "ticket_status": {
                "name": "assigned"
            }
        }

        self.invalid_payload = {
            "ticket_status": {
                "name": ""
            }
        }

        self.status = TicketStatus.objects.create(name='new')

    def test_create_info(self):
        """
         - create info by user
         - create valid info by manager
         - create invalid info by manager
        """
        # create info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.post(
            reverse('info:status-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # create valid info by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.post(
            reverse('info:status-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # create invalid info by manager
        response = self.client.post(
            reverse('info:status-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_info(self):
        """
         - update info by user
         - update valid info by manager
         - update invalid info by manager
         - update non-existing info by manager
        """
        # update info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.put(
            reverse('info:status-detail', kwargs={'pk': self.status.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # update valid info by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.put(
            reverse('info:status-detail', kwargs={'pk': self.status.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # update invalid info by manager
        response = self.client.put(
            reverse('info:status-detail', kwargs={'pk': self.status.id}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # update non-existing info by manager
        response = self.client.put(
            reverse('info:status-detail', kwargs={'pk': 0}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_info(self):
        """
         - retrieve info by user
         - retrieve non-existing info by user
        """
        # retrieve info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.get(
            reverse('info:status-detail', kwargs={'pk': self.status.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # retrieve non-existing info by user
        response = self.client.get(
            reverse('info:status-detail', kwargs={'pk': 0})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_info(self):
        """
         - delete info by user
         - delete valid info by manager
         - delete non-existing info by manager
        """
        # delete info by user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.delete(
            reverse('info:status-detail', kwargs={'pk': self.status.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # delete valid info by manager
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.manager.token
        )
        response = self.client.delete(
            reverse('info:status-detail', kwargs={'pk': self.status.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # delete non-existing info by manager
        response = self.client.delete(
            reverse('info:status-detail', kwargs={'pk': 0}),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserRoleViewSetTest(APITestCase):
    def setUp(self):
        call_command('loaddata', 'permission', verbosity=0)

        self.admin = User.objects.create_superuser(
            email='admin@gluu.org',
            password='admin'
        )

        self.user = User.objects.create_user(
            email='user@gluu.org',
            password='user'
        )

        self.valid_payload = {
            "role": {
                "name": "custom",
                "permissions": [1, 2]
            }
        }

        self.invalid_payload = {
            "role": {
                "name": ""
            }
        }

        self.role = UserRole.objects.create(name='new')

    def test_create_info_by_not_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.post(
            reverse('info:role-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.post(
            reverse('info:role-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_info_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.post(
            reverse('info:role-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_info_by_not_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.put(
            reverse('info:role-detail', kwargs={'pk': self.role.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.put(
            reverse('info:role-detail', kwargs={'pk': self.role.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_info_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.put(
            reverse('info:role-detail', kwargs={'pk': self.role.id}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_non_existing(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.put(
            reverse('info:role-detail', kwargs={'pk': 30}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.get(
            reverse('info:role-detail', kwargs={'pk': self.role.id}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_info_invalid(self):
        response = self.client.get(
            reverse('info:role-detail', kwargs={'pk': 30}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_info_by_not_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.delete(
            reverse('info:role-detail', kwargs={'pk': self.role.id}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.delete(
            reverse('info:role-detail', kwargs={'pk': self.role.id}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_info_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.delete(
            reverse('info:role-detail', kwargs={'pk': 30}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PermissionViewSetTest(APITestCase):
    def setUp(self):

        self.admin = User.objects.create_superuser(
            email='admin@gluu.org',
            password='admin'
        )

        self.user = User.objects.create_user(
            email='user@gluu.org',
            password='user'
        )

        self.valid_payload = {
            "permission": {
                "app_name": "tickets",
                "model_name": "Ticket",
                "actions": "create",
                "description": "Create Ticket"
            }
        }

        self.invalid_payload = {
            "permission": {
                "app_name": "",
                "model_name": "Ticket",
                "actions": "create",
                "description": "Create Ticket"
            }
        }

        self.permission = Permission.objects.create(
            app_name="tickets", model_name="Ticket", actions="update",
            description="abc"
        )

    def test_create_info_by_not_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.post(
            reverse('info:permission-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.post(
            reverse('info:permission-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_info_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.post(
            reverse('info:permission-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_info_by_not_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.put(
            reverse(
                'info:permission-detail',
                kwargs={'pk': self.permission.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.put(
            reverse(
                'info:permission-detail',
                kwargs={'pk': self.permission.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_info_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.put(
            reverse(
                'info:permission-detail',
                kwargs={'pk': self.permission.id}
            ),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_non_existing(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.put(
            reverse('info:permission-detail', kwargs={'pk': 30}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.get(
            reverse(
                'info:permission-detail',
                kwargs={'pk': self.permission.id}
            ),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_info_invalid(self):
        response = self.client.get(
            reverse('info:permission-detail', kwargs={'pk': 0}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_info_by_not_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.delete(
            reverse(
                'info:permission-detail',
                kwargs={'pk': self.permission.id}
            ),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.delete(
            reverse(
                'info:permission-detail',
                kwargs={'pk': self.permission.id}
            ),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_info_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.delete(
            reverse('info:permission-detail', kwargs={'pk': 30}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
