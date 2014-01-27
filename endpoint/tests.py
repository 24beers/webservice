from django.test import TestCase
from rest_framework.test import APIRequestFactory


class EndpointAuthTest(TestCase):
    def auth_test(self):
        factory = APIRequestFactory
        request = factory.get('/endpoint/auth/', )