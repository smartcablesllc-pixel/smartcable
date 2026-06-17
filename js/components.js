/**
 * SmartCable – Component Loader & Interactive Scripts
 * Loads navbar.html and footer.html into placeholders
 */

(function () {
  'use strict';

  /* ── Component Loader ── */
  async function loadComponent(id, path) {
    const el = document.getElementById(id);
    if (!el) return;
    try {
      const res = await fetch(path);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      el.innerHTML = await res.text();
    } catch (err) {
      console.warn(`[SmartCable] Could not load ${path}:`, err);
    }
  }

  async function init() {
    await Promise.all([
      loadComponent('navbar-placeholder', 'components/navbar.html'),
      loadComponent('footer-placeholder', 'components/footer.html'),
    ]);

    initNavbar();
    initScrollAnimations();
    initSmoothScroll();
    initChannelMarquee();
  }

  /* ── Navbar Logic ── */
  function initNavbar() {
    const navbar = document.getElementById('main-navbar');
    const toggle = document.getElementById('navbar-toggle');
    const mobile = document.getElementById('navbar-mobile');

    if (!navbar) return;

    // Scroll handler – add solid background on scroll
    let ticking = false;
    function onScroll() {
      if (!ticking) {
        requestAnimationFrame(function () {
          if (window.scrollY > 60) {
            navbar.classList.add('navbar--scrolled');
            navbar.classList.remove('navbar--transparent');
          } else {
            navbar.classList.remove('navbar--scrolled');
            navbar.classList.add('navbar--transparent');
          }
          ticking = false;
        });
        ticking = true;
      }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll(); // fire on load

    // Hamburger toggle
    if (toggle && mobile) {
      toggle.addEventListener('click', function () {
        const isOpen = mobile.classList.toggle('open');
        toggle.classList.toggle('active', isOpen);
        toggle.setAttribute('aria-expanded', String(isOpen));
        document.body.style.overflow = isOpen ? 'hidden' : '';
      });

      // Close mobile nav when a link is clicked
      mobile.querySelectorAll('.navbar__mobile-link').forEach(function (link) {
        link.addEventListener('click', function () {
          mobile.classList.remove('open');
          toggle.classList.remove('active');
          toggle.setAttribute('aria-expanded', 'false');
          document.body.style.overflow = '';
        });
      });
    }

    // Active link highlighting based on scroll position
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.navbar__link');
    function updateActiveLink() {
      const scrollY = window.scrollY + 120;
      sections.forEach(function (section) {
        const top = section.offsetTop;
        const height = section.offsetHeight;
        const id = section.getAttribute('id');
        if (scrollY >= top && scrollY < top + height) {
          navLinks.forEach(function (link) {
            link.classList.remove('navbar__link--active');
            if (link.getAttribute('href') === '#' + id) {
              link.classList.add('navbar__link--active');
            }
          });
        }
      });
    }
    window.addEventListener('scroll', updateActiveLink, { passive: true });
  }

  /* ── Scroll Animations ── */
  function initScrollAnimations() {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
    );

    document.querySelectorAll('.animate-on-scroll').forEach(function (el) {
      observer.observe(el);
    });
  }

  /* ── Smooth Scroll for Anchor Links ── */
  function initSmoothScroll() {
    document.addEventListener('click', function (e) {
      var link = e.target.closest('a[href^="#"]');
      if (!link) return;
      var id = link.getAttribute('href');
      if (id.length < 2) return;
      var target = document.querySelector(id);
      if (target) {
        e.preventDefault();
        var offset = 80;
        var y = target.getBoundingClientRect().top + window.pageYOffset - offset;
        window.scrollTo({ top: y, behavior: 'smooth' });
      }
    });
  }

  /* ── Channel Marquee Duplication ── */
  function initChannelMarquee() {
    var marquee = document.querySelector('.channels__marquee');
    if (!marquee) return;
    // Duplicate children for seamless loop
    var children = Array.from(marquee.children);
    children.forEach(function (child) {
      var clone = child.cloneNode(true);
      marquee.appendChild(clone);
    });
  }

  /* ── Counter Animation ── */
  window.animateCounter = function (el, target, duration) {
    duration = duration || 2000;
    var start = 0;
    var startTime = null;
    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      var value = Math.floor(progress * target);
      el.textContent = value + (el.dataset.suffix || '');
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = target + (el.dataset.suffix || '');
      }
    }
    requestAnimationFrame(step);
  };

  // Fire
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
