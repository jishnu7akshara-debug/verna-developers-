// @ts-check
/**
 * Verna Developers Layout Check
 * Tests all public pages at 8 widths for:
 * 1. No horizontal overflow
 * 2. No clipped text (scrollWidth > clientWidth with overflow hidden)
 * 3. Full-page screenshots per page per width into tests/screenshots/
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
      await page.waitForTimeout(800); // let JS / fonts settle

      // 1. Horizontal overflow
      const result = await page.evaluate(() => {
        const sw = document.documentElement.scrollWidth;
        const iw = window.innerWidth;
        const bad = [];
        if (sw > iw + 2) {
          document.querySelectorAll('*').forEach(el => {
            const r = el.getBoundingClientRect();
            if (r.right > iw + 2 && r.width > 0 && r.height > 0) {
              const cls = Array.from(el.classList).slice(0,2).join('.');
              bad.push(`${el.tagName.toLowerCase()}${cls ? '.' + cls : ''} right=${Math.round(r.right)}`);
            }
          });
        }
        return { sw, iw, bad: bad.slice(0, 6) };
      });

      if (result.sw > result.iw + 2) {
        console.log(`OVERFLOW ${pg.name}@${width}: scrollW=${result.sw} Offenders: ${result.bad.join(' | ')}`);
      }
      expect(result.sw, `Horizontal overflow on ${pg.name}@${width}. Offenders: ${result.bad.join(', ')}`
      ).toBeLessThanOrEqual(result.iw + 2);

      // 2. Clipped text
      const clipped = await page.evaluate(() => {
        const out = [];
        document.querySelectorAll('h1,h2,h3,h4,p,a,button,li,label').forEach(el => {
          const st = window.getComputedStyle(el);
          if ((st.overflow === 'hidden' || st.overflowX === 'hidden')
              && el.scrollWidth > el.clientWidth + 4 && el.clientWidth > 0) {
            out.push(`${el.tagName} "${(el.textContent||'').trim().slice(0, 25)}"`);
          }
        });
        return out.slice(0, 4);
      });
      if (clipped.length) console.log(`CLIPPED ${pg.name}@${width}:`, clipped.join(' | '));

      // 3. Screenshot
      await page.screenshot({
        path: path.join(ssDir, `${pg.name}-${width}.png`),
        fullPage: true
      });
    });
  }
}
