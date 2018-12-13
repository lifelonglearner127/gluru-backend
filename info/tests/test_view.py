import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from profiles.models import User
from info.models import GluuServer, GluuOS, GluuProduct


class GluuServerViewSetTest(APITestCase):
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

    def test_create_info_by_not_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.post(
            reverse('info:server-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.post(
            reverse('info:server-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_info_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.post(
            reverse('info:server-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_info_by_not_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.put(
            reverse('info:server-detail', kwargs={'pk': self.server.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.put(
            reverse('info:server-detail', kwargs={'pk': self.server.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_info_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.put(
            reverse('info:server-detail', kwargs={'pk': self.server.id}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_non_existing(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.put(
            reverse('info:server-detail', kwargs={'pk': 30}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.get(
            reverse('info:server-detail', kwargs={'pk': self.server.id}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_info_invalid(self):
        response = self.client.get(
            reverse('info:server-detail', kwargs={'pk': 30}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_info_by_not_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.delete(
            reverse('info:server-detail', kwargs={'pk': self.server.id}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.delete(
            reverse('info:server-detail', kwargs={'pk': self.server.id}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_info_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.delete(
            reverse('info:server-detail', kwargs={'pk': 30}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GluuOSViewSetTest(APITestCase):
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

    def test_create_info_by_not_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.post(
            reverse('info:os-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.post(
            reverse('info:os-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_info_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.post(
            reverse('info:os-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_info_by_not_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.put(
            reverse('info:os-detail', kwargs={'pk': self.os.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.put(
            reverse('info:os-detail', kwargs={'pk': self.os.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_info_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.put(
            reverse('info:os-detail', kwargs={'pk': self.os.id}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_non_existing(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.put(
            reverse('info:os-detail', kwargs={'pk': 30}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.get(
            reverse('info:os-detail', kwargs={'pk': self.os.id}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_info_invalid(self):
        response = self.client.get(
            reverse('info:os-detail', kwargs={'pk': 30}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_info_by_not_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.delete(
            reverse('info:os-detail', kwargs={'pk': self.os.id}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.delete(
            reverse('info:os-detail', kwargs={'pk': self.os.id}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_info_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.delete(
            reverse('info:os-detail', kwargs={'pk': 30}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GluuProductViewsetTest(APITestCase):
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

    def test_create_info_by_not_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.post(
            reverse('info:product-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.post(
            reverse('info:product-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_info_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.post(
            reverse('info:product-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_info_by_not_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.put(
            reverse('info:product-detail', kwargs={'pk': self.product.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.put(
            reverse('info:product-detail', kwargs={'pk': self.product.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_info_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.put(
            reverse('info:product-detail', kwargs={'pk': self.product.id}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_non_existing(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.put(
            reverse('info:product-detail', kwargs={'pk': 30}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.get(
            reverse('info:product-detail', kwargs={'pk': self.product.id}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_info_invalid(self):
        response = self.client.get(
            reverse('info:product-detail', kwargs={'pk': 30}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_info_by_not_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.delete(
            reverse('info:product-detail', kwargs={'pk': self.product.id}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.delete(
            reverse('info:product-detail', kwargs={'pk': self.product.id}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_info_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.token)
        response = self.client.delete(
            reverse('info:product-detail', kwargs={'pk': 30}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TicketCategoryViewSetTest(APITestCase):
    pass


class TicketIssueTypeViewSetTest(APITestCase):
    pass


class TicketStatusViewSetTest(APITestCase):
    pass
