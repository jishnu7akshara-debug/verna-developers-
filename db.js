const { Pool } = require('pg');
const fs = require('fs');
const path = require('path');

// Load .env file if present (for local development)
const envPath = path.join(__dirname, '.env');
if (fs.existsSync(envPath)) {
  const envLines = fs.readFileSync(envPath, 'utf8').split(/\r?\n/);
  for (const line of envLines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const eqIdx = trimmed.indexOf('=');
    if (eqIdx > 0) {
      const key = trimmed.slice(0, eqIdx).trim();
      const val = trimmed.slice(eqIdx + 1).trim().replace(/^['"]|['"]$/g, '');
      if (!process.env[key]) process.env[key] = val;
    }
  }
}

const connectionString = process.env.DATABASE_URL || 'postgresql://neondb_owner:npg_VfX58yKABtgw@ep-misty-hat-bd4yfroo-pooler.c-8.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require';

const pool = new Pool({
  connectionString,
  ssl: { rejectUnauthorized: false }
});

pool.on('error', (err) => {
  console.error('[NEON PG POOL ERROR]', err.message);
});

// Initialize database schema and migrate initial data
async function initDb() {
  try {
    const client = await pool.connect();
    console.log('[NEON PG] Connected to cloud database.');

    // 1. Create testimonials table
    await client.query(`
      CREATE TABLE IF NOT EXISTS testimonials (
        id VARCHAR(64) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        role VARCHAR(255),
        service VARCHAR(255),
        comment TEXT,
        rating INT DEFAULT 5,
        image TEXT,
        active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // 2. Create enquiries table
    await client.query(`
      CREATE TABLE IF NOT EXISTS enquiries (
        id VARCHAR(64) PRIMARY KEY,
        name VARCHAR(255),
        phone VARCHAR(64),
        email VARCHAR(255),
        service VARCHAR(255),
        authority VARCHAR(255),
        message TEXT,
        status VARCHAR(64) DEFAULT 'New',
        notes TEXT,
        received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // 3. Create clients table
    await client.query(`
      CREATE TABLE IF NOT EXISTS clients (
        id VARCHAR(64) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        category VARCHAR(255),
        logo TEXT NOT NULL,
        display_order INT DEFAULT 1,
        featured BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // 4. Create settings table to prevent re-seeding after user deletions
    await client.query(`
      CREATE TABLE IF NOT EXISTS app_settings (
        key VARCHAR(64) PRIMARY KEY,
        val TEXT
      );
    `);

    const { rows: sRows } = await client.query("SELECT val FROM app_settings WHERE key = 'seeded'");
    const alreadySeeded = sRows.length > 0 && sRows[0].val === 'true';

    if (!alreadySeeded) {
      await client.query("INSERT INTO app_settings (key, val) VALUES ('seeded', 'true') ON CONFLICT (key) DO UPDATE SET val = 'true'");
      console.log('[NEON PG] Initial seed flag initialized.');
    }

    client.release();
    console.log('[NEON PG] Cloud database tables initialized successfully!');
  } catch (err) {
    console.error('[NEON PG INIT ERROR]', err.message);
  }
}

// ==================== TESTIMONIALS METHODS ====================
async function getTestimonials() {
  try {
    const res = await pool.query('SELECT * FROM testimonials ORDER BY created_at DESC');
    return res.rows.map(r => ({
      id: r.id,
      name: r.name,
      role: r.role,
      service: r.service,
      comment: r.comment,
      rating: r.rating,
      image: r.image,
      active: r.active
    }));
  } catch (err) {
    console.error('[PG ERROR getTestimonials]', err.message);
    const file = path.join(__dirname, 'testimonials.json');
    return fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, 'utf8')) : [];
  }
}

async function createTestimonial(data) {
  const id = data.id || 'testi-' + Date.now();
  try {
    await pool.query(
      `INSERT INTO testimonials (id, name, role, service, comment, rating, image, active)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8)`,
      [id, data.name, data.role, data.service, data.comment, data.rating || 5, data.image || '', data.active !== false]
    );
  } catch (err) {
    console.error('[PG ERROR createTestimonial]', err.message);
  }
  return { id, ...data };
}

async function updateTestimonial(id, data) {
  try {
    await pool.query(
      `UPDATE testimonials
       SET name = COALESCE($1, name),
           role = COALESCE($2, role),
           service = COALESCE($3, service),
           comment = COALESCE($4, comment),
           rating = COALESCE($5, rating),
           image = COALESCE($6, image),
           active = COALESCE($7, active)
       WHERE id = $8`,
      [data.name, data.role, data.service, data.comment, data.rating, data.image, data.active, id]
    );
  } catch (err) {
    console.error('[PG ERROR updateTestimonial]', err.message);
  }
  return { id, ...data };
}

async function deleteTestimonial(id) {
  try {
    await pool.query('DELETE FROM testimonials WHERE id = $1', [id]);
  } catch (err) {
    console.error('[PG ERROR deleteTestimonial]', err.message);
  }
  try {
    const tFile = path.join(__dirname, 'testimonials.json');
    if (fs.existsSync(tFile)) {
      const list = JSON.parse(fs.readFileSync(tFile, 'utf8')).filter(x => x.id !== id);
      fs.writeFileSync(tFile, JSON.stringify(list, null, 2));
    }
  } catch (e) {}
  return true;
}

// ==================== ENQUIRIES METHODS ====================
async function getEnquiries() {
  try {
    const res = await pool.query('SELECT * FROM enquiries ORDER BY received_at DESC');
    return res.rows.map(r => ({
      id: r.id,
      name: r.name,
      phone: r.phone,
      email: r.email,
      service: r.service,
      authority: r.authority,
      message: r.message,
      status: r.status,
      notes: r.notes,
      receivedAt: r.received_at
    }));
  } catch (err) {
    console.error('[PG ERROR getEnquiries]', err.message);
    return [];
  }
}

async function createEnquiry(data) {
  const id = data.id || 'lead-' + Date.now();
  try {
    await pool.query(
      `INSERT INTO enquiries (id, name, phone, email, service, authority, message, status, notes)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)`,
      [id, data.name, data.phone, data.email, data.service, data.authority, data.message, data.status || 'New', data.notes || '']
    );
  } catch (err) {
    console.error('[PG ERROR createEnquiry]', err.message);
  }
  return { id, ...data };
}

async function updateEnquiry(id, data) {
  try {
    await pool.query(
      `UPDATE enquiries
       SET status = COALESCE($1, status),
           notes = COALESCE($2, notes)
       WHERE id = $3`,
      [data.status, data.notes, id]
    );
  } catch (err) {
    console.error('[PG ERROR updateEnquiry]', err.message);
  }
  return { id, ...data };
}

async function deleteEnquiry(id) {
  try {
    await pool.query('DELETE FROM enquiries WHERE id = $1', [id]);
  } catch (err) {
    console.error('[PG ERROR deleteEnquiry]', err.message);
  }
  try {
    const lFile = path.join(__dirname, 'leads.json');
    if (fs.existsSync(lFile)) {
      const list = JSON.parse(fs.readFileSync(lFile, 'utf8')).filter(x => x.id !== id);
      fs.writeFileSync(lFile, JSON.stringify(list, null, 2));
    }
  } catch (e) {}
  return true;
}

// ==================== CLIENTS METHODS ====================
async function getClients() {
  try {
    const res = await pool.query('SELECT * FROM clients ORDER BY display_order ASC, created_at ASC');
    return res.rows.map(r => ({
      id: r.id,
      name: r.name,
      category: r.category,
      logo: r.logo,
      order: r.display_order,
      featured: r.featured
    }));
  } catch (err) {
    console.error('[PG ERROR getClients]', err.message);
    const file = path.join(__dirname, 'clients.json');
    return fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, 'utf8')) : [];
  }
}

async function createClient(data) {
  const id = data.id || 'client-' + Date.now();
  try {
    await pool.query(
      `INSERT INTO clients (id, name, category, logo, display_order, featured)
       VALUES ($1, $2, $3, $4, $5, $6)
       ON CONFLICT (id) DO UPDATE SET
         name = EXCLUDED.name,
         category = EXCLUDED.category,
         logo = EXCLUDED.logo,
         display_order = EXCLUDED.display_order,
         featured = EXCLUDED.featured`,
      [id, data.name, data.category, data.logo, data.order || 1, data.featured !== false]
    );
  } catch (err) {
    console.error('[PG ERROR createClient]', err.message);
  }
  try {
    const cFile = path.join(__dirname, 'clients.json');
    if (fs.existsSync(cFile)) {
      const list = JSON.parse(fs.readFileSync(cFile, 'utf8')).filter(x => x.id !== id);
      list.push({ id, ...data });
      fs.writeFileSync(cFile, JSON.stringify(list, null, 2));
    }
  } catch (e) {}
  return { id, ...data };
}

async function updateClient(id, data) {
  try {
    await pool.query(
      `UPDATE clients
       SET name = COALESCE($1, name),
           category = COALESCE($2, category),
           logo = COALESCE($3, logo),
           display_order = COALESCE($4, display_order),
           featured = COALESCE($5, featured)
       WHERE id = $6`,
      [data.name, data.category, data.logo, data.order, data.featured, id]
    );
  } catch (err) {
    console.error('[PG ERROR updateClient]', err.message);
  }
  return { id, ...data };
}

async function deleteClient(id) {
  try {
    await pool.query('DELETE FROM clients WHERE id = $1', [id]);
  } catch (err) {
    console.error('[PG ERROR deleteClient]', err.message);
  }
  try {
    const cFile = path.join(__dirname, 'clients.json');
    if (fs.existsSync(cFile)) {
      const list = JSON.parse(fs.readFileSync(cFile, 'utf8')).filter(x => x.id !== id);
      fs.writeFileSync(cFile, JSON.stringify(list, null, 2));
    }
  } catch (e) {}
  return true;
}

module.exports = {
  pool,
  initDb,
  getTestimonials,
  createTestimonial,
  updateTestimonial,
  deleteTestimonial,
  getEnquiries,
  createEnquiry,
  updateEnquiry,
  deleteEnquiry,
  getClients,
  createClient,
  updateClient,
  deleteClient
};

