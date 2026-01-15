from datetime import datetime
from typing import Optional, List, Dict

from sqlalchemy import select, update, func

from backend import db
from models.punishment import Punishment
from models.punishment_type import PunishmentType


async def create_punishment(
    guild_id: int,
    user_id: int,
    moderator_id: int,
    punishment_type: PunishmentType,
    reason: str,
    expires_at: Optional[datetime] = None,
) -> Punishment:
    """
    Create a new punishment record in the database
    :param guild_id:
    :param user_id:
    :param moderator_id:
    :param punishment_type:
    :param reason:
    :param expires_at:
    :return:
    """
    async with db.session() as session:
        punishment = Punishment(
            guild_id=guild_id,
            user_id=user_id,
            moderator_id=moderator_id,
            punishment_type=punishment_type,
            reason=reason,
            expires_at=expires_at,
            is_active=True,
        )

        session.add(punishment)
        await session.commit()
        await session.refresh(punishment)

        return punishment


async def get_user_punishments(
    guild_id: int,
    user_id: int,
    active_only: bool = False,
    punishment_type: Optional[PunishmentType] = None,
) -> List[Punishment]:
    """
    Get all punishments for a user in a guild
    :param guild_id:
    :param user_id:
    :param active_only:
    :param punishment_type:
    :return:
    """
    async with db.session() as session:
        query = select(Punishment).where(
            Punishment.guild_id == guild_id,
            Punishment.user_id == user_id,
        )

        if active_only:
            query = query.where(Punishment.is_active == True)

        if punishment_type:
            query = query.where(Punishment.punishment_type == punishment_type)

        query = query.order_by(Punishment.added_at.desc())

        result = await session.execute(query)
        return list(result.scalars().all())


async def deactivate_punishment(punishment_id: int) -> bool:
    """
    Mark a punishment as inactive
    :param punishment_id:
    :return:
    """
    async with db.session() as session:
        stmt = update(Punishment).where(
            Punishment.punishment_id == punishment_id,
            Punishment.is_active == True,
        )
        result = await session.execute(stmt)
        return result.rowcount > 0


async def get_active_timeouts(guild_id: int) -> List[Punishment]:
    """
    Get all active timeout punishments for a guild
    :param guild_id:
    :return:
    """
    async with db.session() as session:
        query = select(Punishment).where(
            Punishment.guild_id == guild_id,
            Punishment.punishment_type == PunishmentType.TIMEOUT,
            Punishment.is_active == True,
        )
        result = await session.execute(query)
        return list(result.scalars().all())


async def get_guild_moderation_stats(guild_id: int) -> Dict:
    """
    Get moderation statistics for a guild
    :param guild_id:
    :return:
    """
    async with db.session() as session:
        total_query = select(func.count(Punishment.punishment_id)).where(Punishment.guild_id == guild_id)
        total_result = await session.execute(total_query)
        total = total_result.scalar() or 0

        active_query = select(func.count(Punishment.punishment_id)).where(
            Punishment.guild_id == guild_id,
            Punishment.is_active == True,
        )
        active_result = await session.execute(active_query)
        active = active_result.scalar() or 0

        inactive = total - active

        type_query = (
            select(Punishment.punishment_type, func.count(Punishment.punishment_id))
            .where(Punishment.guild_id == guild_id)
            .group_by(Punishment.punishment_type)
        )
        type_result = await session.execute(type_query)
        by_type = {row[0]: row[1] for row in type_result.all()}

        mod_query = (
            select(Punishment.moderator_id, func.count(Punishment.punishment_id))
            .where(Punishment.guild_id == guild_id)
            .group_by(Punishment.moderator_id)
            .order_by(func.count(Punishment.punishment_id).desc())
        )
        mod_result = await session.execute(mod_query)
        top_moderators = {row[0]: row[1] for row in mod_result.all()}

        return {
            "total": total,
            "active": active,
            "inactive": inactive,
            "by_type": by_type,
            "top_moderators": top_moderators,
        }
