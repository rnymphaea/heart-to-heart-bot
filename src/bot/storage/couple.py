import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.storage.model import Couple, User


async def create_couple(session: AsyncSession, telegram_id: int) -> Couple:
    token = uuid.uuid4().hex
    couple = Couple(token=token)
    user = User(telegram_id=telegram_id, couple=couple)

    session.add(couple)
    session.add(user)

    await session.commit()
    await session.refresh(couple)
    await session.refresh(user)

    return couple
