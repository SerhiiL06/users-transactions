from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request
from src.services.impl.transactions_service_impl import TransactionServiceImpl
from typing import Annotated
from core.database.connection import core
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

transactions_router = APIRouter(tags=["transactions"])

templates = Jinja2Templates(directory="templates")


@transactions_router.get("/transaction")
async def transaction_form(request: Request):
    return templates.TemplateResponse(request, "create-transaction.html")


@transactions_router.post("/transaction")
async def create_trans(
    request: Request,
    session: Annotated[AsyncSession, Depends(core.session_transaction)],
    service: Annotated[TransactionServiceImpl, Depends()],
):

    form_data = await request.form()

    await service.create_transaction(
        form_data.get("user_id"), form_data.get("amount"), session
    )
    return RedirectResponse("/users/", 204)


@transactions_router.get("/transaction/list/")
async def fetch_transactions(
    request: Request,
    session: Annotated[AsyncSession, Depends(core.session_transaction)],
    service: Annotated[TransactionServiceImpl, Depends()],
):
    trans_list = await service.get_transactions_list(request.query_params, session)
    return templates.TemplateResponse(
        request,
        "trans_list.html",
        {"object_list": trans_list, "count": len(trans_list)},
    )
