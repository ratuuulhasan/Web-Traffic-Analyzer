import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from user_agents import parse
from websites.models import Website
from .models import Visitor, PageView


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