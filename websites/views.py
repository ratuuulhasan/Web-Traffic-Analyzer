from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import Website
from .forms import WebsiteForm
from analytics.models import PageView, Visitor


@login_required
def website_list(request):
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
    website = get_object_or_404(Website, pk=pk, owner=request.user)

    # Basic stats
    total_views = PageView.objects.filter(website=website).count()
    unique_visitors = Visitor.objects.filter(website=website).count()

    # Tracking script URL
    tracking_url = request.build_absolute_uri('/static/tracking.js')

    return render(request, 'websites/website_detail.html', {
        'website': website,
        'total_views': total_views,
        'unique_visitors': unique_visitors,
        'tracking_url': tracking_url,
    })


@login_required
def website_edit(request, pk):
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
    website = get_object_or_404(Website, pk=pk, owner=request.user)

    if request.method == 'POST':
        name = website.name
        website.delete()
        messages.success(request, f"Website '{name}' deleted.")
        return redirect('websites:list')

    return render(request, 'websites/website_confirm_delete.html', {
        'website': website
    })