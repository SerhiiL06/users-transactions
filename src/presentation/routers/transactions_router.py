from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.connection import core
from src.services.impl.transactions_service_impl import TransactionServiceImpl

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

    result = await service.create_transaction(
        form_data.get("user_id"), int(form_data.get("amount")), session
    )
    if isinstance(result, dict) and result.get("errors"):
        return templates.TemplateResponse(
            request, "create-transaction.html", {"errors": result.get("errors")}
        )

    return RedirectResponse("/users/", 301)


@transactions_router.get("/transaction/list/")
async def fetch_transactions(
    request: Request,
    session: Annotated[AsyncSession, Depends(core.session_transaction)],
    service: Annotated[TransactionServiceImpl, Depends()],
):
    trans_list, statistic_data = await service.get_transactions_list(
        request.query_params, session
    )

    context = {
        "object_list": trans_list,
        "count": statistic_data.get("count"),
        "sum": statistic_data.get("sum"),
    }

    return templates.TemplateResponse(request, "trans_list.html", context)
