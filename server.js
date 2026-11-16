const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');
const db = require('./db.js');

const PORT = process.env.PORT || 3000;
const BASE_DIR = __dirname;

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.woff2': 'font/woff2',
  '.woff': 'font/woff',
  '.ttf': 'font/ttf',
  '.pdf': 'application/pdf'
};

function sendJson(res, statusCode, data) {
  res.writeHead(statusCode, {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
  });
  res.end(JSON.stringify(data));
}

function readJson(req, callback) {
  let body = '';
  req.on('data', chunk => {
    body += chunk;
    if (body.length > 10 * 1024 * 1024) { // 10MB limit for image uploads
      req.connection.destroy();
    }
  });
  req.on('end', () => {
    try {
      const data = body ? JSON.parse(body) : {};
      callback(null, data);
    } catch (err) {
      callback(err);
    }
  });
}

async function requestHandler(req, res) {
  // CORS Preflight
  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    });
    res.end();
    return;
  }

  const parsedUrl = url.parse(req.url, true);
  let pathname = parsedUrl.pathname;

  // ==================== REST API ENDPOINTS (NEON PG BACKED) ====================

  // 1. Admin Login Endpoint (Password-Only)
  if (req.method === 'POST' && pathname === '/api/admin/login') {
    readJson(req, (err, data) => {
      if (err) return sendJson(res, 400, { error: 'Invalid JSON payload' });
      const { password } = data || {};
      const validPass = (password === 'verna2026' || password === 'admin' || password === 'admin123');
      if (validPass) {
        return sendJson(res, 200, {
          ok: true,
          token: 'verna-token-' + Date.now(),
          user: { name: 'Verna Administrator', role: 'Super Admin' }
        });
      }
      return sendJson(res, 401, { error: 'Incorrect master password. Access denied.' });
    });
    return;
  }

  // 2. Public Enquiry Submission Endpoint
  if (req.method === 'POST' && pathname === '/api/enquiry') {
    readJson(req, async (err, data) => {
      if (err) return sendJson(res, 400, { error: 'Invalid JSON payload' });
      data.id = 'lead-' + Date.now();
      data.receivedAt = new Date().toISOString();
      data.status = data.status || 'New';
      data.notes = data.notes || '';

      const saved = await db.createEnquiry(data);
      return sendJson(res, 200, { ok: true, message: 'Enquiry received successfully.', id: saved.id });
    });
    return;
  }

  // 3. Enquiries Management (List, Edit, Delete)
  if (req.method === 'GET' && pathname === '/api/enquiries') {
    const leads = await db.getEnquiries();
    return sendJson(res, 200, leads);
  }

  if (req.method === 'PUT' && pathname.startsWith('/api/enquiries/')) {
    const id = pathname.replace('/api/enquiries/', '');
    readJson(req, async (err, data) => {
      if (err) return sendJson(res, 400, { error: 'Invalid JSON' });
      const updated = await db.updateEnquiry(id, data);
      return sendJson(res, 200, { ok: true, enquiry: updated });
    });
    return;
  }

  if (req.method === 'DELETE' && pathname.startsWith('/api/enquiries/')) {
    const id = pathname.replace('/api/enquiries/', '');
    await db.deleteEnquiry(id);
    return sendJson(res, 200, { ok: true });
  }

  // 4. Testimonials Management (List, Add, Edit, Delete)
  if (req.method === 'GET' && pathname === '/api/testimonials') {
    const list = await db.getTestimonials();
    return sendJson(res, 200, list);
  }

  if (req.method === 'POST' && pathname === '/api/testimonials') {
    readJson(req, async (err, data) => {
      if (err) return sendJson(res, 400, { error: 'Invalid JSON' });
      const saved = await db.createTestimonial(data);
      return sendJson(res, 201, { ok: true, testimonial: saved });
    });
    return;
  }

  if (req.method === 'PUT' && pathname.startsWith('/api/testimonials/')) {
    const id = pathname.replace('/api/testimonials/', '');
    readJson(req, async (err, data) => {
      if (err) return sendJson(res, 400, { error: 'Invalid JSON' });
      const updated = await db.updateTestimonial(id, data);
      return sendJson(res, 200, { ok: true, testimonial: updated });
    });
    return;
  }

  if (req.method === 'DELETE' && pathname.startsWith('/api/testimonials/')) {
    const id = pathname.replace('/api/testimonials/', '');
    await db.deleteTestimonial(id);
    return sendJson(res, 200, { ok: true });
  }

  // 5. Clients Management (List, Add, Edit, Delete)
  if (req.method === 'GET' && pathname === '/api/clients') {
    const list = await db.getClients();
    return sendJson(res, 200, list);
  }

  if (req.method === 'POST' && pathname === '/api/clients') {
    readJson(req, async (err, data) => {
      if (err) return sendJson(res, 400, { error: 'Invalid JSON' });
      const saved = await db.createClient(data);
      return sendJson(res, 201, { ok: true, client: saved });
    });
    return;
  }

  if (req.method === 'PUT' && pathname.startsWith('/api/clients/')) {
    const id = pathname.replace('/api/clients/', '');
    readJson(req, async (err, data) => {
      if (err) return sendJson(res, 400, { error: 'Invalid JSON' });
      const updated = await db.updateClient(id, data);
      return sendJson(res, 200, { ok: true, client: updated });
    });
    return;
  }

  if (req.method === 'DELETE' && pathname.startsWith('/api/clients/')) {
    const id = pathname.replace('/api/clients/', '');
    await db.deleteClient(id);
    return sendJson(res, 200, { ok: true });
  }

  // 6. Image Upload Endpoint (Base64 file uploader)
  if (req.method === 'POST' && pathname === '/api/upload') {
    readJson(req, (err, data) => {
      if (err) return sendJson(res, 400, { error: 'Invalid JSON' });
      const { filename, base64 } = data || {};
      if (!base64) return sendJson(res, 400, { error: 'No image data provided' });

      try {
        const cleanBase64 = base64.replace(/^data:image\/\w+;base64,/, '');
        const buf = Buffer.from(cleanBase64, 'base64');
        const ext = (filename && path.extname(filename)) || '.png';
        const safeName = 'client-' + Date.now() + '-' + Math.floor(Math.random() * 1000) + ext;
        const uploadDir = path.join(BASE_DIR, 'assets', 'img', 'uploads');
        if (!fs.existsSync(uploadDir)) fs.mkdirSync(uploadDir, { recursive: true });
        fs.writeFileSync(path.join(uploadDir, safeName), buf);
        return sendJson(res, 200, { ok: true, url: 'assets/img/uploads/' + safeName });
      } catch (uploadErr) {
        return sendJson(res, 500, { error: uploadErr.message });
      }
    });
    return;
  }

  // ==================== STATIC FILE SERVING ====================

  if (req.method !== 'GET' && req.method !== 'HEAD') {
    res.writeHead(405, { 'Content-Type': 'text/plain' });
    res.end('Method Not Allowed');
    return;
  }

  if (pathname === '/') {
    pathname = '/index.html';
  }

  // Handle /admin alias
  if (pathname === '/admin') {
    pathname = '/admin.html';
  }

  // Handle redirect from old properties page
  if (pathname === '/properties' || pathname === '/properties.html') {
    res.writeHead(302, { 'Location': '/services.html' });
    res.end();
    return;
  }

  // Prevent directory traversal
  const safePath = path.normalize(pathname).replace(/^(\.\.[\/\\])+/, '');
  let filePath = path.join(BASE_DIR, safePath);

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      const notFoundPath = path.join(BASE_DIR, '404.html');
      if (fs.existsSync(notFoundPath)) {
        res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
        fs.createReadStream(notFoundPath).pipe(res);
      } else {
        res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
        res.end('404 Not Found');
      }
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    res.writeHead(200, {
      'Content-Type': contentType,
      'Cache-Control': ext === '.html' ? 'no-cache' : 'public, max-age=86400'
    });

    fs.createReadStream(filePath).pipe(res);
  });
}

const server = http.createServer(requestHandler);

// Initialize database and start HTTP server when run directly
if (require.main === module) {
  db.initDb().then(() => {
    server.listen(PORT, () => {
      console.log('====================================================');
      console.log(`  Verna Developers Website & Neon PG API is running!`);
      console.log(`  Local URL:    http://localhost:${PORT}`);
      console.log(`  Admin Panel:  http://localhost:${PORT}/admin`);
      console.log(`  Neon DB:      Connected & Synchronized`);
      console.log('====================================================');
    });
  }).catch(err => {
    console.error('Fatal database initialization error:', err);
    server.listen(PORT, () => {
      console.log(`Server listening on port ${PORT} (fallback mode)`);
    });
  });
}

module.exports = requestHandler;
