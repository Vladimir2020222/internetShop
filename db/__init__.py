from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import config

engine = create_async_engine(
    f"postgresql+asyncpg://{config.DB_USERNAME}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/internetshop"
)


async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
