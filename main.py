from fastapi import FastAPI

from src.presentation.routers.transactions_router import transactions_router
from src.presentation.routers.users_router import users_router


def application():

    app = FastAPI()

    app.include_router(users_router)
    app.include_router(transactions_router)
    return app


app = application()
