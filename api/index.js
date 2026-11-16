const requestHandler = require('../server.js');
const db = require('../db.js');

let dbInitialized = false;

module.exports = async (req, res) => {
  if (!dbInitialized) {
    try {
      await db.initDb();
      dbInitialized = true;
    } catch (e) {
      console.error('Vercel Neon DB Init Warning:', e);
    }
  }
  return requestHandler(req, res);
};

