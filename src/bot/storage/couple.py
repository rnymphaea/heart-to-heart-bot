import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from src.bot.storage.model import Couple, User


async def create_couple(session: AsyncSession, telegram_id: int) -> Couple:
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise ValueError("Пользователь уже состоит в паре")

    token = uuid.uuid4().hex
    couple = Couple(token=token)
    user = User(telegram_id=telegram_id, couple=couple)

    session.add(couple)
    session.add(user)

    await session.commit()
    await session.refresh(couple)
    await session.refresh(user)

    return couple


async def leave_couple(session: AsyncSession, telegram_id: int) -> None:
    result = await session.execute(
        select(User)
        .options(selectinload(User.couple).selectinload(Couple.users))
        .where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise ValueError("Пользователь не найден")

    couple = user.couple

    await session.delete(user)

    if not couple.is_active:
        await session.delete(couple)

    await session.commit()


async def user_in_couple(session: AsyncSession, telegram_id: int) -> None | str:
    result = await session.execute(
        select(User)
        .options(selectinload(User.couple))
        .where(User.telegram_id == telegram_id)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        return existing_user.couple.token

    return None


async def join_couple(session: AsyncSession, telegram_id: int, token: str) -> Couple:
    existing_user = await user_in_couple(session, telegram_id)
    if existing_user:
        raise ValueError("вы уже состоите в паре")

    couple = await session.scalar(
        select(Couple).where(Couple.token == token)
    )
    if not couple:
        raise ValueError("пара с таким кодом не найдена")

    if couple.is_active:
        raise ValueError("к этой паре уже присоединились оба партнёра")

    new_user = User(telegram_id=telegram_id, couple=couple)
    session.add(new_user)

    couple.is_active = True
    await session.commit()
    await session.refresh(couple)

    return couple
