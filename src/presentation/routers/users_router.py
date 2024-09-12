from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.connection import core
from src.services.impl.user_service_impl import UserServiceImpl

users_router = APIRouter(tags=["users"], prefix="/users")

templates = Jinja2Templates(directory="templates")


@users_router.get("/register/")
async def register(request: Request):
    return templates.TemplateResponse(request, "register.html")


@users_router.post("/register/")
async def register(
    request: Request,
    session: Annotated[AsyncSession, Depends(core.session_transaction)],
    service: UserServiceImpl = Depends(UserServiceImpl),
):
    data = await request.form()
    user_id = await service.register(data, session)
    return templates.TemplateResponse(request, "register.html", {"user_id": user_id})


@users_router.get("/")
async def user_list(
    request: Request,
    session: Annotated[AsyncSession, Depends(core.session_transaction)],
    service: Annotated[UserServiceImpl, Depends()],
):
    users = await service.fetch_users(session)
    return templates.TemplateResponse(
        request, "user_list.html", context={"users": users}
    )


@users_router.get("/{user_id}/")
async def user_info(
    request: Request,
    user_id: int,
    session: Annotated[AsyncSession, Depends(core.session_transaction)],
    service: UserServiceImpl = Depends(UserServiceImpl),
):
    user = await service.fetch_user_info(user_id, session)

    if not user:
        return templates.TemplateResponse(request, "notfound.html")
    return templates.TemplateResponse(request, "detail.html", {"user": user})


@users_router.post("/{user_id}/delete/")
async def delete_user(
    request: Request,
    user_id: int,
    session: Annotated[AsyncSession, Depends(core.session_transaction)],
    service: UserServiceImpl = Depends(UserServiceImpl),
):
    await service.delete_user(user_id, session)
    return RedirectResponse("/users/", 301)


@users_router.get("/{user_id}/update/")
async def update(
    request: Request,
    user_id: int,
    session: Annotated[AsyncSession, Depends(core.session_transaction)],
    service: UserServiceImpl = Depends(UserServiceImpl),
):
    user = await service.fetch_user_info(user_id, session)

    if not user:
        return templates.TemplateResponse(request, "notfound.html")

    return templates.TemplateResponse(request, "update.html", {"user": user})


@users_router.post("/{user_id}/update/")
async def update(
    request: Request,
    user_id: int,
    session: Annotated[AsyncSession, Depends(core.session_transaction)],
    service: UserServiceImpl = Depends(UserServiceImpl),
):

    form_data = await request.form()
    await service.update_user(user_id, form_data, session)
    return RedirectResponse("/users/", 301)
