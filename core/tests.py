import datetime

from django.test import TestCase, override_settings


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class AcceptanceTests(TestCase):
    """ Site acceptance tests for core functions """

    def test_homepage_returns(self):
        """ Make sure the homepage responds with something. """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Memorials at Whitkirk")
