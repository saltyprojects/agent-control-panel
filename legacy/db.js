const { Pool } = require('pg');

// Database connection pool
const pool = new Pool({
  connectionString: process.env.DATABASE_URL || process.env.DATABASE_PRIVATE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Test connection
pool.on('connect', () => {
  console.log('✓ Connected to PostgreSQL database');
});

pool.on('error', (err) => {
  console.error('PostgreSQL pool error:', err);
});

// Waitlist functions
async function addToWaitlist(email, source = 'landing', metadata = {}) {
  const result = await pool.query(
    'INSERT INTO waitlist (email, source, metadata) VALUES ($1, $2, $3) ON CONFLICT (email) DO NOTHING RETURNING id, created_at',
    [email, source, metadata]
  );
  return result.rows[0];
}

async function getWaitlistCount() {
  const result = await pool.query('SELECT COUNT(*) FROM waitlist');
  return parseInt(result.rows[0].count);
}

async function getWaitlist(limit = 100, offset = 0) {
  const result = await pool.query(
    'SELECT id, email, created_at, source FROM waitlist ORDER BY created_at DESC LIMIT $1 OFFSET $2',
    [limit, offset]
  );
  return result.rows;
}

// Agent functions (for future use)
async function createAgent(userId, name, model, metadata = {}) {
  const result = await pool.query(
    'INSERT INTO agents (user_id, name, model, metadata) VALUES ($1, $2, $3, $4) RETURNING *',
    [userId, name, model, metadata]
  );
  return result.rows[0];
}

async function getAgents(userId) {
  const result = await pool.query(
    'SELECT * FROM agents WHERE user_id = $1 ORDER BY created_at DESC',
    [userId]
  );
  return result.rows;
}

async function logAgentActivity(agentId, action, target, status, metadata = {}) {
  await pool.query(
    'INSERT INTO agent_logs (agent_id, action, target, status, metadata) VALUES ($1, $2, $3, $4, $5)',
    [agentId, action, target, status, metadata]
  );
}

// Initialize database schema
async function initDatabase() {
  try {
    const fs = require('fs');
    const schema = fs.readFileSync(__dirname + '/schema.sql', 'utf8');
    await pool.query(schema);
    console.log('✓ Database schema initialized');
  } catch (err) {
    console.error('Error initializing database:', err);
    throw err;
  }
}

module.exports = {
  pool,
  addToWaitlist,
  getWaitlistCount,
  getWaitlist,
  createAgent,
  getAgents,
  logAgentActivity,
  initDatabase,
};
