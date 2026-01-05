from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db_session
from app.schemas.admin import AdminBootstrapRequest, AdminBootstrapResponse
from app.services.admin_bootstrap import AdminBootstrapService

router = APIRouter(prefix="/bootstrap", tags=["bootstrap"])


@router.post("/admin", response_model=AdminBootstrapResponse, status_code=status.HTTP_201_CREATED)
async def bootstrap_admin(
    body: AdminBootstrapRequest,
    session: AsyncSession = Depends(get_db_session),
) -> AdminBootstrapResponse:
    user = await AdminBootstrapService(session).bootstrap_admin(
        bootstrap_token=body.bootstrap_token,
        email=body.email,
        password=body.password,
        full_name=body.full_name,
    )
    return AdminBootstrapResponse(created=True, role=user.role)
