/* ============================================
   EduVerse LMS — JavaScript
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {

    // ---- Mobile Navigation Toggle ----
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function () {
            navMenu.classList.toggle('active');
            // Animate hamburger
            const spans = navToggle.querySelectorAll('span');
            if (navMenu.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
            } else {
                spans[0].style.transform = '';
                spans[1].style.opacity = '';
                spans[2].style.transform = '';
            }
        });
    }

    // ---- User Dropdown ----
    const dropdownToggle = document.getElementById('user-dropdown-toggle');
    const dropdown = dropdownToggle ? dropdownToggle.closest('.nav-dropdown') : null;

    if (dropdownToggle && dropdown) {
        dropdownToggle.addEventListener('click', function (e) {
            e.preventDefault();
            dropdown.classList.toggle('active');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function (e) {
            if (!dropdown.contains(e.target)) {
                dropdown.classList.remove('active');
            }
        });
    }

    // ---- Navbar Scroll Effect ----
    const navbar = document.getElementById('main-navbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // ---- Auto-dismiss Alerts ----
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert, index) {
        setTimeout(function () {
            alert.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(100px)';
            setTimeout(function () {
                alert.remove();
            }, 300);
        }, 4000 + (index * 500));
    });

    // ---- Scroll Animations (Intersection Observer) ----
    const animatedElements = document.querySelectorAll('.fade-in-up');
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.style.animationPlayState = 'running';
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        animatedElements.forEach(function (el) {
            el.style.animationPlayState = 'paused';
            observer.observe(el);
        });
    }

    // ---- Module Toggle (Course Detail Page) ----
    // Open all modules by default
    const moduleCards = document.querySelectorAll('.module-card');
    moduleCards.forEach(function (card) {
        card.classList.add('module-open');
    });

});
