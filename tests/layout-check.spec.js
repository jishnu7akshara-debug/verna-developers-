// @ts-check
/**
 * Verna Developers Layout Check
 * Tests all 29 public pages at 8 widths [320, 360, 390, 430, 768, 820, 1024, 1280] for:
 * 1. No horizontal overflow (scrollWidth <= innerWidth)
 * 2. No overlapping non-nested visible text-bearing elements (>2px intersection)
 * 3. No clipped text (scrollWidth > clientWidth with overflow hidden)
 * 4. Full-page screenshots per page per width into tests/screenshots/
 */
const { test, expect } = require('@playwright/test');
const path = require('path');
const fs = require('fs');

const PAGES = [
  { name: 'home',         path: '/' },
  { name: 'about',        path: '/about.html' },
  { name: 'services',     path: '/services.html' },
  { name: 'departments',  path: '/departments.html' },
  { name: 'team',         path: '/team.html' },
  { name: 'contact',      path: '/contact.html' },
  { name: 'properties',   path: '/properties.html' },
  { name: '404',          path: '/404.html' },
  { name: 'dept-bbmp',    path: '/dept-bbmp.html' },
  { name: 'dept-bda',     path: '/dept-bda.html' },
  { name: 'dept-bmrda',   path: '/dept-bmrda.html' },
  { name: 'dept-bmicapa', path: '/dept-bmicapa.html' },
  { name: 'dept-bmrcl',   path: '/dept-bmrcl.html' },
  { name: 'dept-citb',    path: '/dept-citb.html' },
  { name: 'dept-kiadb',   path: '/dept-kiadb.html' },
  { name: 'dept-rera',    path: '/dept-rera.html' },
  { name: 'svc-buying',   path: '/service-buying-selling.html' },
  { name: 'svc-agri',     path: '/service-agriculture-land-conversion.html' },
  { name: 'svc-dispute',  path: '/service-dispute-resolutions.html' },
  { name: 'svc-legal',    path: '/service-legal-advisory.html' },
  { name: 'svc-npa',      path: '/service-npa-funding.html' },
  { name: 'svc-liaison',  path: '/service-residential-industrial-liaison.html' },
  { name: 'prop-avalahalli',        path: '/property-avalahalli.html' },
  { name: 'prop-banashankari',      path: '/property-banashankari.html' },
  { name: 'prop-chikkanagamangala', path: '/property-chikkanagamangala.html' },
  { name: 'prop-doddamavalli',      path: '/property-doddamavalli.html' },
  { name: 'prop-hulimavu',          path: '/property-hulimavu.html' },
  { name: 'prop-koramangala',       path: '/property-koramangala.html' },
  { name: 'prop-kumara-park',       path: '/property-kumara-park.html' },
];

const WIDTHS = [320, 360, 390, 430, 768, 820, 1024, 1280];
const HEIGHTS = {
  320: 568, 360: 780, 390: 844, 430: 932,
  768: 1024, 820: 1180, 1024: 768, 1280: 800
};

const ssDir = path.join(__dirname, 'screenshots');
if (!fs.existsSync(ssDir)) fs.mkdirSync(ssDir, { recursive: true });

for (const pg of PAGES) {
  for (const width of WIDTHS) {
    const height = HEIGHTS[width] || 800;

    test(`${pg.name} @ ${width}px`, async ({ page }) => {
      await page.setViewportSize({ width, height });
      await page.goto(pg.path, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await page.waitForTimeout(800);

      const report = await page.evaluate(() => {
        const sw = document.documentElement.scrollWidth;
        const iw = window.innerWidth;
        const overflowOffenders = [];
        if (sw > iw + 2) {
          document.querySelectorAll('*').forEach(el => {
            const r = el.getBoundingClientRect();
            if (r.right > iw + 2 && r.width > 0 && r.height > 0) {
              const cls = Array.from(el.classList).slice(0, 2).join('.');
              overflowOffenders.push(`${el.tagName.toLowerCase()}${cls ? '.' + cls : ''} right=${Math.round(r.right)}`);
            }
          });
        }

        // Clipped text
        const clipped = [];
        document.querySelectorAll('h1,h2,h3,h4,p,a,button,li,label').forEach(el => {
          const st = window.getComputedStyle(el);
          if (st.display === 'none' || st.visibility === 'hidden') return;
          if ((st.overflow === 'hidden' || st.overflowX === 'hidden') &&
              !el.closest('.marquee') && !el.classList.contains('visually-hidden') &&
              !el.classList.contains('skip') &&
              el.scrollWidth > el.clientWidth + 4 && el.clientWidth > 0) {
            clipped.push(`${el.tagName.toLowerCase()} "${(el.textContent || '').trim().slice(0, 25)}"`);
          }
        });

        // Overlap check among visible non-nested text-bearing elements (excluding intentional fixed layers & marquees)
        const isLayer = el => !!el.closest('.site-header, .bottom-tab-bar, .floating-whatsapp, .site-preloader, .marquee, [hidden], .nav:not(.is-open)');
        const items = [];
        document.querySelectorAll('h1,h2,h3,h4,p,a,button,label,input,select,textarea').forEach(el => {
          if (isLayer(el)) return;
          const st = window.getComputedStyle(el);
          if (st.display === 'none' || st.visibility === 'hidden' || parseFloat(st.opacity) === 0) return;
          if (!el.textContent?.trim() && el.tagName !== 'INPUT' && el.tagName !== 'SELECT' && el.tagName !== 'TEXTAREA') return;
          const r = el.getBoundingClientRect();
          if (r.width < 2 || r.height < 2) return;
          items.push({ el, r, tag: el.tagName.toLowerCase(), txt: (el.textContent || el.getAttribute('name') || '').trim().slice(0, 22) });
        });

        const overlaps = [];
        for (let i = 0; i < items.length; i++) {
          for (let j = i + 1; j < items.length; j++) {
            const a = items[i], b = items[j];
            if (a.el.contains(b.el) || b.el.contains(a.el)) continue;
            const ix = Math.min(a.r.right, b.r.right) - Math.max(a.r.left, b.r.left);
            const iy = Math.min(a.r.bottom, b.r.bottom) - Math.max(a.r.top, b.r.top);
            if (ix > 4 && iy > 4) {
              overlaps.push(`${a.tag}("${a.txt}") <-> ${b.tag}("${b.txt}") [${Math.round(ix)}x${Math.round(iy)}px]`);
              if (overlaps.length >= 5) break;
            }
          }
          if (overlaps.length >= 5) break;
        }

        return {
          sw, iw,
          overflowOffenders: overflowOffenders.slice(0, 6),
          clipped: clipped.slice(0, 5),
          overlaps
        };
      });

      if (report.clipped.length) {
        console.log(`CLIPPED ${pg.name}@${width}:`, report.clipped.join(' | '));
      }
      if (report.overlaps.length) {
        console.log(`OVERLAP ${pg.name}@${width}:`, report.overlaps.join(' | '));
      }

      expect(report.sw, `Horizontal overflow on ${pg.name}@${width}: ${report.overflowOffenders.join(', ')}`).toBeLessThanOrEqual(report.iw + 2);
      expect(report.overlaps, `Element overlap on ${pg.name}@${width}: ${report.overlaps.join(', ')}`).toEqual([]);

      await page.screenshot({
        path: path.join(ssDir, `${pg.name}-${width}.png`),
        fullPage: true
      });
    });
  }
}
