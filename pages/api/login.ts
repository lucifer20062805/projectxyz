import type { NextApiRequest, NextApiResponse } from 'next';
import { pool } from '../../lib/db';

type LoginRequest = {
  username: string;
  password: string;
};

type LoginResponse = {
  success: boolean;
  message?: string;
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<LoginResponse>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, message: 'Method not allowed' });
  }

  const { username, password }: LoginRequest = req.body;

  if (!username || !password) {
    return res.status(400).json({ success: false, message: 'Username and password are required' });
  }

  if (typeof username !== 'string' || typeof password !== 'string') {
    return res.status(400).json({ success: false, message: 'Invalid input types' });
  }

  try {
    const result = await pool.query(
      `SELECT id FROM users 
       WHERE username = $1 
       AND password_hash = crypt($2, password_hash)`,
      [username.trim(), password]
    );

    if (result.rows.length === 0) {
      return res.status(401).json({ success: false, message: 'Invalid credentials' });
    }

    return res.status(200).json({ success: true });
  } catch (error) {
    console.error('Database error during login:', error instanceof Error ? error.message : 'Unknown error');
    return res.status(500).json({ success: false, message: 'Internal server error' });
  }
}
