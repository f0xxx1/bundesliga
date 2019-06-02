from django.test import TestCase
from django.urls import reverse, resolve

from ..views import index_view, current_season_view, help_view


class TestIndexView(TestCase):

    def setUp(self):
        url = reverse("core:index")
        self.response = self.client.get(url)

    def test_index_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_index_view_template(self):
        view = resolve("/")
        self.assertEquals(view.func, index_view)


class TestCurrentSeasonView(TestCase):

    def setUp(self):
        url = reverse("core:current_season")
        self.response = self.client.get(url)

    def test_current_season_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_current_season_template(self):
        view = resolve("/season/")
        self.assertEquals(view.func, current_season_view)


class TestHelpViewPage(TestCase):

    def setUp(self):
        url = reverse("core:help")
        self.response = self.client.get(url)

    def test_help_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_help_view_template(self):
        view = resolve("/help/")
        self.assertEquals(view.func, help_view)
