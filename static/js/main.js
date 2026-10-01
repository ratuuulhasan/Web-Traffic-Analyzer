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