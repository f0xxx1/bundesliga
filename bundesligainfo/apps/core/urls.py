from django.urls import path

from .views import index_view, current_season_view, help_view, search_view

urlpatterns = [
    path("", index_view, name="index"),
    path("season/", current_season_view, name="current_season"),
    path("help/", help_view, name="help"),
    path("search/", search_view, name="search"),
]
