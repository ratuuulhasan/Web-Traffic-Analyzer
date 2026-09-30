from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from datetime import timedelta
from .models import Website, EmailReportSetting
from analytics.models import PageView, Visitor


def calculate_report_stats(website, since):
    """Calculate stats for a website since given datetime."""
    pageviews = PageView.objects.filter(website=website, timestamp__gte=since)
    visitors = Visitor.objects.filter(website=website)

    total_views = pageviews.count()
    unique_visitors = visitors.filter(last_visit__gte=since).count()
    new_visitors = visitors.filter(first_visit__gte=since).count()

    # Bounce rate
    single_page_visitors = (
        visitors
        .annotate(view_count=Count('pageviews'))
        .filter(view_count=1, last_visit__gte=since)
        .count()
    )
    bounce_rate = (
        round((single_page_visitors / unique_visitors) * 100, 1)
        if unique_visitors > 0 else 0
    )

    # Top pages
    top_pages = list(
        pageviews
        .values('url')
        .annotate(views=Count('id'))
        .order_by('-views')[:5]
    )

    # Top countries
    countries = list(
        visitors
        .filter(last_visit__gte=since)
        .exclude(country='')
        .values('country')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

    return {
        'page_views': total_views,
        'unique_visitors': unique_visitors,
        'new_visitors': new_visitors,
        'bounce_rate': bounce_rate,
    }, top_pages, countries


def send_report_email(setting, frequency):
    """Send report email for a given setting."""
    website = setting.website
    user = website.owner

    if not user.email:
        return False, f"No email for user {user.username}"

    # Date range
    now = timezone.now()
    if frequency == 'daily':
        since = now - timedelta(days=1)
        template = 'emails/daily_report.html'
        subject = f"📊 Daily Report: {website.name} — {now.strftime('%d %b %Y')}"
        date_range = now.strftime('%d %b %Y')
    elif frequency == 'weekly':
        since = now - timedelta(days=7)
        template = 'emails/weekly_report.html'
        subject = f"📊 Weekly Report: {website.name}"
        date_range = f"{(now - timedelta(days=7)).strftime('%d %b')} - {now.strftime('%d %b %Y')}"
    elif frequency == 'monthly':
        since = now - timedelta(days=30)
        template = 'emails/weekly_report.html'
        subject = f"📊 Monthly Report: {website.name}"
        date_range = f"{(now - timedelta(days=30)).strftime('%d %b')} - {now.strftime('%d %b %Y')}"
    else:
        return False, "Invalid frequency"

    # Calculate stats
    stats, top_pages, countries = calculate_report_stats(website, since)

    # Render email
    context = {
        'website': website,
        'stats': stats,
        'top_pages': top_pages,
        'countries': countries,
        'date': now,
        'date_range': date_range,
        'dashboard_url': f"{settings.SITE_URL}/websites/{website.id}/",
        'detail_url': f"{settings.SITE_URL}/websites/{website.id}/",
    }

    html_content = render_to_string(template, context)
    text_content = f"""
Traffic Report for {website.name}

Page Views: {stats['page_views']}
Unique Visitors: {stats['unique_visitors']}
New Visitors: {stats['new_visitors']}
Bounce Rate: {stats['bounce_rate']}%

View full dashboard: {settings.SITE_URL}/websites/{website.id}/
"""

    # Send
    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)

        setting.last_sent = now
        setting.save(update_fields=['last_sent'])
        return True, f"Sent to {user.email}"
    except Exception as e:
        return False, str(e)


@shared_task
def check_and_send_reports():
    """Main task: runs every hour, sends reports if due."""
    now = timezone.now()
    current_hour = now.hour
    current_weekday = now.weekday()  # 0 = Monday

    sent_count = 0
    failed_count = 0

    settings_qs = EmailReportSetting.objects.filter(
        is_enabled=True,
        send_hour=current_hour,
    ).select_related('website', 'website__owner')

    for setting in settings_qs:
        # For daily: check if already sent today
        if setting.frequency == 'daily':
            if setting.last_sent and setting.last_sent.date() == now.date():
                continue

        # For weekly: only send on Monday
        elif setting.frequency == 'weekly':
            if current_weekday != 0:  # 0 = Monday
                continue
            if setting.last_sent and (now - setting.last_sent).days < 6:
                continue

        # For monthly: only send on 1st of month
        elif setting.frequency == 'monthly':
            if now.day != 1:
                continue
            if setting.last_sent and (now - setting.last_sent).days < 28:
                continue

        success, message = send_report_email(setting, setting.frequency)
        if success:
            sent_count += 1
        else:
            failed_count += 1
            print(f"Failed to send report for {setting.website.name}: {message}")

    return f"Sent {sent_count} reports, {failed_count} failed"


@shared_task
def send_test_report(website_id):
    """Send a test report immediately."""
    try:
        website = Website.objects.get(id=website_id)
        setting, _ = EmailReportSetting.objects.get_or_create(website=website)
        success, message = send_report_email(setting, 'daily')
        return {'success': success, 'message': message}
    except Website.DoesNotExist:
        return {'success': False, 'message': 'Website not found'}