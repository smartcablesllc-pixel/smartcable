/**
 * SmartCable – Dynamic Mobile Menu Logic
 * ─────────────────────────────────────────────────────
 * Uses Event Delegation attached to the document to handle
 * the mobile hamburger menu toggle, accommodating dynamic navbar loading.
 */

(function () {
  'use strict';

  // Listen for click events on the entire document
  document.addEventListener('click', function (event) {
    // 1. Hamburger toggle click handling
    var toggleButton = event.target.closest('#navbar-toggle');
    if (toggleButton) {
      var mobileMenu = document.getElementById('navbar-mobile');
      if (mobileMenu) {
        var isOpen = mobileMenu.classList.toggle('open');
        toggleButton.classList.toggle('active', isOpen);
        toggleButton.setAttribute('aria-expanded', String(isOpen));

        // Add active class on the main navigation menu container too if needed
        mobileMenu.classList.toggle('active', isOpen);

        document.body.style.overflow = isOpen ? 'hidden' : '';
      }
      return;
    }

    // 2. Close menu when a mobile nav link is clicked
    var mobileLink = event.target.closest('.navbar__mobile-link');
    if (mobileLink) {
      var mobileMenu = document.getElementById('navbar-mobile');
      var toggleButton = document.getElementById('navbar-toggle');
      if (mobileMenu && toggleButton) {
        mobileMenu.classList.remove('open');
        mobileMenu.classList.remove('active');
        toggleButton.classList.remove('active');
        toggleButton.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      }
    }
  });
})();
