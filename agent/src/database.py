"""Database connection and operations for Neon DB."""
import asyncpg
import os
from typing import Optional

# Database connection pool
_pool: Optional[asyncpg.Pool] = None


async def get_connection() -> asyncpg.Connection:
    """Get a database connection from the pool."""
    global _pool
    if _pool is None:
        await init_pool()
    return await _pool.acquire()


async def return_connection(conn: asyncpg.Connection):
    """Return a connection to the pool."""
    await _pool.release(conn)


async def init_pool():
    """Initialize the database connection pool."""
    global _pool
    connection_string = os.getenv('NEON_DATABASE_URL')
    
    if not connection_string:
        raise ValueError("NEON_DATABASE_URL environment variable is not set")
    
    _pool = await asyncpg.create_pool(
        connection_string,
        min_size=1,
        max_size=10,
    )
    
    # Initialize schema
    async with _pool.acquire() as conn:
        await create_schema(conn)


async def create_schema(conn: asyncpg.Connection):
    """Create database schema if it doesn't exist."""
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS proverbs (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW()
        )
    """)


async def close_pool():
    """Close the database connection pool."""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None


async def execute_query(query: str, *args):
    """Execute a database query."""
    conn = await get_connection()
    try:
        result = await conn.execute(query, *args)
        return result
    finally:
        await return_connection(conn)


async def fetch_query(query: str, *args):
    """Fetch results from a database query."""
    conn = await get_connection()
    try:
        result = await conn.fetch(query, *args)
        return result
    finally:
        await return_connection(conn)


# Proverbs-specific operations
async def get_proverbs_from_db() -> list[str]:
    """Get all proverbs from the database."""
    try:
        results = await fetch_query("SELECT text FROM proverbs ORDER BY created_at ASC")
        return [row['text'] for row in results]
    except Exception as e:
        print(f"Database error getting proverbs: {e}")
        return []


async def save_proverbs_to_db(proverbs: list[str]) -> None:
    """Save proverbs to the database. Clears existing and adds new ones."""
    try:
        # Clear existing proverbs
        await execute_query("DELETE FROM proverbs")
        
        # Insert new proverbs
        if proverbs:
            conn = await get_connection()
            try:
                await conn.executemany(
                    "INSERT INTO proverbs (text) VALUES ($1)",
                    [(proverb,) for proverb in proverbs]
                )
            finally:
                await return_connection(conn)
    except Exception as e:
        print(f"Database error saving proverbs: {e}")


async def delete_proverb_from_db(proverb: str) -> None:
    """Delete a specific proverb from the database."""
    try:
        await execute_query("DELETE FROM proverbs WHERE text = $1", proverb)
    except Exception as e:
        print(f"Database error deleting proverb: {e}")

