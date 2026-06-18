/**
 * SmartCable – Component Loader & Interactive Scripts
 * ─────────────────────────────────────────────────────
 * • Loads /components/navbar.html  → #navbar-placeholder
 * • Loads /components/footer.html  → #footer-placeholder
 * • Initialises navbar scroll, hamburger, active-link, scroll animations
 */

(function () {
  'use strict';

  /* ── Component Loader ── */
  async function loadComponent(id, path) {
    var el = document.getElementById(id);
    if (!el) return;
    try {
      var res = await fetch(path);
      if (!res.ok) throw new Error('HTTP ' + res.status);
      el.innerHTML = await res.text();
    } catch (err) {
      console.warn('[SmartCable] Could not load ' + path + ':', err);
    }
  }

  /* ── Bootstrap ── */
  async function init() {
    await Promise.all([
      loadComponent('navbar-placeholder', 'components/navbar.html'),
      loadComponent('footer-placeholder', 'components/footer.html'),
    ]);

    initNavbar();
    initScrollAnimations();
    initSmoothScroll();
    initChannelMarquee();
    initFaqAccordion();
    initFilterTabs();
    initChannelSearch();
    initComparisonToggle();
  }

  /* ══════════════════════════════════════════════
     NAVBAR
     ══════════════════════════════════════════════ */
  function initNavbar() {
    var navbar = document.getElementById('main-navbar');
    var toggle = document.getElementById('navbar-toggle');
    var mobile = document.getElementById('navbar-mobile');

    if (!navbar) return;

    /* ── Determine if we are on a page with a hero (index) ── */
    var hasHero = !!document.querySelector('.hero');

    /* On interior pages (no hero), start navbar solid immediately */
    if (!hasHero) {
      navbar.classList.add('navbar--scrolled');
      navbar.classList.remove('navbar--transparent');
    }

    /* ── Scroll handler ── */
    var ticking = false;
    function onScroll() {
      if (!ticking) {
        requestAnimationFrame(function () {
          if (hasHero) {
            if (window.scrollY > 60) {
              navbar.classList.add('navbar--scrolled');
              navbar.classList.remove('navbar--transparent');
            } else {
              navbar.classList.remove('navbar--scrolled');
              navbar.classList.add('navbar--transparent');
            }
          }
          ticking = false;
        });
        ticking = true;
      }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    /* ── Hamburger toggle handled in js/main.js via event delegation ── */

    /* ── Active link based on current page ── */
    var currentPage = window.location.pathname.split('/').pop() || 'index.html';
    var navLinks = document.querySelectorAll('.navbar__link');
    navLinks.forEach(function (link) {
      link.classList.remove('navbar__link--active');
      var href = link.getAttribute('href') || '';
      if (href === currentPage || (currentPage === '' && href === 'index.html')) {
        link.classList.add('navbar__link--active');
      }
    });

    /* Also for mobile links */
    var mobileLinks = document.querySelectorAll('.navbar__mobile-link');
    mobileLinks.forEach(function (link) {
      var href = link.getAttribute('href') || '';
      if (href === currentPage || (currentPage === '' && href === 'index.html')) {
        link.style.color = 'var(--color-primary)';
      }
    });

    /* ── Scroll-based active (only on index.html with section anchors) ── */
    if (hasHero) {
      var sections = document.querySelectorAll('section[id]');
      function updateActiveLink() {
        var scrollY = window.scrollY + 120;
        sections.forEach(function (section) {
          var top = section.offsetTop;
          var height = section.offsetHeight;
          var id = section.getAttribute('id');
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
  }

  /* ══════════════════════════════════════════════
     SCROLL ANIMATIONS (IntersectionObserver)
     ══════════════════════════════════════════════ */
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

  /* ══════════════════════════════════════════════
     SMOOTH SCROLL (anchor links)
     ══════════════════════════════════════════════ */
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

  /* ══════════════════════════════════════════════
     CHANNEL MARQUEE (duplicate children)
     ══════════════════════════════════════════════ */
  function initChannelMarquee() {
    var marquee = document.querySelector('.channels__marquee');
    if (!marquee) return;
    var children = Array.from(marquee.children);
    children.forEach(function (child) {
      marquee.appendChild(child.cloneNode(true));
    });
  }

  /* ══════════════════════════════════════════════
     FAQ ACCORDION (support.html)
     ══════════════════════════════════════════════ */
  function initFaqAccordion() {
    var items = document.querySelectorAll('.faq__item');
    if (!items.length) return;

    items.forEach(function (item) {
      var header = item.querySelector('.faq__question');
      if (!header) return;
      header.addEventListener('click', function () {
        var isOpen = item.classList.contains('faq__item--open');

        /* close all */
        items.forEach(function (i) {
          i.classList.remove('faq__item--open');
          var ans = i.querySelector('.faq__answer');
          if (ans) ans.style.maxHeight = null;
        });

        /* toggle current */
        if (!isOpen) {
          item.classList.add('faq__item--open');
          var answer = item.querySelector('.faq__answer');
          if (answer) answer.style.maxHeight = answer.scrollHeight + 'px';
        }
      });
    });
  }

  /* ══════════════════════════════════════════════
     FILTER TABS (packages / channels / offers)
     ══════════════════════════════════════════════ */
  function initFilterTabs() {
    var tabGroups = document.querySelectorAll('[data-filter-group]');
    tabGroups.forEach(function (group) {
      var tabs = group.querySelectorAll('[data-filter]');
      var targetId = group.dataset.filterGroup;
      var container = document.getElementById(targetId);
      if (!container) return;

      tabs.forEach(function (tab) {
        tab.addEventListener('click', function () {
          /* Activate tab */
          tabs.forEach(function (t) { t.classList.remove('filter-tab--active'); });
          tab.classList.add('filter-tab--active');

          var filterVal = tab.dataset.filter;
          var items = container.querySelectorAll('[data-category]');
          items.forEach(function (item) {
            if (filterVal === 'all' || item.dataset.category === filterVal) {
              item.style.display = '';
              item.style.animation = 'fadeInUp 0.4s ease both';
            } else {
              item.style.display = 'none';
            }
          });
        });
      });
    });
  }

  /* ══════════════════════════════════════════════
     CHANNEL SEARCH (channels.html)
     ══════════════════════════════════════════════ */
  function initChannelSearch() {
    var searchInput = document.getElementById('channel-search');
    if (!searchInput) return;
    var grid = document.getElementById('channel-grid');
    if (!grid) return;

    searchInput.addEventListener('input', function () {
      var query = searchInput.value.toLowerCase().trim();
      var items = grid.querySelectorAll('[data-channel-name]');
      items.forEach(function (item) {
        var name = (item.dataset.channelName || '').toLowerCase();
        if (!query || name.indexOf(query) !== -1) {
          item.style.display = '';
        } else {
          item.style.display = 'none';
        }
      });
    });
  }

  /* ══════════════════════════════════════════════
     COMPARISON TABLE TOGGLE (packages.html)
     ══════════════════════════════════════════════ */
  function initComparisonToggle() {
    var btn = document.getElementById('toggle-comparison');
    var table = document.getElementById('comparison-section');
    if (!btn || !table) return;
    btn.addEventListener('click', function () {
      var hidden = table.style.display === 'none';
      table.style.display = hidden ? 'block' : 'none';
      btn.textContent = hidden ? 'Hide Comparison' : 'Compare All Plans';
      if (hidden) {
        table.style.animation = 'fadeInUp 0.5s ease both';
        table.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  }

  /* ══════════════════════════════════════════════
     COUNTER ANIMATION (exported global)
     ══════════════════════════════════════════════ */
  window.animateCounter = function (el, target, duration) {
    duration = duration || 2000;
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

  /* ── Fire ── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
