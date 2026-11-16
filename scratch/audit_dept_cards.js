const http = require('http');

const urls = [
  '/',
  '/index.html',
  '/departments',
  '/departments.html',
  '/dept-bbmp',
  '/dept-bda',
  '/dept-bmrda',
  '/dept-bmicapa',
  '/dept-bmrcl',
  '/dept-kiadb',
  '/dept-citb',
  '/dept-rera',
  '/assets/img/dept/dept-bbmp.webp',
  '/assets/img/dept/dept-bbmp-2x.webp',
  '/assets/img/dept/dept-bda.webp',
  '/assets/img/dept/dept-bda-2x.webp',
  '/assets/img/dept/dept-bmrda.webp',
  '/assets/img/dept/dept-bmrda-2x.webp',
  '/assets/img/dept/dept-bmicapa.webp',
  '/assets/img/dept/dept-bmicapa-2x.webp',
  '/assets/img/dept/dept-bmrcl.webp',
  '/assets/img/dept/dept-bmrcl-2x.webp',
  '/assets/img/dept/dept-kiadb.webp',
  '/assets/img/dept/dept-kiadb-2x.webp',
  '/assets/img/dept/dept-citb.webp',
  '/assets/img/dept/dept-citb-2x.webp',
  '/assets/img/dept/dept-rera.webp',
  '/assets/img/dept/dept-rera-2x.webp'
];

async function checkUrl(url) {
  return new Promise((resolve) => {
    http.get('http://localhost:3000' + url, (res) => {
      resolve({ url, status: res.statusCode, type: res.headers['content-type'] });
    }).on('error', (err) => {
      resolve({ url, error: err.message });
    });
  });
}

async function run() {
  console.log('Testing all department pages and card image assets...');
  let errors = 0;
  for (const u of urls) {
    const res = await checkUrl(u);
    if (res.status === 200) {
      console.log(`[PASS 200] ${u} (${res.type})`);
    } else {
      console.error(`[FAIL ${res.status || 'ERR'}] ${u}`, res.error || '');
      errors++;
    }
  }
  console.log(`\nAudit complete: ${urls.length - errors} passed, ${errors} failed.`);
  if (errors > 0) process.exit(1);
}

run();

