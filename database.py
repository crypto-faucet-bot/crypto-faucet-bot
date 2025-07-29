import aiosqlite

async def init_db():
    async with aiosqlite.connect("users.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                referrer_id INTEGER
            )
        """)
        await db.commit()

async def register_user(user_id, username, referrer_id=None):
    async with aiosqlite.connect("users.db") as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id, username, referrer_id) VALUES (?, ?, ?)",
                         (user_id, username, referrer_id))
        await db.commit()

async def get_referral_stats(user_id):
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT COUNT(*) FROM users WHERE referrer_id = ?", (user_id,))
        count = await cursor.fetchone()
        return count[0]