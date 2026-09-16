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
    initRechargeBar();
    initProductBuyButtons();
    initImageFallbacks();
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

    /* ── Scroll-based active (only on SPA with section anchors) ── */
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
      updateActiveLink();
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
      var target = null;
      try {
        target = document.querySelector(id);
      } catch (err) {
        target = null;
      }
      if (target) {
        e.preventDefault();
        var offset = 80;
        var y = target.getBoundingClientRect().top + window.pageYOffset - offset;
        window.scrollTo({ top: y, behavior: 'smooth' });
      } else {
        var page = window.location.pathname.split('/').pop() || 'index.html';
        if (page !== 'index.html' && page !== '') {
          e.preventDefault();
          window.location.href = 'index.html' + id;
        }
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
     FILTER TABS (products / packages / channels / offers)
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
          var delay = 0;
          items.forEach(function (item) {
            if (filterVal === 'all' || item.dataset.category === filterVal) {
              item.style.display = '';
              item.style.animation = 'none';
              /* stagger the fade-in */
              (function (el, d) {
                setTimeout(function () {
                  el.style.animation = 'fadeInUp 0.4s ease both';
                }, d);
              })(item, delay);
              delay += 30;
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
     RECHARGE BAR LOGIC (legacy – graceful no-op)
     ══════════════════════════════════════════════ */
  function initRechargeBar() {
    var inputEl = document.getElementById('recharge-input');
    var btnEl = document.getElementById('recharge-btn');
    if (!inputEl || !btnEl) return;

    function handleProceed() {
      var val = inputEl.value.trim();
      if (!val) { inputEl.focus(); return; }
      window.location.href = 'subscribe.html?recharge_val=' + encodeURIComponent(val);
    }

    btnEl.addEventListener('click', handleProceed);
    inputEl.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { handleProceed(); }
    });
  }

  /* ══════════════════════════════════════════════
     PRODUCT BUY BUTTONS (Buy Now -> Contact Form Pre-fill)
     ══════════════════════════════════════════════ */
  function initProductBuyButtons() {
    var grid = document.getElementById('products-grid');
    if (!grid) return;
    grid.addEventListener('click', function (e) {
      var btn = e.target.closest('.product-card__btn');
      if (!btn) return;
      e.preventDefault();
      var card = btn.closest('.product-card');
      var name = card ? (card.querySelector('.product-card__name') || {}).textContent || 'Product' : 'Product';
      var price = card ? (card.querySelector('.product-card__price') || {}).textContent || '' : '';
      name = name.trim();
      price = price.trim();

      /* Flash button state */
      var orig = btn.textContent;
      btn.textContent = '\u2713 Selected!';
      btn.style.background = 'linear-gradient(135deg, #10b981, #34d399)';
      btn.style.boxShadow = '0 0 16px rgba(16, 185, 129, 0.6)';
      setTimeout(function () {
        btn.textContent = orig;
        btn.style.background = '';
        btn.style.boxShadow = '';
      }, 2000);

      /* Pre-fill Contact Form */
      var subjectInput = document.getElementById('contact-subject');
      var messageInput = document.getElementById('contact-message');
      var nameInput = document.getElementById('contact-name');

      if (subjectInput) {
        subjectInput.value = 'Interested in purchasing: ' + name;
      }
      if (messageInput) {
        messageInput.value = 'Hi, I am interested in purchasing the ' + name + (price ? ' (' + price + ')' : '') + '. Please provide ordering and delivery details.';
      }

      /* Smooth scroll to contact section */
      var contactSection = document.getElementById('contact');
      if (contactSection) {
        var offset = 70;
        var y = contactSection.getBoundingClientRect().top + window.pageYOffset - offset;
        window.scrollTo({ top: y, behavior: 'smooth' });
        setTimeout(function () {
          if (nameInput && !nameInput.value) {
            nameInput.focus();
          } else if (messageInput) {
            messageInput.focus();
          }
        }, 800);
      }
    });
  }

  /* ══════════════════════════════════════════════
     IMAGE FALLBACKS (Gracefully handle offline / broken CDN links)
     ══════════════════════════════════════════════ */
  function initImageFallbacks() {
    var imgs = document.querySelectorAll('.product-card__img');
    imgs.forEach(function (img) {
      img.addEventListener('error', function () {
        var card = img.closest('.product-card');
        var name = card ? (card.querySelector('.product-card__name') || {}).textContent || 'Product' : 'Product';
        name = name.trim();
        var svg = '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300">' +
          '<rect width="400" height="300" fill="#0d111a"/>' +
          '<circle cx="200" cy="130" r="45" fill="none" stroke="#00f2fe" stroke-width="2" opacity="0.4"/>' +
          '<path d="M185 130h30M200 115v30" stroke="#00f2fe" stroke-width="2" stroke-linecap="round"/>' +
          '<text x="200" y="210" font-family="sans-serif" font-size="14" font-weight="bold" fill="#00f2fe" text-anchor="middle">' +
          name.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;') +
          '</text>' +
          '<text x="200" y="235" font-family="sans-serif" font-size="11" fill="#707d93" text-anchor="middle">SMART CABLE SERVICES</text>' +
          '</svg>';
        img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
        img.classList.add('product-card__img--fallback');
      });
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
