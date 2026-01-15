from datetime import timedelta
from typing import Optional, Dict

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

        await service.apply_warn(
            member,
            reason,
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

    @commands.command(
        name="modlog",
        description="View moderation history for a user",
    )
    @commands.has_permissions(moderate_members=True)
    async def modlog(
        self,
        ctx: commands.Context,
        user: discord.User,
        limit: Optional[int] = 10,
    ):
        """
        View moderation history for a user
        :param ctx:
        :param user:
        :param limit:
        :return:
        """
        if limit < 1 or limit > 25:
            await ctx.reply("Limit must be between 1 and 25.")
            return

        punishments = await compass.get_user_punishments(
            guild_id=ctx.guild.id,
            user_id=user.id,
        )

        if not punishments:
            embed = discord.Embed(
                title="📋 Moderation Log",
                description=f"**{user.mention}** has no moderation history.",
                color=0x393A41,
                timestamp=retrieve_current_time(),
            )
            await ctx.reply(embed=embed)
            return

        punishments = punishments[:limit]

        embed = discord.Embed(
            title="📋 Moderation Log",
            description=f"Moderation history for **{user.mention}**",
            color=0x393A41,
            timestamp=retrieve_current_time(),
        )

        for punishment in punishments:
            moderator = await self.bot.fetch_user(punishment.moderator_id)

            punishment_icon = {
                PunishmentType.BAN: "🔨",
                PunishmentType.KICK: "👢",
                PunishmentType.TIMEOUT: "🔇",
                PunishmentType.WARN: "⚠️",
            }.get(punishment.punishment_type, "❓")

            status = "🟢 Active" if punishment.is_active else "⚫ Inactive"

            field_value = f"**Moderator:** {moderator.mention}\n"
            field_value += f"**Reason:** {punishment.reason}\n"
            field_value += f"**Status:** {status}\n"
            field_value += f"**Date:** <t:{int(punishment.added_at.timestamp())}:F>\n"

            if punishment.expires_at:
                field_value += f"**Expires:** <t:{int(punishment.expires_at.timestamp())}:R>\n"

            embed.add_field(
                name=f"{punishment_icon} {punishment.punishment_type.value.title()} (ID: {punishment.punishment_id})",
                value=field_value,
                inline=False,
            )

        embed.set_footer(
            text=f"Showing {len(punishments)} of {len(await compass.get_user_punishments(ctx.guild.id, user.id))} total punishments"
        )

        await ctx.reply(embed=embed)

    @commands.command(
        name="modstats",
        description="View moderation statistics for the server",
    )
    @commands.has_permissions(moderate_members=True)
    async def modstats(
        self,
        ctx: commands.Context,
    ):
        """
        View moderation statistics for the server
        :param ctx:
        :return:
        """
        stats = await compass.get_guild_moderation_stats(ctx.guild.id)

        if not stats or stats["total"] == 0:
            embed = discord.Embed(
                title="📊 Moderation Statistics",
                description="No moderation actions have been taken in this server.",
                color=0x393A41,
                timestamp=retrieve_current_time(),
            )
            await ctx.reply(embed=embed)
            return

        embed = discord.Embed(
            title="📊 Moderation Statistics",
            description=f"Server-wide moderation statistics for **{ctx.guild.name}**",
            color=0x393A41,
            timestamp=retrieve_current_time(),
        )

        embed.add_field(
            name="📈 Overview",
            value=f"**Total Actions:** {stats['total']}\n"
            f"**Active Punishments:** {stats['active']}\n"
            f"**Inactive Punishments:** {stats['inactive']}",
            inline=False,
        )

        type_breakdown = ""
        for punishment_type, count in stats["by_type"].items():
            icon = {
                PunishmentType.BAN: "🔨",
                PunishmentType.KICK: "👢",
                PunishmentType.TIMEOUT: "🔇",
                PunishmentType.WARN: "⚠️",
            }.get(punishment_type, "❓")
            type_breakdown += f"{icon} **{punishment_type.value.title()}:** {count}\n"

        embed.add_field(
            name="📋 By Type",
            value=type_breakdown,
            inline=True,
        )

        top_mods = ""
        for mod_id, count in list(stats["top_moderators"].items())[:5]:
            try:
                moderator = await self.bot.fetch_user(mod_id)
                top_mods += f"{moderator.mention}: {count}\n"
            except:
                top_mods += f"<@{mod_id}>: {count}\n"

        if top_mods:
            embed.add_field(
                name="👮 Top Moderators",
                value=top_mods,
                inline=True,
            )

        await ctx.reply(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
