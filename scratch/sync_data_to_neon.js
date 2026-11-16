const fs = require('fs');
const path = require('path');
const { pool } = require('../db.js');

async function syncAll() {
  const tList = JSON.parse(fs.readFileSync(path.join(__dirname, '../testimonials.json'), 'utf8'));
  for (const t of tList) {
    await pool.query(
      `INSERT INTO testimonials (id, name, role, service, comment, rating, image, active)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
       ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, comment = EXCLUDED.comment`,
      [t.id, t.name, t.role, t.service || '', t.comment, t.rating || 5, t.image || '', t.active !== false]
    );
  }
  console.log('Seeded testimonials:', tList.length);

  const lList = JSON.parse(fs.readFileSync(path.join(__dirname, '../leads.json'), 'utf8'));
  for (const l of lList) {
    await pool.query(
      `INSERT INTO enquiries (id, name, phone, email, service, authority, message, status, notes)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
       ON CONFLICT (id) DO UPDATE SET status = EXCLUDED.status`,
      [l.id, l.name, l.phone, l.email, l.service, l.authority, l.message, l.status || 'New', l.notes || '']
    );
  }
  console.log('Seeded leads:', lList.length);

  const { rows: tRows } = await pool.query('SELECT COUNT(*) FROM testimonials');
  const { rows: lRows } = await pool.query('SELECT COUNT(*) FROM enquiries');
  const { rows: cRows } = await pool.query('SELECT COUNT(*) FROM clients');
  console.log('Counts in Neon PG -> Testimonials:', tRows[0].count, 'Enquiries:', lRows[0].count, 'Clients:', cRows[0].count);
  await pool.end();
}

syncAll().catch(err => {
  console.error('Sync error:', err);
  process.exit(1);
});
