const http = require('http');

function get(url) {
  return new Promise((resolve, reject) => {
    http.get('http://localhost:3000' + url, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => resolve({ status: res.statusCode, headers: res.headers, body: data }));
    }).on('error', reject);
  });
}

async function run() {
  console.log('--- Testing Homepage ---');
  const home = await get('/');
  console.log('Homepage Status:', home.status);
  console.log('Has Preloader:', home.body.includes('id="site-preloader"'));
  console.log('Has Properties for sale Section:', home.body.includes('Properties for sale'));
  console.log('Has 8 Govt Cards:', home.body.includes('Bruhat Bengaluru Mahanagara Palike') && home.body.includes('Real Estate Regulatory Authority'));

  console.log('\n--- Testing Preloader Logo Asset ---');
  const logo = await get('/assets/img/verna-logo-dark.png');
  console.log('Logo Asset Status:', logo.status, 'Type:', logo.headers['content-type']);

  console.log('\n--- Testing /properties redirect ---');
  const propRedirect = await get('/properties');
  console.log('Properties Redirect Status:', propRedirect.status, 'Location:', propRedirect.headers['location']);

  console.log('\n--- Testing Master Pages ---');
  for (const page of ['/services', '/departments', '/team', '/contact']) {
    const res = await get(page);
    console.log(`${page}: Status ${res.status}, Preloader: ${res.body.includes('id="site-preloader"')}`);
  }

  console.log('\nAudit complete.');
}

run().catch(console.error);

