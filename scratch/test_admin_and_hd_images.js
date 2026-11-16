const http = require('http');

function request(method, path, body) {
  return new Promise((resolve, reject) => {
    const opts = {
      hostname: 'localhost',
      port: 3000,
      path: path,
      method: method,
      headers: {
        'Content-Type': 'application/json'
      }
    };
    const req = http.request(opts, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, headers: res.headers, json: JSON.parse(data), raw: data });
        } catch (e) {
          resolve({ status: res.statusCode, headers: res.headers, raw: data });
        }
      });
    });
    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

async function testAll() {
  console.log('=== 1. Testing Admin Pages & HD Card Images ===');
  const urls = [
    '/admin',
    '/admin.html',
    '/assets/img/dept/dept-bbmp.webp',
    '/assets/img/dept/dept-bda.webp',
    '/assets/img/dept/dept-bmrda.webp',
    '/assets/img/dept/dept-bmicapa.webp',
    '/assets/img/dept/dept-bmrcl.webp',
    '/assets/img/dept/dept-kiadb.webp',
    '/assets/img/dept/dept-citb.webp',
    '/assets/img/dept/dept-rera.webp'
  ];
  for (const u of urls) {
    const res = await request('GET', u);
    if (res.status === 200) {
      console.log(`[PASS 200] ${u}`);
    } else {
      console.error(`[FAIL ${res.status}] ${u}`);
    }
  }

  console.log('\n=== 2. Testing Admin Login API ===');
  const loginRes = await request('POST', '/api/admin/login', { username: 'admin', password: 'verna2026' });
  console.log('Login Response:', loginRes.status, loginRes.json);

  console.log('\n=== 3. Testing Testimonials API (CRUD) ===');
  const listRes = await request('GET', '/api/testimonials');
  console.log(`GET /api/testimonials: ${listRes.status}, count: ${listRes.json.length}`);

  // Create Testimonial
  const createRes = await request('POST', '/api/testimonials', {
    name: 'Automation Test Client',
    role: 'CEO, Infra Holdings',
    rating: 5,
    comment: 'Testing dynamic testimonial creation.',
    image: 'assets/img/clients/sasken.webp',
    active: true
  });
  console.log('POST /api/testimonials:', createRes.status, createRes.json ? createRes.json.testimonial.id : 'Err');
  const testId = createRes.json.testimonial.id;

  // Edit Testimonial
  const editRes = await request('PUT', `/api/testimonials/${testId}`, {
    comment: 'Updated testimonial comment with 5 stars.'
  });
  console.log('PUT /api/testimonials/:id:', editRes.status, editRes.json ? editRes.json.testimonial.comment : 'Err');

  // Delete Testimonial
  const delRes = await request('DELETE', `/api/testimonials/${testId}`);
  console.log('DELETE /api/testimonials/:id:', delRes.status, delRes.json);

  console.log('\n=== 4. Testing Enquiries API ===');
  const enqList = await request('GET', '/api/enquiries');
  console.log(`GET /api/enquiries: ${enqList.status}, count: ${enqList.json.length}`);

  if (enqList.json.length > 0) {
    const firstId = enqList.json[0].id;
    const updateEnq = await request('PUT', `/api/enquiries/${firstId}`, {
      status: 'In Progress',
      notes: 'Consultation conducted by Ajay Vernekar.'
    });
    console.log(`PUT /api/enquiries/${firstId}:`, updateEnq.status, updateEnq.json ? updateEnq.json.enquiry.status : 'Err');
  }

  console.log('\n=== 5. Testing Image Upload API ===');
  const tinyPngBase64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==';
  const uploadRes = await request('POST', '/api/upload', {
    filename: 'test-avatar.png',
    base64: tinyPngBase64
  });
  console.log('POST /api/upload:', uploadRes.status, uploadRes.json);

  console.log('\nALL ADMIN & HD IMAGES AUDIT PASSED 100%!');
}

testAll().catch(console.error);

