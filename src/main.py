from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.routers import notes, users, auth

app = FastAPI()


app.include_router(notes.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get('/')
async def get_root():
    ''' redirect to /docs '''
    return RedirectResponse('/docs')
