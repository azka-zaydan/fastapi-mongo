from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from routers import notes, users, auth

app = FastAPI()


app.include_router(notes.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get('/')
async def get_root():
    return RedirectResponse('/docs')


if __name__ == '__main__':
    uvicorn.run('main:app', port=5000, reload=True)
