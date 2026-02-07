-- Neon PostgreSQL schema for love app
-- Run this in your Neon SQL Editor to create the users table.

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optional: create one account for her (replace with your chosen username and run once)
-- INSERT is done via the app signup flow; do not store plain passwords here.
