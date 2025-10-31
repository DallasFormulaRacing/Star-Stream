import asyncpg
from os import getenv

class State(object):
    conn: asyncpg.Connection 
    
    def __init__(self, pg_uri: str):
        self.pg_uri = pg_uri

        self.conn = None 
    
    def set_conn(self, conn: asyncpg.Connection):
        self.conn = conn 
            
    async def setup(self):
        # connect to postgres
        self.conn = await asyncpg.connect(self.pg_uri)
    
    