(function() {
    // ============ Visitor ID ============
    function getVisitorId() {
        var name = 'ta_visitor_id=';
        var decoded = decodeURIComponent(document.cookie);
        var parts = decoded.split(';');
        for (var i = 0; i < parts.length; i++) {
            var c = parts[i].trim();
            if (c.indexOf(name) === 0) return c.substring(name.length);
        }
        var id = 'v_' + Math.random().toString(36).substr(2, 12) + '_' + Date.now();
        document.cookie = name + id + ';max-age=' + (60*60*24*365) + ';path=/';
        return id;
    }

    // ============ Get tracking ID ============
    var scriptTag = document.currentScript || (function() {
        var scripts = document.getElementsByTagName('script');
        return scripts[scripts.length - 1];
    })();
    var trackingId = scriptTag.getAttribute('data-tracking-id');
    if (!trackingId) {
        console.warn('[TrafficAnalyzer] tracking-id missing');
        return;
    }

    var API_BASE = scriptTag.getAttribute('data-api-url') || 
                   new URL(scriptTag.src).origin;
    var visitorId = getVisitorId();

    // ============ Page View Track ============
    function trackPageView() {
        var payload = {
            tracking_id: trackingId,
            visitor_id: visitorId,
            url: window.location.href,
            title: document.title,
            referrer: document.referrer
        };

        fetch(API_BASE + '/api/track/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload),
            keepalive: true
        }).catch(function() {});
    }

    // ============ Custom Event Track ============
    function trackEvent(name, properties) {
        if (!name) {
            console.warn('[TrafficAnalyzer] event name required');
            return;
        }
        properties = properties || {};

        var payload = {
            tracking_id: trackingId,
            visitor_id: visitorId,
            event_name: name,
            properties: properties,
            url: window.location.href
        };

        fetch(API_BASE + '/api/track/event/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload),
            keepalive: true
        }).catch(function() {});
    }

    // ============ Auto-tracking ============

    // 1. Auto-track outbound link clicks
    function setupAutoTracking() {
        document.addEventListener('click', function(e) {
            var target = e.target.closest('a, button');
            if (!target) return;

            var tag = target.tagName.toLowerCase();
            var text = (target.innerText || target.textContent || '').trim().slice(0, 50);

            // Outbound links
            if (tag === 'a' && target.href) {
                var linkHost = '';
                try { linkHost = new URL(target.href).hostname; } catch(err) {}
                if (linkHost && linkHost !== window.location.hostname) {
                    trackEvent('outbound_click', {
                        url: target.href,
                        text: text
                    });
                }
            }

            // Button clicks (only if data-ta-event attribute present)
            if (target.hasAttribute('data-ta-event')) {
                trackEvent(target.getAttribute('data-ta-event'), {
                    text: text,
                    tag: tag
                });
            }
        }, true);

        // 2. Auto-track form submissions
        document.addEventListener('submit', function(e) {
            var form = e.target;
            if (form.tagName !== 'FORM') return;
            trackEvent('form_submit', {
                form_id: form.id || '',
                form_action: form.action || '',
                form_name: form.getAttribute('name') || ''
            });
        }, true);
    }

    // ============ Expose global function ============
    window.trackEvent = trackEvent;
    window.taTrackEvent = trackEvent;  // alternate name

    // ============ Initialize ============
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            trackPageView();
            setupAutoTracking();
        });
    } else {
        trackPageView();
        setupAutoTracking();
    }
})();