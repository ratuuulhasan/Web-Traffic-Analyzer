import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from user_agents import parse
from websites.models import Website
from .models import Visitor, PageView, Event
from django.db.models.functions import TruncDate
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import PageView, Visitor
from django.contrib.gis.geoip2 import GeoIP2, GeoIP2Exception
import geoip2.errors
from .realtime import mark_visitor_active, get_active_visitors
from .realtime import get_all_active_summary
from django.shortcuts import get_object_or_404
from .realtime import get_active_visitors
from .country_coords import get_coords
import random




def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def get_country_from_ip(ip_address):
    if not ip_address:
        return {}

    try:
        g = GeoIP2()
        response = g.country(ip_address)
        return {
            'country_code': response.get('country_code', ''),
            'country_name': response.get('country_name', ''),
        }
    except (GeoIP2Exception, geoip2.errors.AddressNotFoundError):
        return {}
    except Exception:
        return {}


@csrf_exempt
def track_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    tracking_id = data.get('tracking_id')
    url = data.get('url', '')
    page_title = data.get('title', '')
    referrer = data.get('referrer', '')
    visitor_id = data.get('visitor_id')

    if not tracking_id or not visitor_id:
        return JsonResponse({'error': 'Missing fields'}, status=400)

    try:
        website = Website.objects.get(tracking_id=tracking_id)
    except Website.DoesNotExist:
        return JsonResponse({'error': 'Invalid tracking id'}, status=404)

    # User-agent parse
    
    ua_string = request.META.get('HTTP_USER_AGENT', '')
    ua = parse(ua_string)
    browser = ua.browser.family
    os_name = ua.os.family
    if ua.is_mobile:
        device = 'Mobile'
    elif ua.is_tablet:
        device = 'Tablet'
    elif ua.is_pc:
        device = 'PC'
    else:
        device = 'Other'

    ip = get_client_ip(request)
    country_info = get_country_from_ip(ip)

    # Visitor create/update
    
    country_info = get_country_from_ip(ip)
    country_name = country_info.get('country_name', '')

    visitor, created = Visitor.objects.get_or_create(
        visitor_id=visitor_id,
        website=website,
        defaults={
            'ip_address': ip,
            'country': country_name,
            'browser': browser,
            'os': os_name,
            'device': device,
        }
    )

    if not created and not visitor.country and country_name:
        visitor.country = country_name
        visitor.save(update_fields=['country'])

    # PageView save
    PageView.objects.create(
        website=website,
        visitor=visitor,
        url=url,
        page_title=page_title,
        referrer=referrer,
    )

    # ⚡ Mark visitor as active (realtime)
    mark_visitor_active(
        website_id=website.id,
        visitor_id=visitor_id,
        data={
            'url': url,
            'page_title': page_title,
            'country': country_name or visitor.country or 'Unknown',
            'browser': browser,
            'os': os_name,
            'device': device,
            'referrer': referrer[:100] if referrer else '',
        }
    )

    return JsonResponse({'status': 'ok'})


@login_required
def stats_api(request):
    """API endpoint to get dashboard stats"""
    websites = request.user.websites.all()

    # Total stats
    total_views = PageView.objects.filter(website__in=websites).count()
    total_visitors = Visitor.objects.filter(website__in=websites).count()

    # Last 7 days data
    seven_days_ago = timezone.now() - timedelta(days=7)
    daily_data = (
        PageView.objects
        .filter(website__in=websites, timestamp__gte=seven_days_ago)
        .annotate(day=TruncDate('timestamp'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    # Build last 7 days labels
    labels = []
    counts = []
    today = timezone.now().date()
    data_map = {item['day']: item['count'] for item in daily_data}

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        labels.append(day.strftime('%d %b'))
        counts.append(data_map.get(day, 0))

    # Browser breakdown
    browser_data = (
        Visitor.objects
        .filter(website__in=websites)
        .values('browser')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

     
    country_data = (
        Visitor.objects
        .filter(website__in=websites)
        .exclude(country='')
        .values('country')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

    return JsonResponse({
        'total_views': total_views,
        'total_visitors': total_visitors,
        'total_websites': websites.count(),
        'daily_labels': labels,
        'daily_counts': counts,
        'browsers': {
            'labels': [b['browser'] or 'Unknown' for b in browser_data],
            'counts': [b['count'] for b in browser_data],
        },
        'countries': {
            'labels': [c['country'] for c in country_data],
            'counts': [c['count'] for c in country_data],
        },
    })

@login_required
def realtime_api(request):
    """API to get real-time visitor data for user's websites."""
    websites = request.user.websites.all()

    summary = get_all_active_summary(websites)

    return JsonResponse({
        'count': summary['total'],
        'visitors': summary['visitors'][:20],  # max 20
        'timestamp': timezone.now().isoformat(),
    })


@login_required
def realtime_website_api(request, pk):
    """API for single website realtime data."""
    from websites.models import Website
    from django.shortcuts import get_object_or_404

    website = get_object_or_404(Website, pk=pk, owner=request.user)
    active = get_active_visitors(website.id)

    visitors = []
    for vid, data in active.items():
        data['visitor_id'] = vid
        visitors.append(data)

    visitors.sort(key=lambda x: x.get('last_seen', ''), reverse=True)

    return JsonResponse({
        'count': len(visitors),
        'visitors': visitors[:20],
        'timestamp': timezone.now().isoformat(),
    })


@login_required
def website_stats_api(request, pk):
    """Detailed stats for a single website."""
    website = get_object_or_404(Website, pk=pk, owner=request.user)

    pageviews = PageView.objects.filter(website=website)
    visitors = Visitor.objects.filter(website=website)

    # Last 30 days daily data
    thirty_days_ago = timezone.now() - timedelta(days=30)
    from django.db.models.functions import TruncDate

    daily_data = (
        pageviews
        .filter(timestamp__gte=thirty_days_ago)
        .annotate(day=TruncDate('timestamp'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    data_map = {item['day']: item['count'] for item in daily_data}

    labels = []
    counts = []
    today = timezone.now().date()
    for i in range(29, -1, -1):
        day = today - timedelta(days=i)
        labels.append(day.strftime('%d %b'))
        counts.append(data_map.get(day, 0))

    # Browser breakdown
    browser_data = (
        visitors
        .values('browser')
        .annotate(count=Count('id'))
        .order_by('-count')[:6]
    )

    # OS breakdown
    os_data = (
        visitors
        .values('os')
        .annotate(count=Count('id'))
        .order_by('-count')[:6]
    )

    # Device breakdown
    device_data = (
        visitors
        .values('device')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Country breakdown
    country_data = (
        visitors
        .exclude(country='')
        .values('country')
        .annotate(count=Count('id'))
        .order_by('-count')[:8]
    )

    # Realtime count for this website
    realtime_count = len(get_active_visitors(website.id))

    return JsonResponse({
        'daily_labels': labels,
        'daily_counts': counts,
        'browsers': {
            'labels': [b['browser'] or 'Unknown' for b in browser_data],
            'counts': [b['count'] for b in browser_data],
        },
        'os': {
            'labels': [o['os'] or 'Unknown' for o in os_data],
            'counts': [o['count'] for o in os_data],
        },
        'devices': {
            'labels': [d['device'] or 'Unknown' for d in device_data],
            'counts': [d['count'] for d in device_data],
        },
        'countries': {
            'labels': [c['country'] for c in country_data],
            'counts': [c['count'] for c in country_data],
        },
        'realtime_count': realtime_count,
    })

@csrf_exempt
def track_event_view(request):
    """Track custom events."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    tracking_id = data.get('tracking_id')
    visitor_id = data.get('visitor_id')
    event_name = data.get('event_name')
    properties = data.get('properties', {})
    url = data.get('url', '')

    if not all([tracking_id, visitor_id, event_name]):
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    # Validate properties (must be dict, small)
    if not isinstance(properties, dict):
        properties = {}

    # Limit properties size
    properties = {str(k)[:50]: str(v)[:500] for k, v in list(properties.items())[:20]}

    try:
        website = Website.objects.get(tracking_id=tracking_id)
    except Website.DoesNotExist:
        return JsonResponse({'error': 'Invalid tracking id'}, status=404)

    # Get or create visitor
    visitor, _ = Visitor.objects.get_or_create(
        visitor_id=visitor_id,
        website=website,
    )

    # Save event
    Event.objects.create(
        website=website,
        visitor=visitor,
        name=event_name[:100],
        properties=properties,
        url=url[:500],
    )

    return JsonResponse({'status': 'ok'})


@login_required
def website_events_api(request, pk):
    """Get events data for a website."""
    from websites.models import Website
    from django.shortcuts import get_object_or_404

    website = get_object_or_404(Website, pk=pk, owner=request.user)

    # Optional: filter by event name
    event_filter = request.GET.get('name', '').strip()

    qs = Event.objects.filter(website=website)
    if event_filter:
        qs = qs.filter(name=event_filter)

    # Top event names
    top_events = list(
        qs.values('name')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )

    # Events per day (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    daily = (
        qs.filter(timestamp__gte=thirty_days_ago)
        .annotate(day=TruncDate('timestamp'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    daily_map = {item['day'].isoformat(): item['count'] for item in daily}

    labels = []
    counts = []
    today = timezone.now().date()
    for i in range(29, -1, -1):
        day = today - timedelta(days=i)
        labels.append(day.strftime('%d %b'))
        counts.append(daily_map.get(day.isoformat(), 0))

    return JsonResponse({
        'total_events': qs.count(),
        'unique_event_types': qs.values('name').distinct().count(),
        'top_events': top_events,
        'daily_labels': labels,
        'daily_counts': counts,
    })


@login_required
def website_events_list_api(request, pk):
    """Paginated list of events (for table)."""
    from websites.models import Website
    from django.shortcuts import get_object_or_404
    from django.core.paginator import Paginator

    website = get_object_or_404(Website, pk=pk, owner=request.user)

    qs = Event.objects.filter(website=website).select_related('visitor')

    # Filter by event name
    event_filter = request.GET.get('name', '').strip()
    if event_filter:
        qs = qs.filter(name=event_filter)

    # Pagination
    page_num = int(request.GET.get('page', 1))
    page_size = 50
    paginator = Paginator(qs, page_size)
    page = paginator.get_page(page_num)

    events = []
    for e in page:
        events.append({
            'id': e.id,
            'name': e.name,
            'properties': e.properties,
            'url': e.url,
            'visitor_id': e.visitor.visitor_id if e.visitor else '',
            'country': e.visitor.country if e.visitor else '',
            'timestamp': e.timestamp.isoformat(),
        })

    return JsonResponse({
        'events': events,
        'page': page.number,
        'total_pages': paginator.num_pages,
        'total': paginator.count,
        'has_next': page.has_next(),
        'has_prev': page.has_previous(),
    })

@login_required
def map_data_api(request, pk):
    """Return location data for map markers."""
    from websites.models import Website
    from django.shortcuts import get_object_or_404
    from .realtime import get_active_visitors

    website = get_object_or_404(Website, pk=pk, owner=request.user)

    # Active visitors (last 5 min)
    active = get_active_visitors(website.id)

    markers = []
    country_counts = {}

    for vid, data in active.items():
        country = data.get('country', 'Unknown')

        # Skip if we can't determine coordinates
        coords = get_coords(country)
        if not coords:
            continue

        lat, lng = coords

        # Small random offset so multiple visitors from same country don't overlap
        lat += random.uniform(-1.5, 1.5)
        lng += random.uniform(-1.5, 1.5)

        markers.append({
            'lat': lat,
            'lng': lng,
            'country': country,
            'visitor_id': vid,
            'url': data.get('url', ''),
            'page_title': data.get('page_title', ''),
            'browser': data.get('browser', ''),
            'os': data.get('os', ''),
            'device': data.get('device', ''),
            'last_seen': data.get('last_seen', ''),
        })

        country_counts[country] = country_counts.get(country, 0) + 1

    # Sort countries by count
    top_countries = sorted(
        [{'country': k, 'count': v} for k, v in country_counts.items()],
        key=lambda x: -x['count']
    )

    return JsonResponse({
        'count': len(markers),
        'markers': markers,
        'top_countries': top_countries,
        'timestamp': timezone.now().isoformat(),
    })


@login_required
def map_history_api(request, pk):
    """Historical map data (visitors in last N days)."""
    from websites.models import Website
    from django.shortcuts import get_object_or_404

    website = get_object_or_404(Website, pk=pk, owner=request.user)

    days = int(request.GET.get('days', 7))
    days = min(max(days, 1), 90)
    since = timezone.now() - timedelta(days=days)

    visitors = (
        Visitor.objects
        .filter(website=website, last_visit__gte=since)
        .exclude(country='')
        .values('country')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    markers = []
    for v in visitors:
        coords = get_coords(v['country'])
        if not coords:
            continue
        lat, lng = coords
        # Larger offset for country-level aggregation
        lat += random.uniform(-2, 2)
        lng += random.uniform(-2, 2)
        markers.append({
            'lat': lat,
            'lng': lng,
            'country': v['country'],
            'count': v['count'],
        })

    return JsonResponse({
        'markers': markers,
        'days': days,
    })