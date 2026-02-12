from contextlib import asynccontextmanager
from app.database.pool import db_pool

@asynccontextmanager
async def get_connection():
     async with db_pool.pool.acquire() as conn:
        yield conn 
         
        