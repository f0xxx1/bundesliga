from django.test import TestCase
from django.urls import reverse, resolve

from ..views import search_view


class TestSearchPage(TestCase):

    def setUp(self):
        url = reverse("core:search")
        self.response = self.client.get(url+'?q=fc')

    def test_search_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_search_view_template(self):
        view = resolve("/search/")
        self.assertEquals(view.func, search_view)

    def test_search_view_contains_string(self):
        self.assertContains(self.response, "1. FC Nürnberg")
