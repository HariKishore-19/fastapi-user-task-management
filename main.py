from fastapi import FastAPI

from routers.users import router as users_router
from routers.tasks import router as tasks_router


app = FastAPI(title="Simple To-Do API")

app.include_router(users_router)
app.include_router(tasks_router)