import logging
import uuid

from pyrogram import filters
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired
from pyrogram.raw import base
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.phone import (
    CreateGroupCall,
    DiscardGroupCall,
    ExportGroupCallInvite,
    GetGroupParticipants,
)
from pyrogram.types import Message

from YukkiMusic import app
from YukkiMusic.utils.database import get_assistant


@app.on_message(filters.command("startvc"))
async def startvc(client, message: Message):

    call_name = message.text.split(maxsplit=1)[1] if len(message.command) > 1 else " VC"
    hell = await message.reply_text("Starting Voice Chat...")
    userbot = await get_assistant(message.chat.id)

    try:
        await userbot.invoke(
            CreateGroupCall(
                peer=(await userbot.resolve_peer(message.chat.id)),
                random_id=int(str(uuid.uuid4().int)[:8]),
                title=call_name,
            )
        )

        await hell.edit_text("Voice Chat started!")
    except ChatAdminRequired:
        await hell.edit_text(
            "Give Manage vc power To My Assistant instead to use this Command"
        )
    except Exception as e:
        logging.exception(e)
        await hell.edit_text(str(e))


@app.on_message(filters.command("endvc"))
async def endvc(client, message: Message):
    hell = await message.reply_text("Ending Voice Chat...")
    userbot = await get_assistant(message.chat.id)

    try:
        full_chat: base.messages.ChatFull = await userbot.invoke(
            GetFullChannel(channel=(await userbot.resolve_peer(message.chat.id)))
        )
        await userbot.invoke(DiscardGroupCall(call=full_chat.full_chat.call))
        await hell.edit_text("Voice Chat ended!")
    except ChatAdminRequired:
        await hell.edit_text(
            "Give me Manage vc power To My Assistant instead to use this Command"
        )
    except Exception as e:
        if "'NoneType' object has no attribute 'write'" in str(e):
            await hell.edit_text("vc is already off baby")
        elif "phone.DiscardGroupCall" in str(e):
            await hell.edit_text(
                "Give Manage vc power To My Assistant instead to use this Command"
            )
        else:
            logging.exception(e)
            await hell.edit_text(e)


@app.on_message(filters.command("vclink"))
async def vclink(client, message: Message):
    userbot = await get_assistant(message.chat.id)
    hell = await message.reply_text("Getting Voice Chat link...")

    try:
        full_chat: base.messages.ChatFull = await userbot.invoke(
            GetFullChannel(channel=(await userbot.resolve_peer(message.chat.id)))
        )

        invite: base.phone.ExportedGroupCallInvite = await userbot.invoke(
            ExportGroupCallInvite(call=full_chat.full_chat.call)
        )
        await hell.edit_text(f"Voice Chat Link: {invite.link}")
    except ChatAdminRequired:
        await hell.edit_text(
            "Give me Manage vc power To My Assistant instead to use this Command"
        )
    except Exception as e:
        if "'NoneType' object has no attribute 'write'" in str(e):
            await hell.edit_text("vc is  off baby")
        else:
            logging.exception(e)
            await hell.edit_text(e)


@app.on_message(filters.command("vcmembers"))
async def vcmembers(client, message: Message):
    userbot = await get_assistant(message.chat.id)
    hell = await message.reply_text("Getting Voice Chat members...")

    try:
        full_chat: base.messages.ChatFull = await userbot.invoke(
            GetFullChannel(channel=(await userbot.resolve_peer(message.chat.id)))
        )
        participants: base.phone.GroupParticipants = await userbot.invoke(
            GetGroupParticipants(
                call=full_chat.full_chat.call,
                ids=[],
                sources=[],
                offset="",
                limit=1000,
            )
        )
        count = participants.count
        text = f"Total Voice Chat Members: {count}\n"
        users = []
        for participant in participants.participants:
            users.append(participant.peer.user_id)
        for i in users:
            b = await app.get_users(i)
            text += f"[{b.first_name + (' ' + b.last_name if b.last_name else '')}](tg://user?id={b.id})\n"

        await hell.edit_text(text)
    except ChatAdminRequired:
        await hell.edit_text(
            "Give me Manage vc power To My Assistant instead to use this Command"
        )
    except Exception as e:
        if "'NoneType' object has no attribute 'write'" in str(e):
            await hell.edit_text("vc is  off baby")
        else:
            logging.exception(e)
            await hell.edit_text(e)


__MODULE__ = ""
__HELP__ = """
/startvc - sᴛᴀʀᴛ ᴛʜᴇ ᴠᴄ [ᴍᴀᴋᴇ sᴜʀᴇ Assɪsɪᴛᴀɴᴛ ɪs ᴀɴ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴘᴇʀᴍɪssɪᴏɴ]
/vcend - Eɴᴅ ᴛʜᴇ ᴠᴄ [ᴍᴀᴋᴇ sᴜʀᴇ Assɪsɪᴛᴀɴᴛ ɪs ᴀɴ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴘᴇʀᴍɪssɪᴏɴ]
/vclink - ɢᴇᴛ ᴠᴏɪᴄᴇᴄʜᴀᴛ ʟɪɴᴋ
/vcmembers - Gᴇᴛ ᴍᴇᴍᴇʙᴇʀ ʟɪsᴛ ᴛʜᴀᴛ ɪs ɪɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ
"""
