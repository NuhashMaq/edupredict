from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db_session
from app.deps.auth import get_current_user, require_roles
from app.models.user import User, UserRole
from app.schemas.user import UserPublic, UsersList
from app.services.users import UsersService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserPublic)
async def get_me(user: User = Depends(get_current_user)) -> UserPublic:
    return UserPublic.model_validate(user, from_attributes=True)


@router.get(
    "",
    response_model=UsersList,
    dependencies=[Depends(require_roles(UserRole.teacher, UserRole.admin))],
)
async def list_users(
    role: UserRole | None = None,
    q: str | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> UsersList:
    # Teachers can only list students. Admins can list all roles.
    if user.role == UserRole.teacher:
        role = UserRole.student
    elif user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    items, total = await UsersService(session).list_users_filtered(
        role=role,
        q=q,
        limit=limit,
        offset=offset,
    )
    return UsersList(items=[UserPublic.model_validate(u, from_attributes=True) for u in items], total=total)
