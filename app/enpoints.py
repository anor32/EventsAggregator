from fastapi import APIRouter

router = APIRouter()


@router.get("/api/health/")
@router.get("/")
async def health():
    return {"status": "ok"}


@router.post("/api/sync/trigger")
async def manual_sync():
    pass


@router.get("/api/events")
async def get_events():
    pass


@router.get("/api/events/{event_id}")
async def event_detail(event_id):
    pass


@router.get("/api/events/{event_id}/seats")
async def event_seats(event_id):
    pass


@router.post("/api/tickets", status_code=201)
async def event_register():
    pass


@router.delete("/api/tickets/{ticket_id}")
async def cancel_register():
    return {"success": True}
