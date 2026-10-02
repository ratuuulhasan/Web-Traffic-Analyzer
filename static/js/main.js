// ============ Sidebar Toggle (Mobile) ============
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    const toggleBtn = document.getElementById('sidebarToggle');

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', function() {
            sidebar.classList.toggle('open');
            if (overlay) overlay.classList.toggle('active');
        });
    }

    if (overlay) {
        overlay.addEventListener('click', function() {
            sidebar.classList.remove('open');
            overlay.classList.remove('active');
        });
    }

    // ============ Auto-dismiss alerts ============
    setTimeout(function() {
        document.querySelectorAll('.alert-auto-dismiss').forEach(function(el) {
            el.style.transition = 'opacity 0.5s, transform 0.5s';
            el.style.opacity = '0';
            el.style.transform = 'translateY(-10px)';
            setTimeout(() => el.remove(), 500);
        });
    }, 4000);
});

// ============ Dark Mode ============
(function() {
    const html = document.documentElement;
    const toggleBtn = document.getElementById('themeToggle');
    const iconEl = document.getElementById('themeIcon');

    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    html.setAttribute('data-theme', savedTheme);
    if (iconEl) iconEl.textContent = savedTheme === 'dark' ? '☀️' : '🌙';

    if (toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            const current = html.getAttribute('data-theme') || 'light';
            const next = current === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
            if (iconEl) iconEl.textContent = next === 'dark' ? '☀️' : '🌙';
            
            // Charts update করতে reload
            if (document.querySelector('canvas')) {
                setTimeout(() => location.reload(), 200);
            }
        });
    }
})();

// ============ Number Counter Animation ============
window.animateNumber = function(element, target, duration = 1200) {
    if (!element) return;

    // Remove non-numeric characters to get pure number
    const targetNum = parseInt(String(target).replace(/[^0-9]/g, '')) || 0;
    const suffix = String(target).replace(/[0-9]/g, '').trim();

    const start = 0;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // Ease out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = Math.floor(start + (targetNum - start) * eased);

        element.textContent = current.toLocaleString() + suffix;

        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            element.textContent = targetNum.toLocaleString() + suffix;
        }
    }

    requestAnimationFrame(update);
};

