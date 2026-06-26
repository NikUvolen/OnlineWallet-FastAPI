from fastapi import APIRouter, FastAPI

from app.wallets.router import router as wallets_router

app = FastAPI(title='Online Wallet API')
v1_router = APIRouter(prefix='/v1', tags=['v1'])
v1_router.include_router(wallets_router)
app.include_router(v1_router)


@app.get('/')
async def root():
    return {'message': 'app is running'}
