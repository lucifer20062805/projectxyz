import type { VercelRequest, VercelResponse } from '@vercel/node';
import { jwtVerify } from 'jose';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const cookies = req.headers.cookie || '';
  const tokenMatch = cookies.match(/auth_token=([^;]+)/);

  if (!tokenMatch) {
    return res.status(401).json({ error: 'Not authenticated' });
  }

  try {
    const secret = new TextEncoder().encode(process.env.JWT_SECRET || 'default-secret-change-me');
    const { payload } = await jwtVerify(tokenMatch[1], secret);

    return res.status(200).json({
      user: { id: payload.userId, email: payload.email },
    });
  } catch (error) {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }
}
