import { Handler, HandlerEvent, HandlerContext } from '@netlify/functions';
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false,
  },
});

interface LoginRequest {
  username: string;
  password: string;
}

interface LoginResponse {
  success: boolean;
  message?: string;
}

export const handler: Handler = async (
  event: HandlerEvent,
  context: HandlerContext
): Promise<{ statusCode: number; body: string }> => {
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ success: false, message: 'Method not allowed' }),
    };
  }

  if (!process.env.DATABASE_URL) {
    console.error('DATABASE_URL environment variable is not set');
    return {
      statusCode: 500,
      body: JSON.stringify({ success: false, message: 'Internal server error' }),
    };
  }

  let body: LoginRequest;
  try {
    body = JSON.parse(event.body || '{}');
  } catch (error) {
    return {
      statusCode: 400,
      body: JSON.stringify({ success: false, message: 'Invalid JSON' }),
    };
  }

  const { username, password } = body;

  if (!username || !password) {
    return {
      statusCode: 400,
      body: JSON.stringify({ success: false, message: 'Username and password are required' }),
    };
  }

  if (typeof username !== 'string' || typeof password !== 'string') {
    return {
      statusCode: 400,
      body: JSON.stringify({ success: false, message: 'Invalid input types' }),
    };
  }

  try {
    const result = await pool.query(
      `SELECT id FROM users 
       WHERE username = $1 
       AND password_hash = crypt($2, password_hash)`,
      [username.trim(), password]
    );

    if (result.rows.length === 0) {
      return {
        statusCode: 401,
        body: JSON.stringify({ success: false, message: 'Invalid credentials' }),
      };
    }

    return {
      statusCode: 200,
      body: JSON.stringify({ success: true }),
    };
  } catch (error) {
    console.error('Database error during login:', error instanceof Error ? error.message : 'Unknown error');
    return {
      statusCode: 500,
      body: JSON.stringify({ success: false, message: 'Internal server error' }),
    };
  }
};
