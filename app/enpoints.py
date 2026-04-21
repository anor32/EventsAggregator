from fastapi import APIRouter
router = APIRouter()


@router.get('/api/health/')
@router.get('/')
async def health():
    return {'status':'ok'}