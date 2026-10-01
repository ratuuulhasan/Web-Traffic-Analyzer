from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import Website, APIKey
from .forms import WebsiteForm
from analytics.models import PageView, Visitor
import csv
from django.http import StreamingHttpResponse
from .models import EmailReportSetting
from .tasks import send_test_report


@login_required
def website_list(request):
    """List all websites of logged in user."""
    websites = Website.objects.filter(owner=request.user).annotate(
        total_views=Count('pageviews')
    ).order_by('-created_at')

    return render(request, 'websites/website_list.html', {
        'websites': websites
    })

@login_required
def website_add(request):
    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        if form.is_valid():
            website = form.save(commit=False)
            website.owner = request.user
            website.save()

            #Auto-create API key
            APIKey.objects.create(website=website)

            messages.success(request, f"Website '{website.name}' added successfully!")
            return redirect('websites:detail', pk=website.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = WebsiteForm()

    return render(request, 'websites/website_form.html', {
        'form': form,
        'title': 'Add New Website'
    })


@login_required
def website_detail(request, pk):
    """Detailed analytics page for a website."""
    website = get_object_or_404(Website, pk=pk, owner=request.user)

    # ---------- Basic Stats ----------
    pageviews = PageView.objects.filter(website=website)
    visitors = Visitor.objects.filter(website=website)

    total_views = pageviews.count()
    unique_visitors = visitors.count()

    # ---------- Today's Stats ----------
    today = timezone.now().date()
    today_views = pageviews.filter(timestamp__date=today).count()
    today_visitors = visitors.filter(last_visit__date=today).count()

    # ---------- Last 7 Days Stats ----------
    seven_days_ago = timezone.now() - timedelta(days=7)
    week_views = pageviews.filter(timestamp__gte=seven_days_ago).count()
    week_visitors = visitors.filter(last_visit__gte=seven_days_ago).count()

    # ---------- Bounce Rate ----------
    single_page_visitors = (
        visitors
        .annotate(view_count=Count('pageviews'))
        .filter(view_count=1)
        .count()
    )
    bounce_rate = (
        round((single_page_visitors / unique_visitors) * 100, 1)
        if unique_visitors > 0 else 0
    )

    # ---------- Top Pages ----------
    top_pages = (
        pageviews
        .values('url')
        .annotate(views=Count('id'))
        .order_by('-views')[:10]
    )

    # ---------- Top Referrers ----------
    top_referrers = (
        pageviews
        .exclude(referrer='')
        .exclude(referrer__isnull=True)
        .values('referrer')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )

    # ---------- Recent Visitors ----------
    recent_visitors = visitors.order_by('-last_visit')[:20]

    tracking_url = request.build_absolute_uri('/static/tracking.js')
    api_key, _ = APIKey.objects.get_or_create(website=website)

    context = {
        'website': website,
        'total_views': total_views,
        'unique_visitors': unique_visitors,
        'today_views': today_views,
        'today_visitors': today_visitors,
        'week_views': week_views,
        'week_visitors': week_visitors,
        'bounce_rate': bounce_rate,
        'top_pages': top_pages,
        'top_referrers': top_referrers,
        'recent_visitors': recent_visitors,
        'tracking_url': tracking_url,
        'api_key': api_key,
    }

    return render(request, 'websites/website_detail.html', context)


@login_required
def website_edit(request, pk):
    """Edit website info."""
    website = get_object_or_404(Website, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = WebsiteForm(request.POST, instance=website)
        if form.is_valid():
            form.save()
            messages.success(request, "Website updated successfully!")
            return redirect('websites:detail', pk=website.pk)
    else:
        form = WebsiteForm(instance=website)

    return render(request, 'websites/website_form.html', {
        'form': form,
        'title': 'Edit Website',
        'website': website
    })


@login_required
def website_delete(request, pk):
    """Delete website with confirmation."""
    website = get_object_or_404(Website, pk=pk, owner=request.user)

    if request.method == 'POST':
        name = website.name
        website.delete()
        messages.success(request, f"Website '{name}' deleted.")
        return redirect('websites:list')

    return render(request, 'websites/website_confirm_delete.html', {
        'website': website
    })

# ============ CSV Export Helpers ============
class Echo:
    """An object that implements just the write method of the file-like interface."""
    def write(self, value):
        return value


@login_required
def export_pageviews_csv(request, pk):
    """Export PageViews as CSV."""
    website = get_object_or_404(Website, pk=pk, owner=request.user)

    # Date range
    days = int(request.query_params.get('days', 30)) if hasattr(request, 'query_params') else int(request.GET.get('days', 30))
    days = min(max(days, 1), 365)
    since = timezone.now() - timedelta(days=days)

    qs = (
        PageView.objects
        .filter(website=website, timestamp__gte=since)
        .select_related('visitor')
        .order_by('-timestamp')
    )

    def rows():
        # Header
        yield ['Timestamp', 'URL', 'Page Title', 'Referrer',
               'Visitor ID', 'Country', 'Browser', 'OS', 'Device']
        for pv in qs.iterator(chunk_size=500):
            v = pv.visitor
            yield [
                pv.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                pv.url or '',
                pv.page_title or '',
                pv.referrer or '',
                v.visitor_id if v else '',
                v.country if v else '',
                v.browser if v else '',
                v.os if v else '',
                v.device if v else '',
            ]

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)

    def stream():
        for row in rows():
            yield writer.writerow(row)

    filename = f"{website.name.replace(' ', '_')}_pageviews_{days}d.csv"
    response = StreamingHttpResponse(
        stream(),
        content_type='text/csv',
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@login_required
def export_visitors_csv(request, pk):
    """Export Visitors as CSV."""
    website = get_object_or_404(Website, pk=pk, owner=request.user)

    days = int(request.GET.get('days', 30))
    days = min(max(days, 1), 365)
    since = timezone.now() - timedelta(days=days)

    qs = (
        Visitor.objects
        .filter(website=website, last_visit__gte=since)
        .order_by('-last_visit')
    )

    def rows():
        yield ['Visitor ID', 'IP Address', 'Country', 'City',
               'Browser', 'OS', 'Device', 'First Visit', 'Last Visit']
        for v in qs.iterator(chunk_size=500):
            yield [
                v.visitor_id,
                v.ip_address or '',
                v.country or '',
                v.city or '',
                v.browser or '',
                v.os or '',
                v.device or '',
                v.first_visit.strftime('%Y-%m-%d %H:%M:%S'),
                v.last_visit.strftime('%Y-%m-%d %H:%M:%S'),
            ]

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)

    def stream():
        for row in rows():
            yield writer.writerow(row)

    filename = f"{website.name.replace(' ', '_')}_visitors_{days}d.csv"
    response = StreamingHttpResponse(stream(), content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@login_required
def export_stats_csv(request, pk):
    """Export aggregated daily stats as CSV."""
    website = get_object_or_404(Website, pk=pk, owner=request.user)

    days = int(request.GET.get('days', 30))
    days = min(max(days, 1), 365)

    from django.db.models.functions import TruncDate

    today = timezone.now().date()
    start_date = today - timedelta(days=days - 1)

    # Views per day
    views = (
        PageView.objects
        .filter(website=website, timestamp__date__gte=start_date)
        .annotate(day=TruncDate('timestamp'))
        .values('day')
        .annotate(count=Count('id'))
    )
    views_map = {item['day']: item['count'] for item in views}

    # New visitors per day (first_visit on that day)
    new_visitors = (
        Visitor.objects
        .filter(website=website, first_visit__date__gte=start_date)
        .annotate(day=TruncDate('first_visit'))
        .values('day')
        .annotate(count=Count('id'))
    )
    new_visitors_map = {item['day']: item['count'] for item in new_visitors}

    # Active visitors per day (last_visit on that day)
    active_visitors = (
        Visitor.objects
        .filter(website=website, last_visit__date__gte=start_date)
        .annotate(day=TruncDate('last_visit'))
        .values('day')
        .annotate(count=Count('id'))
    )
    active_visitors_map = {item['day']: item['count'] for item in active_visitors}

    def rows():
        yield ['Date', 'Page Views', 'New Visitors', 'Active Visitors']
        for i in range(days):
            day = start_date + timedelta(days=i)
            yield [
                day.isoformat(),
                views_map.get(day, 0),
                new_visitors_map.get(day, 0),
                active_visitors_map.get(day, 0),
            ]

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)

    def stream():
        for row in rows():
            yield writer.writerow(row)

    filename = f"{website.name.replace(' ', '_')}_stats_{days}d.csv"
    response = StreamingHttpResponse(stream(), content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@login_required
def email_settings(request, pk):
    website = get_object_or_404(Website, pk=pk, owner=request.user)
    setting, _ = EmailReportSetting.objects.get_or_create(website=website)

    if request.method == 'POST':
        setting.is_enabled = request.POST.get('is_enabled') == 'on'
        setting.frequency = request.POST.get('frequency', 'daily')
        setting.send_hour = int(request.POST.get('send_hour', 9))
        setting.save()
        messages.success(request, "Email report settings saved!")
        return redirect('websites:email-settings', pk=website.pk)

    return render(request, 'websites/email_settings.html', {
        'website': website,
        'setting': setting,
        'hours': list(range(24)),  # 0-23
    })


@login_required
def send_test_email(request, pk):
    website = get_object_or_404(Website, pk=pk, owner=request.user)
    result = send_test_report(website.id)

    if result['success']:
        messages.success(request, f"Test email sent! {result['message']}")
    else:
        messages.error(request, f"Failed: {result['message']}")

    return redirect('websites:email-settings', pk=website.pk)

@login_required
def website_events(request, pk):
    website = get_object_or_404(Website, pk=pk, owner=request.user)

    total_events = website.events.count()
    unique_event_types = website.events.values('name').distinct().count()

    # Top event names
    top_events = list(
        website.events.values('name')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )

    return render(request, 'websites/website_events.html', {
        'website': website,
        'total_events': total_events,
        'unique_event_types': unique_event_types,
        'top_events': top_events,
    })