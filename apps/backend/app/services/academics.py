from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.academic_record import AcademicRecord


class AcademicsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, record_id: uuid.UUID) -> AcademicRecord | None:
        res = await self.session.execute(select(AcademicRecord).where(AcademicRecord.id == record_id))
        return res.scalar_one_or_none()

    async def list(
        self,
        *,
        student_user_id: uuid.UUID | None = None,
        term: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[AcademicRecord], int]:
        q = select(AcademicRecord)
        cq = select(func.count(AcademicRecord.id))

        if student_user_id is not None:
            q = q.where(AcademicRecord.student_user_id == student_user_id)
            cq = cq.where(AcademicRecord.student_user_id == student_user_id)
        if term:
            q = q.where(AcademicRecord.term == term)
            cq = cq.where(AcademicRecord.term == term)

        q = q.order_by(AcademicRecord.created_at.desc()).limit(limit).offset(offset)

        items_res = await self.session.execute(q)
        count_res = await self.session.execute(cq)

        items = list(items_res.scalars().all())
        total = int(count_res.scalar_one())
        return items, total

    async def create(self, record: AcademicRecord) -> AcademicRecord:
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def update(self, record: AcademicRecord, patch: dict) -> AcademicRecord:
        for k, v in patch.items():
            setattr(record, k, v)
        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def delete(self, record: AcademicRecord) -> None:
        await self.session.delete(record)
        await self.session.commit()

    @staticmethod
    def forbid_if_none(record: AcademicRecord | None) -> AcademicRecord:
        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Academic record not found")
        return record
