import json
from django.core.cache import cache
from django.utils import timezone


REALTIME_WINDOW = 300  # 5 minutes


def _key_prefix(website_id):
    return f'realtime:website:{website_id}'


def mark_visitor_active(website_id, visitor_id, data):
    """
    Mark a visitor as active in realtime.
    Data structure: {visitor_id: {...visitor data...}}
    """
    key = _key_prefix(website_id)

    # Get existing dict or empty
    active = cache.get(key, {}) or {}

    data['last_seen'] = timezone.now().isoformat()
    active[visitor_id] = data

    # Save with TTL
    cache.set(key, active, timeout=REALTIME_WINDOW)
    return True


def get_active_visitors(website_id):
    """Get all active visitors for a website."""
    key = _key_prefix(website_id)
    active = cache.get(key, {}) or {}

    # Filter out stale (older than REALTIME_WINDOW)
    now = timezone.now()
    fresh = {}
    for vid, data in active.items():
        last_seen_str = data.get('last_seen')
        if not last_seen_str:
            continue
        try:
            last_seen = timezone.datetime.fromisoformat(last_seen_str)
            if last_seen.tzinfo is None:
                last_seen = timezone.make_aware(last_seen)
            if (now - last_seen).total_seconds() < REALTIME_WINDOW:
                fresh[vid] = data
        except (ValueError, TypeError):
            continue

    # Update cache with fresh data
    if fresh:
        cache.set(key, fresh, timeout=REALTIME_WINDOW)
    else:
        cache.delete(key)

    return fresh


def get_active_count(website_id):
    """Get count of active visitors."""
    return len(get_active_visitors(website_id))


def get_all_active_summary(websites):
    """Get combined active visitors for multiple websites."""
    all_visitors = []
    total = 0

    for website in websites:
        active = get_active_visitors(website.id)
        total += len(active)
        for vid, data in active.items():
            data['visitor_id'] = vid
            data['website_name'] = website.name
            data['website_id'] = website.id
            all_visitors.append(data)

    # Sort by last_seen descending
    all_visitors.sort(key=lambda x: x.get('last_seen', ''), reverse=True)
    return {
        'total': total,
        'visitors': all_visitors,
    }