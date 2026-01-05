from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db_session
from app.deps.auth import require_roles
from app.models.user import UserRole
from app.schemas.user import UserCreateAdmin, UserPublic, UserUpdateAdmin, UsersList
from app.services.users import UsersService

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get(
    "/users",
    response_model=UsersList,
    dependencies=[Depends(require_roles(UserRole.admin))],
)
async def list_users(
    session: AsyncSession = Depends(get_db_session),
    role: UserRole | None = None,
    q: str | None = None,
    is_active: bool | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> UsersList:
    items, total = await UsersService(session).list_users_filtered(
        role=role,
        q=q,
        is_active=is_active,
        limit=limit,
        offset=offset,
    )
    return UsersList(
        items=[UserPublic.model_validate(u, from_attributes=True) for u in items],
        total=total,
    )


@router.post(
    "/users",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(UserRole.admin))],
)
async def create_user_admin(
    body: UserCreateAdmin,
    session: AsyncSession = Depends(get_db_session),
) -> UserPublic:
    users = UsersService(session)
    existing = await users.get_by_email(body.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = await users.create_user(
        email=body.email,
        full_name=body.full_name,
        role=body.role,
        password=body.password,
    )
    return UserPublic.model_validate(user, from_attributes=True)


@router.patch(
    "/users/{user_id}",
    response_model=UserPublic,
    dependencies=[Depends(require_roles(UserRole.admin))],
)
async def update_user_admin(
    user_id: uuid.UUID,
    body: UserUpdateAdmin,
    session: AsyncSession = Depends(get_db_session),
) -> UserPublic:
    users = UsersService(session)
    user = await users.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    patch = {k: v for k, v in body.model_dump().items() if v is not None}
    updated = await users.update_user(user, patch)
    return UserPublic.model_validate(updated, from_attributes=True)
