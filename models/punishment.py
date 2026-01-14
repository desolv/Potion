from sqlalchemy import Column, BigInteger, Boolean, DateTime, String, Enum

from backend.base import Base
from core.helper import retrieve_current_time
from models.punishment_type import PunishmentType


class Punishment(Base):
    __tablename__ = "punishment"

    punishment_id = Column(BigInteger, autoincrement=True, primary_key=True)

    guild_id = Column(BigInteger, nullable=False, index=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    moderator_id = Column(BigInteger, nullable=False, index=True)

    punishment_type = Column(
        Enum(PunishmentType, name="punishment_type_enum"),
        nullable=False,
    )

    reason = Column(String, nullable=False)

    added_at = Column(DateTime, default=retrieve_current_time)
    expires_at = Column(DateTime, nullable=True)

    is_active = Column(Boolean, default=True, index=True)
