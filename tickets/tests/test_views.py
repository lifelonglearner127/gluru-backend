import json
from django.urls import reverse
from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APITestCase
from profiles.models import User


class TicketCreateTest(APITestCase):
    """
    Test module for creating a new ticket
    """
    def setUp(self):
        call_command('loaddata', 'data', verbosity=0)

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

    def test_create_ticket_by_unauthorized_user(self):
        response = self.client.post(
            reverse('tickets:ticket-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_valid_ticket(self):
        user = User.objects.create_user(
            email='admin@example.com',
            password='gibupjo127'
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.token)
        response = self.client.post(
            reverse('tickets:ticket-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_ticket(self):
        user = User.objects.create_user(
            email='admin@example.com',
            password='gibupjo127'
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.token)
        response = self.client.post(
            reverse('tickets:ticket-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
