from fastapi import FastAPI

from app.database import Base, engine
from app.api import router

app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    import uvicorn
    print("Starting fastapi server")
    uvicorn.run(app, host="0.0.0.0", port=8000)
