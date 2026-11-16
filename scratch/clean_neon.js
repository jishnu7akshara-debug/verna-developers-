const db = require('../db.js');

async function run() {
  await db.pool.query("DELETE FROM testimonials WHERE name = 'QWERTGW' OR id LIKE 'testi-1794829213717%'");
  const t = await db.getTestimonials();
  const e = await db.getEnquiries();
  console.log('Neon Testimonials count:', t.length);
  console.log('Neon Enquiries count:', e.length);
  process.exit(0);
}
run();
