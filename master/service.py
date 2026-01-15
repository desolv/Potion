from datetime import timedelta
import discord


async def apply_ban(
    guild: discord.Guild,
    user: discord.User | discord.Member,
    reason: str,
    delete_message_days: int = 0,
) -> bool:
    """
    Ban a user from the guild
    :param guild:
    :param user:
    :param reason:
    :param delete_message_days:
    :return:
    """
    try:
        await guild.ban(
            user,
            reason=reason,
            delete_message_days=delete_message_days,
        )
        return True
    except Exception as e:
        print(f"Something went wrong when banning user at {guild.id}: {e}")
        return False


async def apply_kick(
    guild: discord.Guild,
    member: discord.Member,
    reason: str,
) -> bool:
    """
    Kick a member from the guild
    :param guild:
    :param member:
    :param reason:
    :return:
    """
    try:
        await member.kick(reason=reason)
        return True
    except Exception as e:
        print(f"Something went wrong when kicking user at {guild.id}: {e}")
        return False


async def apply_timeout(
    guild: discord.Guild,
    member: discord.Member,
    duration: timedelta,
    reason: str,
) -> bool:
    """
    Timeout a user on the guild
    :param guild:
    :param member:
    :param duration:
    :param reason:
    :return:
    """
    try:
        await member.timeout(duration, reason=reason)
        return True
    except Exception as e:
        print(f"Something went wrong when timing out user at {guild.id}: {e}")
        return False


async def apply_warn(
    guild: discord.Guild,
    member: discord.Member,
    reason: str,
    moderator: discord.Member,
) -> bool:
    """
    Send a warning to a user
    :param guild:
    :param member:
    :param reason:
    :param moderator:
    :return:
    """
    try:
        # TODO
        return True
    except Exception as e:
        print(f"Something went wrong when warning user at {guild.id}: {e}")
        return False


async def remove_timeout(
    guild: discord.Guild,
    member: discord.Member,
    reason: str = "Timeout expired",
) -> bool:
    """
    Remove a timeout from a user on the guild
    :param guild:
    :param member:
    :param reason:
    :return:
    """
    try:
        await member.timeout(None, reason=reason)
        return True
    except Exception as e:
        print(f"Something went wrong when removing a timeout from user at {guild.id}: {e}")
        return False
