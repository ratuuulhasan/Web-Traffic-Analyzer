from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from datetime import timedelta

from websites.models import Website
from analytics.models import PageView, Visitor
from analytics.realtime import get_active_visitors
from .serializers import WebsiteSerializer, PageViewSerializer, VisitorSerializer


def get_user_website(request, pk):
    """Helper to get website belonging to authenticated user."""
    api_key = request.auth
    # Restrict: API key only gives access to its own website
    if api_key and api_key.website_id != int(pk):
        from rest_framework.exceptions import PermissionDenied
        raise PermissionDenied("This API key cannot access this website.")
    return get_object_or_404(Website, pk=pk, owner=request.user)


# ============ List all websites ============
class WebsiteListView(APIView):
    def get(self, request):
        api_key = request.auth
        if api_key:
            websites = [api_key.website]
        else:
            websites = Website.objects.filter(owner=request.user)

        serializer = WebsiteSerializer(websites, many=True)
        return Response({'count': len(websites), 'results': serializer.data})


# ============ Website detail ============
class WebsiteDetailView(APIView):
    def get(self, request, pk):
        website = get_user_website(request, pk)
        serializer = WebsiteSerializer(website)
        return Response(serializer.data)


# ============ Website stats ============
class WebsiteStatsView(APIView):
    def get(self, request, pk):
        website = get_user_website(request, pk)

        # Date range from query params (default: 30 days)
        days = int(request.query_params.get('days', 30))
        days = min(days, 90)  # max 90

        since = timezone.now() - timedelta(days=days)

        pageviews = PageView.objects.filter(website=website)
        visitors = Visitor.objects.filter(website=website)

        # Basic counts
        total_views = pageviews.count()
        total_visitors = visitors.count()
        views_in_range = pageviews.filter(timestamp__gte=since).count()
        visitors_in_range = visitors.filter(last_visit__gte=since).count()

        # Daily data
        daily_data = (
            pageviews
            .filter(timestamp__gte=since)
            .annotate(day=TruncDate('timestamp'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        data_map = {item['day'].isoformat(): item['count'] for item in daily_data}

        daily = []
        today = timezone.now().date()
        for i in range(days - 1, -1, -1):
            day = today - timedelta(days=i)
            daily.append({
                'date': day.isoformat(),
                'views': data_map.get(day.isoformat(), 0),
            })

        # Top pages
        top_pages = list(
            pageviews
            .filter(timestamp__gte=since)
            .values('url')
            .annotate(views=Count('id'))
            .order_by('-views')[:10]
        )

        # Top referrers
        top_referrers = list(
            pageviews
            .filter(timestamp__gte=since)
            .exclude(referrer='')
            .values('referrer')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )

        # Country breakdown
        countries = list(
            visitors
            .exclude(country='')
            .values('country')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )

        # Browser breakdown
        browsers = list(
            visitors
            .values('browser')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )

        # Device breakdown
        devices = list(
            visitors
            .values('device')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        return Response({
            'website': {
                'id': website.id,
                'name': website.name,
                'domain': website.domain,
            },
            'range_days': days,
            'totals': {
                'page_views': total_views,
                'unique_visitors': total_visitors,
                'views_in_range': views_in_range,
                'visitors_in_range': visitors_in_range,
            },
            'daily': daily,
            'top_pages': top_pages,
            'top_referrers': top_referrers,
            'countries': countries,
            'browsers': browsers,
            'devices': devices,
        })


# ============ PageViews list (paginated) ============
class PageViewListView(APIView):
    def get(self, request, pk):
        website = get_user_website(request, pk)

        qs = PageView.objects.filter(website=website).select_related('visitor')

        # Filter by date range
        since = request.query_params.get('since')
        until = request.query_params.get('until')

        if since:
            qs = qs.filter(timestamp__gte=since)
        if until:
            qs = qs.filter(timestamp__lte=until)

        # URL filter
        url_filter = request.query_params.get('url')
        if url_filter:
            qs = qs.filter(url__icontains=url_filter)

        paginator = PageNumberPagination()
        paginator.page_size = 50
        page = paginator.paginate_queryset(qs, request)
        serializer = PageViewSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


# ============ Visitors list ============
class VisitorListView(APIView):
    def get(self, request, pk):
        website = get_user_website(request, pk)

        qs = Visitor.objects.filter(website=website).order_by('-last_visit')

        # Country filter
        country = request.query_params.get('country')
        if country:
            qs = qs.filter(country__iexact=country)

        paginator = PageNumberPagination()
        paginator.page_size = 50
        page = paginator.paginate_queryset(qs, request)
        serializer = VisitorSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


# ============ Real-time count ============
class RealtimeView(APIView):
    def get(self, request, pk):
        website = get_user_website(request, pk)
        active = get_active_visitors(website.id)

        visitors = []
        for vid, data in active.items():
            data['visitor_id'] = vid
            visitors.append(data)

        visitors.sort(key=lambda x: x.get('last_seen', ''), reverse=True)

        return Response({
            'count': len(visitors),
            'visitors': visitors[:50],
            'window_seconds': 300,
        })


# ============ Country breakdown ============
class CountryBreakdownView(APIView):
    def get(self, request, pk):
        website = get_user_website(request, pk)

        countries = list(
            Visitor.objects
            .filter(website=website)
            .exclude(country='')
            .values('country')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        return Response({
            'total_countries': len(countries),
            'countries': countries,
        })