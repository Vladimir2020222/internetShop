from contextlib import asynccontextmanager

from fastapi import FastAPI

import mail
from accounts import router as accounts_router


@asynccontextmanager
async def lifespan(fastapi_app):
    await mail.init_smtp()
    yield
    await mail.stop_smtp()


app = FastAPI(lifespan=lifespan)
app.include_router(accounts_router)
