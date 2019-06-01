from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.cache import cache
from django.core.paginator import Paginator

from .openligasdk.openligasdk import OpenLigaSDK


def index_view(request):
    """
    The index view of the page, it shows both Rankings and
    the upcoming matches (this weekend).
    Route: '/'
    """
    openligasdk = OpenLigaSDK()

    if cache.get("rankings") is None:
        # Get Current Rankings
        rankings = openligasdk.get_rankings("2018")
        cache.set("rankings", rankings, 60)

    if cache.get("upcoming_matches") is None:
        # Get Upcoming Matches
        upcoming_matches = openligasdk.get_weekend_matches("2018")
        cache.set("upcoming_matches", upcoming_matches, 60)

    template_name = "core/index.html"

    context = {
        "rankings": cache.get("rankings"),
        "upcoming_matches": cache.get("upcoming_matches"),
    }

    return render(request, template_name, context)


def current_season_view(request):
    """
    Getting the current season(bundesliga 2018)
    Route: '/season/'
    """
    openligasdk = OpenLigaSDK()
    page = request.GET.get("page", 1)
    season_matches = None

    if cache.get("season_matches") is None:
        # Getting current Season
        season_matches = openligasdk.get_season("2018", reverse=True)
        cache.set("season_matches", season_matches, 60 * 60)
    else:
        season_matches = cache.get("season_matches")

    season_matches_paginated = Paginator(season_matches, 15).page(page)

    template_name = "core/current_season.html"

    context = {"season_matches": season_matches_paginated, "is_paginated": True}

    return render(request, template_name, context)


def help_view(request):
    """
    Helping view of the page
    Route: '/help/'
    """
    template_name = "core/help.html"
    return render(request, template_name)


def search_view(request):
    """
    Searching view for the teams.
    Route: /search/
    Accepts: GET Request with 'q' as a query string.
    """
    openligasdk = OpenLigaSDK()

    if "q" in request.GET:
        query_string = str(request.GET["q"])
        search_results = openligasdk.search_team(query_string, "2018")
        context = {"search_results": search_results, "query_string": query_string}
    else:
        context = {}
    template_name = "core/search.html"
    return render(request, template_name, context)
