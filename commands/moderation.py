from datetime import timedelta
from typing import Optional

import discord
from discord.ext import commands

from core.helper import parse_duration, retrieve_current_time
from master import compass, service
from models.punishment_type import PunishmentType


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        name="ban",
        description="Ban a user from the server",
    )
    @commands.has_permissions(ban_members=True)
    async def ban(
        self,
        ctx: commands.Context,
        user: discord.User,
        delete_messages: Optional[int] = 0,
        *,
        reason: str = "No reason provided",
    ):
        """
        Ban a user from the server
        :param ctx:
        :param user:
        :param delete_messages:
        :param reason:
        :return:
        """
        if delete_messages < 0 or delete_messages > 7:
            await ctx.reply("Delete messages must be between 0 and 7 days.")
            return

        if user.id == ctx.author.id:
            await ctx.reply("You cannot ban yourself.")
            return

        if user.id == self.bot.user.id:
            await ctx.reply("I cannot ban myself.")
            return

        try:
            await service.apply_ban(
                ctx.guild,
                user,
                reason,
                delete_messages,
            )

            await compass.create_punishment(
                guild_id=ctx.guild.id,
                user_id=user.id,
                moderator_id=ctx.author.id,
                punishment_type=PunishmentType.BAN,
                reason=reason,
            )

            embed = discord.Embed(
                title="🔨 User Banned",
                description=f"**{user.mention}** has been banned from the server.",
                color=0x393A41,
                timestamp=retrieve_current_time(),
            )

            await ctx.reply(embed=embed)

        except Exception as e:
            await ctx.send(f"Something went wrong when banning {user.mention}!")
            print(f"Something went wrong when banning usert at {ctx.guild.id}/{user.id}: {e}")

    @commands.command(
        name="kick",
        description="Kick a member from the server",
    )
    @commands.has_permissions(kick_members=True)
    async def kick(
        self,
        ctx: commands.Context,
        member: discord.Member,
        *,
        reason: str = "No reason provided",
    ):
        """
        Kick a member from the server
        :param ctx:
        :param member:
        :param reason:
        :return:
        """
        if member.id == ctx.author.id:
            await ctx.reply("You cannot kick yourself.")
            return

        if member.id == self.bot.user.id:
            await ctx.reply("I cannot kick myself.")
            return

        try:
            await service.apply_kick(
                ctx.guild,
                member,
                reason,
            )

            await compass.create_punishment(
                guild_id=ctx.guild.id,
                user_id=member.id,
                moderator_id=ctx.author.id,
                punishment_type=PunishmentType.KICK,
                reason=reason,
            )

            embed = discord.Embed(
                title="👢 Member Kicked",
                description=f"**{member.mention}** has been kicked from the server.",
                color=0x393A41,
                timestamp=retrieve_current_time(),
            )

            await ctx.reply(embed=embed)

        except Exception as e:
            await ctx.send(f"Something went wrong when kicking {member.mention}!")
            print(f"Something went wrong when kicking member at {ctx.guild.id}/{member.id}: {e}")

    @commands.command(
        name="mute",
        description="Timeout a member",
    )
    @commands.has_permissions(moderate_members=True)
    async def mute(
        self,
        ctx: commands.Context,
        member: discord.Member,
        duration: str,
        *,
        reason: str = "No reason provided",
    ):
        """
        Timeout (mute) a member for a specified duration
        :param ctx:
        :param member:
        :param duration:
        :param reason:
        :return:
        """
        if member.id == ctx.author.id:
            await ctx.reply("You cannot mute yourself.")
            return

        if member.id == self.bot.user.id:
            await ctx.reply("I cannot mute myself.")
            return

        try:
            duration_delta = parse_duration(duration)
        except ValueError as e:
            await ctx.reply(f"Invalid duration format: {e}")
            return

        if duration_delta > timedelta(days=28):
            await ctx.reply("Timeout duration cannot exceed 28 days.")
            return

        try:
            expires_at = retrieve_current_time() + duration_delta

            await service.apply_timeout(
                member,
                duration_delta,
                reason,
            )

            await compass.create_punishment(
                guild_id=ctx.guild.id,
                user_id=member.id,
                moderator_id=ctx.author.id,
                punishment_type=PunishmentType.TIMEOUT,
                reason=reason,
                expires_at=expires_at,
            )

            embed = discord.Embed(
                title="🔇 Member Timed Out",
                description=f"**{member.mention}** has been timed out.",
                color=0x393A41,
                timestamp=retrieve_current_time(),
            )

            await ctx.reply(embed=embed)

        except Exception as e:
            await ctx.send(f"Something went wrong when timing out {member.mention}!")
            print(f"Something went wrong when timing out member at {ctx.guild.id}/{member.id}: {e}")

    @commands.command(
        name="warn",
        description="Warn a member",
    )
    @commands.has_permissions(moderate_members=True)
    async def warn(
        self,
        ctx: commands.Context,
        member: discord.Member,
        *,
        reason: str = "No reason provided",
    ):
        """
        Warn a member
        :param ctx:
        :param member:
        :param reason:
        :return:
        """
        if member.id == ctx.author.id:
            await ctx.reply("You cannot warn yourself.")
            return

        if member.id == self.bot.user.id:
            await ctx.reply("You cannot warn me.")
            return

        try:
            await service.apply_warn(
                member,
                reason,
                ctx.author,
            )

            await compass.create_punishment(
                guild_id=ctx.guild.id,
                user_id=member.id,
                moderator_id=ctx.author.id,
                punishment_type=PunishmentType.WARN,
                reason=reason,
            )

            embed = discord.Embed(
                title="⚠️ Member Warned",
                description=f"**{member.mention}** has been warned.",
                color=0x393A41,
                timestamp=retrieve_current_time(),
            )

            await ctx.reply(embed=embed)

        except Exception as e:
            await ctx.send(f"Something went wrong when warning {member.mention}!")
            print(f"Something went wrong when warning member at {ctx.guild.id}/{member.id}: {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
