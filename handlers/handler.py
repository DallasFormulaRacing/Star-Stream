from typing import TYPE_CHECKING, List, Self

if TYPE_CHECKING:
    from ..state import State 
    from ..models import Event
    
class Handler:
    async def process_event(state: "State", data: "Event"): None
    