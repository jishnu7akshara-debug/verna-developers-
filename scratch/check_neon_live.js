const { Pool } = require('pg');

const pool = new Pool({
  connectionString: 'postgresql://neondb_owner:npg_VfX58yKABtgw@ep-misty-hat-bd4yfroo-pooler.c-8.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require',
  ssl: { rejectUnauthorized: false }
});

async function runCheck() {
  console.log('=== Neon PostgreSQL Live Database Audit ===');
  
  // Testimonials
  const { rows: tRows } = await pool.query('SELECT id, name, role, rating FROM testimonials LIMIT 5');
  console.log(`Testimonials in Neon PG (${tRows.length}):`);
  tRows.forEach(t => console.log(`  - [${t.id}] ${t.name} (${t.role}) ★${t.rating}`));

  // Clients
  const { rows: cRows } = await pool.query('SELECT id, name, category, logo FROM clients ORDER BY display_order ASC LIMIT 6');
  console.log(`Corporate Clients in Neon PG (${cRows.length}):`);
  cRows.forEach(c => console.log(`  - [${c.id}] ${c.name} (${c.category})`));

  // Enquiries
  const { rows: eRows } = await pool.query('SELECT id, name, phone, status FROM enquiries LIMIT 5');
  console.log(`Enquiries in Neon PG (${eRows.length}):`);
  eRows.forEach(e => console.log(`  - [${e.id}] ${e.name} (${e.phone}) -> ${e.status}`));

  await pool.end();
  console.log('=== LIVE AUDIT COMPLETE: 100% CONNECTED ===');
}

runCheck().catch(err => {
  console.error('Audit failed:', err);
  process.exit(1);
});

