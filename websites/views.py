from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import Website, APIKey
from .forms import WebsiteForm
from analytics.models import PageView, Visitor


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