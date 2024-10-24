from datetime import datetime, timezone
from .handler import Handler 
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import SessionEvent

#if your wondering why the session. anything isnt highlighted, its because the session data model 
#is implemented by type checking therefore it cant recognize until runtime (to prevent circular imports)
class SessionHandler(Handler):
    async def process_event(state, session: "SessionEvent.Data"):

        if session.status == "Open":
            await state.conn.execute(
                """
                INSERT INTO sessions (id, start, status, car) 
                VALUES ($1, $2, $3, $4)
                """,
                session.id, session.start, session.status, session.car
            )
        elif session.status == "Closed":
            await state.conn.execute(
                """
                UPDATE sessions
                SET stop = $1, status = $2
                WHERE id = $3
                """,
                session.stop, session.status, session.id
            )
        else:
            raise ValueError(f"Invalid session status {session.status}")
        # within rows to insert, since its 7 fields, i didnt know outside just filling the fields with "None" 
        # didnt know if it was according to model or the fields in postgres database