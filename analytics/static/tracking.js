(function() {
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

    var trackingId = document.currentScript.getAttribute('data-tracking-id');
    if (!trackingId) return;

    var payload = {
        tracking_id: trackingId,
        visitor_id: getVisitorId(),
        url: window.location.href,
        title: document.title,
        referrer: document.referrer
    };

    fetch('http://127.0.0.1:8000/api/track/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        keepalive: true
    }).catch(function() {});
})();