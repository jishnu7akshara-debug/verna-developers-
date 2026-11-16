/* Verna Developers site behaviour. No dependencies. Everything here is progressive:
   with JavaScript off the page is complete, static and readable. */
(function () {
  'use strict';

  var root = document.documentElement;
  root.classList.remove('no-js');
  root.classList.add('js');

  // ==================== Site Preloader Logic (Immediate & Bulletproof) ====================
  var preloader = document.getElementById('site-preloader');
  if (preloader) {
    var preloaderDismissed = false;
    function dismissPreloader() {
      if (preloaderDismissed) return;
      preloaderDismissed = true;
      preloader.classList.add('loaded');
      setTimeout(function () {
        if (preloader && preloader.parentNode) {
          preloader.parentNode.removeChild(preloader);
        }
      }, 500);
    }

    if (document.readyState === 'complete' || document.readyState === 'interactive') {
      setTimeout(dismissPreloader, 350);
    } else {
      window.addEventListener('DOMContentLoaded', function () { setTimeout(dismissPreloader, 350); });
      window.addEventListener('load', function () { setTimeout(dismissPreloader, 100); });
    }
    // Absolute fallback dismiss
    setTimeout(dismissPreloader, 1500);
  }

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };
  var clamp = function (n, lo, hi) { return Math.min(hi, Math.max(lo, n)); };

  /* ---------- Header: hairline once scrolled, hide on scroll down, show on scroll up ---------- */
  var header = $('[data-header]');
  var mobileBar = $('[data-mobile-bar]');
  var hero = $('.hero');
  var contact = $('#contact');
  var lastY = window.scrollY;
  var ticking = false;
  var processSteps = $('[data-process]');
  var inset = $('[data-drift]');

  function onFrame() {
    ticking = false;
    var y = window.scrollY;
    if (header) {
      header.classList.toggle('is-scrolled', y > 8);
      var goingDown = y > lastY + 4;
      var goingUp = y < lastY - 4;
      if (root.classList.contains('nav-open') || y < 320) header.classList.remove('is-hidden');
      else if (goingDown) header.classList.add('is-hidden');
      else if (goingUp) header.classList.remove('is-hidden');
    }
    if (mobileBar) {
      var pastHero = hero ? y > hero.offsetHeight * 0.7 : y > 500;
      var atContact = contact ? contact.getBoundingClientRect().top < window.innerHeight * 0.6 : false;
      mobileBar.classList.toggle('is-visible', pastHero && !atContact);
    }
    if (processSteps && !reduceMotion) {
      var r = processSteps.getBoundingClientRect();
      var p = clamp((window.innerHeight * 0.8 - r.top) / Math.max(r.height, window.innerHeight * 0.45), 0, 1);
      processSteps.style.setProperty('--p', p.toFixed(3));
      var steps = processSteps.children;
      for (var i = 0; i < steps.length; i++) steps[i].classList.toggle('is-done', p >= (i + 0.35) / steps.length);
    }
    if (inset && !reduceMotion && y < window.innerHeight * 1.5) {
      inset.style.translate = '0 ' + (y * -0.05).toFixed(1) + 'px';
    }
    lastY = y;
  }
  function requestFrame() { if (!ticking) { ticking = true; window.requestAnimationFrame(onFrame); } }
  window.addEventListener('scroll', requestFrame, { passive: true });
  window.addEventListener('resize', requestFrame);
  if (processSteps && reduceMotion) $$('.step', processSteps).forEach(function (s) { s.classList.add('is-done'); });
  onFrame();

  /* ---------- Mobile menu ---------- */
  var toggle = $('[data-menu-toggle]');
  var nav = $('#nav');
  function setMenu(open) {
    root.classList.toggle('nav-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.firstChild.textContent = open ? 'Close' : 'Menu';
  }
  if (toggle && nav) {
    toggle.addEventListener('click', function () { setMenu(!root.classList.contains('nav-open')); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && root.classList.contains('nav-open')) { setMenu(false); toggle.focus(); }
    });
    window.matchMedia('(min-width: 56rem)').addEventListener('change', function (m) { if (m.matches) setMenu(false); });
  }

  /* ---------- Current page / section in the nav ---------- */
  var curPage = location.pathname.split('/').filter(Boolean).pop() || 'index.html';
  if (curPage.indexOf('.') === -1) curPage += '.html';
  $$('.nav a').forEach(function (a) {
    var href = a.getAttribute('href');
    if (!href) return;
    var targetFile = href.split('#')[0].split('/').filter(Boolean).pop();
    if (targetFile && targetFile === curPage) {
      a.setAttribute('aria-current', 'page');
    }
  });

  var spyLinks = $$('.nav a[href^="#"]');
  if (spyLinks.length && 'IntersectionObserver' in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        spyLinks.forEach(function (a) {
          if (a.getAttribute('href') === '#' + en.target.id) a.setAttribute('aria-current', 'true');
          else a.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    spyLinks.forEach(function (a) { var s = $(a.getAttribute('href')); if (s) spy.observe(s); });
  }

  /* ---------- Scroll reveals: only elements that start below the fold are hidden ---------- */
  $$('[data-stagger]').forEach(function (group) {
    $$('[data-reveal]', group).forEach(function (el, i) { el.style.setProperty('--i', i); });
  });
  if (!reduceMotion && 'IntersectionObserver' in window) {
    var revealer = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.remove('is-pending');
        revealer.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    $$('[data-reveal]').forEach(function (el) {
      if (el.getBoundingClientRect().top > window.innerHeight * 0.95) {
        el.classList.add('is-pending');
        revealer.observe(el);
      }
    });
  }

  /* ---------- Marquees: duplicate the list, loop it smoothly with hover pause ---------- */
  function setupMarquee(m) {
    if (reduceMotion) return;
    var list = $('ul', m);
    if (!list) return;

    var existingView = $('.marquee-view', m);
    if (existingView) {
      m.insertBefore(list, existingView);
      existingView.remove();
    }

    var track = document.createElement('div');
    track.className = 'marquee-track';
    list.classList.add('marquee-group');
    var view = document.createElement('div');
    view.className = 'marquee-view';
    m.insertBefore(view, list);
    view.appendChild(track);
    track.appendChild(list);

    var originals = $$('li', list);
    var guard = 0;
    while (list.scrollWidth < window.innerWidth * 1.5 && guard++ < 8) {
      originals.forEach(function (li) { var c = li.cloneNode(true); c.setAttribute('aria-hidden', 'true'); list.appendChild(c); });
    }
    var copy = list.cloneNode(true);
    copy.setAttribute('aria-hidden', 'true');
    $$('a, button', copy).forEach(function (el) { el.tabIndex = -1; });
    track.appendChild(copy);

    var pxPerSec = Number(m.getAttribute('data-speed')) || 50;
    m.style.setProperty('--marquee-dur', (list.scrollWidth / pxPerSec).toFixed(1) + 's');
    m.classList.add('is-running');

    // Auto pause on hover / resume on mouse leave
    m.addEventListener('mouseenter', function () {
      m.setAttribute('data-paused', 'true');
    });
    m.addEventListener('mouseleave', function () {
      m.removeAttribute('data-paused');
    });
  }

  $$('[data-marquee]').forEach(setupMarquee);

  // ==================== Dynamic Corporate Clients Loader ====================
  var logoMarqueeEl = document.querySelector('.logo-marquee');
  if (logoMarqueeEl) {
    fetch('/api/clients')
      .then(function (r) { return r.json(); })
      .then(function (clients) {
        if (Array.isArray(clients) && clients.length > 0) {
          var ul = $('ul', logoMarqueeEl);
          if (ul) {
            ul.innerHTML = clients.map(function (c) {
              return '<li><img src="' + c.logo + '" width="800" height="500" loading="lazy" alt="' + (c.name || 'Corporate Client') + '"></li>';
            }).join('');
            setupMarquee(logoMarqueeEl);
          }
        }
      })
      .catch(function () {});
  }

  /* ---------- Properties: filter by type ---------- */
  var props = $('[data-props]');
  if (props) {
    var pchips = $$('[data-filter]', props);
    var cards = $$('[data-type]', props);
    var pcount = $('[data-prop-count]', props);
    var pempty = $('[data-prop-empty]', props);
    pchips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        var f = chip.getAttribute('data-filter');
        var shown = 0;
        pchips.forEach(function (c) { c.setAttribute('aria-pressed', String(c === chip)); });
        cards.forEach(function (card) {
          var hit = f === 'all' || card.getAttribute('data-type') === f;
          card.hidden = !hit;
          if (hit) { shown++; card.classList.remove('is-pending'); }
        });
        if (pcount) pcount.textContent = shown + (shown === 1 ? ' property' : ' properties') + ' for sale';
        if (pempty) pempty.hidden = shown !== 0;
      });
    });
  }

  /* ---------- Services: accordion, one open at a time ---------- */
  $$('[data-accordion]').forEach(function (acc) {
    var items = $$('.svc-item', acc);
    items.forEach(function (item) {
      var btn = $('.svc-btn', item);
      btn.addEventListener('click', function () {
        var open = btn.getAttribute('aria-expanded') === 'true';
        items.forEach(function (other) {
          other.classList.remove('is-open');
          $('.svc-btn', other).setAttribute('aria-expanded', 'false');
        });
        if (!open) { item.classList.add('is-open'); btn.setAttribute('aria-expanded', 'true'); }
      });
    });
  });

  /* ---------- "Enquire about this property" pre-fills the form ---------- */
  $$('[data-enquire]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var form = $('[data-enquiry]');
      if (!form) return;
      var sel = form.elements.interest;
      var name = btn.getAttribute('data-enquire');
      if (sel) {
        var opt = Array.prototype.filter.call(sel.options, function (o) { return o.value === name; })[0];
        if (opt) sel.value = name;
      }
      var msg = form.elements.message;
      if (msg && !msg.value) msg.value = 'I would like details on ' + name + '.';
      $('#contact').scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth' });
      setTimeout(function () { form.elements.name.focus({ preventScroll: true }); }, reduceMotion ? 0 : 700);
    });
  });

  /* ---------- Enquiry form ---------- */
  var form = $('[data-enquiry]');
  if (form) {
    var status = $('[data-form-status]', form);
    var submit = $('button[type="submit"]', form);
    var submitLabel = submit.textContent;
    var phoneFallback = form.getAttribute('data-phone') || '96202 53180';
    var startedAt = 0;
    form.addEventListener('focusin', function () { if (!startedAt) startedAt = Date.now(); });

    var rules = {
      name: function (v) { return v.trim().length >= 2 ? '' : 'Enter your name.'; },
      phone: function (v) {
        var d = v.replace(/\D/g, '');
        return d.length >= 10 && d.length <= 13 ? '' : 'Enter a phone number with at least 10 digits.';
      },
      email: function (v) { return !v.trim() || /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) ? '' : 'Check the email address, or leave it empty.'; }
    };
    var consentBox = form.elements.consent;
    var consentOk = function () {
      if (!consentBox) return true;
      var ok = consentBox.checked;
      var box = $('#f-consent-error', form);
      if (box) box.textContent = ok ? '' : 'Tick the box to let us use your details to reply.';
      if (ok) consentBox.removeAttribute('aria-invalid'); else consentBox.setAttribute('aria-invalid', 'true');
      return ok;
    };
    if (consentBox) {
      consentBox.addEventListener('change', function () { if (consentBox.getAttribute('aria-invalid')) consentOk(); });
    }
    var setError = function (input, msg) {
      if (!input) return;
      var box = $('#' + input.id + '-error', form);
      if (box) box.textContent = msg;
      if (msg) input.setAttribute('aria-invalid', 'true'); else input.removeAttribute('aria-invalid');
    };
    var validate = function (input) {
      if (!input) return true;
      var rule = rules[input.name];
      var msg = rule ? rule(input.value) : '';
      setError(input, msg);
      return !msg;
    };
    var setStatus = function (state, msg) {
      if (status) {
        status.setAttribute('data-state', state);
        status.textContent = msg;
      }
    };

    Object.keys(rules).forEach(function (name) {
      var input = form.elements[name];
      if (!input) return;
      input.addEventListener('blur', function () { if (input.value) validate(input); });
      input.addEventListener('input', function () { if (input.getAttribute('aria-invalid')) validate(input); });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      setStatus('', '');
      var firstBad = null;
      Object.keys(rules).forEach(function (name) {
        var input = form.elements[name];
        if (!input) return;
        if (!validate(input) && !firstBad) firstBad = input;
      });
      if (consentBox && !consentOk() && !firstBad) firstBad = consentBox;
      if (firstBad) { firstBad.focus(); return; }
      if (form.elements.website && form.elements.website.value) return; /* honeypot: bots fill this, people never see it */

      var endpoint = form.getAttribute('data-endpoint') || '/api/enquiry';
      var payload = {};
      ['name', 'phone', 'email', 'interest', 'message'].forEach(function (k) {
        var el = form.elements[k];
        payload[k] = el ? el.value.trim() : '';
      });
      payload.page = location.pathname;
      payload.consent = true;
      payload.startedAt = startedAt;
      var key = form.getAttribute('data-access-key');
      if (key) payload.access_key = key;

      if (submit) {
        submit.disabled = true;
        submit.textContent = 'Sending enquiry';
      }
      var ctrl = 'AbortController' in window ? new AbortController() : null;
      var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, 15000);
      fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(payload),
        signal: ctrl ? ctrl.signal : undefined
      }).then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        form.reset();
        setStatus('ok', 'Enquiry sent. We will call you back shortly.');
      }).catch(function () {
        setStatus('error', 'Your enquiry was not sent. Check your connection and send it again, or call ' + phoneFallback + '.');
      }).then(function () {
        clearTimeout(timer);
        if (submit) {
          submit.disabled = false;
          submit.textContent = submitLabel;
        }
      });
    });
  }

  // ==================== Dynamic Public Testimonials Loader ====================
  var testiContainer = document.getElementById('public-testimonials-container');
  if (testiContainer) {
    fetch('/api/testimonials')
      .then(function (r) { return r.json(); })
      .then(function (list) {
        var activeItems = (list || []).filter(function (t) { return t.active !== false; });
        if (!activeItems.length) return;

        testiContainer.innerHTML = '';
        activeItems.forEach(function (t) {
          var card = document.createElement('article');
          card.className = 'testi-public-card';
          var stars = '★★★★★'.slice(0, t.rating || 5);

          card.innerHTML = [
            '<div class="testi-public-top">',
            '  <img src="' + (t.image || 'assets/img/clients/axis-capstone.webp') + '" alt="' + t.name + '" class="testi-public-avatar" onerror="this.src=\'assets/img/clients/axis-capstone.webp\'">',
            '  <div>',
            '    <h3 class="testi-public-name">' + t.name + '</h3>',
            '    <p class="testi-public-role">' + t.role + '</p>',
            '  </div>',
            '</div>',
            '<div class="testi-public-stars">' + stars + '</div>',
            '<blockquote class="testi-public-quote">“' + t.comment + '”</blockquote>',
            '<div class="testi-public-foot">',
            '  <span class="note">' + (t.date || 'Verified Client') + '</span>',
            '  <span class="testi-public-verified">✔ Verified Clearance</span>',
            '</div>'
          ].join('');

          testiContainer.appendChild(card);
        });
      })
      .catch(function (err) {
        console.warn('Could not load testimonials:', err);
      });
  }
  // ==================== Global Clickable Cards (Open Full Service/Scope) ====================
  document.addEventListener('click', function (e) {
    // If clicked on an actual link or button, let natural click happen
    if (e.target.closest('a') || e.target.closest('button') || e.target.closest('input')) return;

    // 1. Service Feature Card
    var serviceCard = e.target.closest('.service-feature-card');
    if (serviceCard) {
      var sLink = serviceCard.querySelector('a.service-explore-link') || serviceCard.querySelector('a.service-card-thumb-link') || serviceCard.querySelector('.service-card-title a') || serviceCard.querySelector('a.text-link') || serviceCard.querySelector('h3 a');
      if (sLink && sLink.href) {
        window.location.href = sLink.href;
      }
      return;
    }

    // 2. Government Authority Card
    var govtCard = e.target.closest('.govt-auth-card');
    if (govtCard) {
      var gLink = govtCard.querySelector('a.govt-auth-link') || govtCard.querySelector('.govt-auth-thumb-link') || govtCard.querySelector('.govt-auth-title a') || govtCard.querySelector('h3 a');
      if (gLink && gLink.href) {
        window.location.href = gLink.href;
      }
      return;
    }
  });
})();
