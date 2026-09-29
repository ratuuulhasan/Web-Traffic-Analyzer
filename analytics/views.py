import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from user_agents import parse
from websites.models import Website
from .models import Visitor, PageView
from django.db.models.functions import TruncDate
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import PageView, Visitor




def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0]
    return request.META.get('REMOTE_ADDR')


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

    # Visitor create/update
    visitor, created = Visitor.objects.get_or_create(
        visitor_id=visitor_id,
        website=website,
        defaults={
            'ip_address': ip,
            'browser': browser,
            'os': os_name,
            'device': device,
        }
    )

    # PageView save
    PageView.objects.create(
        website=website,
        visitor=visitor,
        url=url,
        page_title=page_title,
        referrer=referrer,
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

    return JsonResponse({
        'total_views': total_views,
        'total_visitors': total_visitors,
        'total_websites': websites.count(),
        'daily_labels': labels,
        'daily_counts': counts,
        'browsers': {
            'labels': [b['browser'] or 'Unknown' for b in browser_data],
            'counts': [b['count'] for b in browser_data],
        }
    })