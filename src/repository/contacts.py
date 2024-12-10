from typing import List, Optional
from datetime import date, timedelta, datetime
from sqlalchemy import func, case, select, or_, extract, and_, text
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Contact
from src.schemas import ContactModel


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(
        self,
        skip: int = 0,
        limit: int = 100,
        name: Optional[str] = None,
        lastname: Optional[str] = None,
        email: Optional[str] = None,
    ) -> List[Contact]:

        query = select(Contact).offset(skip).limit(limit)
        filters = []

        if name:
            filters.append(Contact.firstname.ilike(f"%{name}%"))
        if lastname:
            filters.append(Contact.lastname.ilike(f"%{lastname}%"))
        if email:
            filters.append(Contact.email.ilike(f"%{email}%"))

        if filters:
            query = query.where(or_(*filters))

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_contact_by_id(self, contact_id: int) -> Contact | None:
        stmt = select(Contact).filter_by(id=contact_id)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def create_contact(self, body: ContactModel) -> Contact:
        contact = Contact(**body.model_dump(exclude_unset=True))
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def update_contact(
        self, contact_id: int, body: ContactModel
    ) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            contact.firstname = body.firstname
            contact.lastname = body.lastname
            contact.email = body.email
            contact.phone = body.phone
            contact.birthdate = body.birthdate
            contact.additional = body.additional

            await self.db.commit()
            await self.db.refresh(contact)
        return contact

    async def remove_contact(self, contact_id: int) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def get_upcoming_birthdays(self) -> List[Contact]:
        today = datetime.utcnow()
        next_week = today + timedelta(days=7)

        stmt = select(Contact).filter(
            and_(
                Contact.birthdate
                >= today.replace(hour=0, minute=0, second=0, microsecond=0),
                Contact.birthdate
                <= next_week.replace(hour=23, minute=59, second=59, microsecond=999999),
            )
        )

        results = await self.db.execute(stmt)
        return results.scalars().all()
