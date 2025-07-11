import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ChatAction

from Venom import VenomX as app
from Venom.modules.helpers import is_chatbot_enabled, enable_chatbot, disable_chatbot, durga_api, is_admins

async def text_filter(_, __, m: Message):
    """Filters valid chatbot messages."""
    return (
        bool(m.text)
        and len(m.text) <= 69
        and not m.text.startswith(("!", "/"))
        and (not m.reply_to_message or m.reply_to_message.reply_to_message_id == m._client.me.id)
    )

chatbot_filter = filters.create(text_filter)

@app.on_message(
    ((filters.text & (filters.group | filters.private) & chatbot_filter) | filters.mentioned)
    & ~filters.bot
    & ~filters.sticker
)
async def chatbot(_, message: Message):
    """Replies with chatbot response if enabled or when mentioned (also works in private chat)."""
    chat_id = message.chat.id

    if message.chat.type != "private":
        if not await is_chatbot_enabled(chat_id) and not message.mentioned:
            return

    await app.send_chat_action(chat_id, ChatAction.TYPING)
    reply = durga_api.ask_question(message.text)
    await message.reply_text(reply or "❖ ChatBot Error. Contact @PURVI_SUPPORT.")

@app.on_message(filters.command(["chatbot"]) & filters.group & ~filters.bot)
@is_admins
async def chatbot_toggle(_, message: Message):
    """Shows chatbot enable/disable options."""
    await message.reply_text(
        "**❖ ᴄʜᴀᴛʙᴏᴛ ᴄᴏɴᴛʀᴏʟ ᴘᴀɴᴇʟ.**\n\n"
        f"**✦ ᴄʜᴀᴛ ɴᴀᴍᴇ : {message.chat.title}**\n"
        "**✦ ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴘᴛɪᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ / ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ.**",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("ᴇɴᴀʙʟᴇ", callback_data="addchat"),
                InlineKeyboardButton("ᴅɪsᴀʙʟᴇ", callback_data="rmchat"),
            ]
        ]),
    )

@app.on_callback_query(filters.regex("addchat|rmchat") & ~filters.bot)
@is_admins
async def chatbot_callback(_, query: CallbackQuery):
    """Handles enabling/disabling chatbot."""
    chat_id = query.message.chat.id

    if query.data == "addchat":
        if await is_chatbot_enabled(chat_id):
            await query.edit_message_text(f"**❖ ᴄʜᴀᴛʙᴏᴛ ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ ʙʏ {query.from_user.mention}.**")  
            return
        await enable_chatbot(chat_id)
        await query.edit_message_text(f"**❖ ᴄʜᴀᴛʙᴏᴛ ᴇɴᴀʙʟᴇᴅ ʙʏ {query.from_user.mention}.**")

    elif query.data == "rmchat":
        if not await is_chatbot_enabled(chat_id):
            await query.edit_message_text(f"**❖ ᴄʜᴀᴛʙᴏᴛ ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ ʙʏ {query.from_user.mention}.**")
            return
        await disable_chatbot(chat_id)
        await query.edit_message_text(f"**❖ ᴄʜᴀᴛʙᴏᴛ ᴅɪsᴀʙʟᴇᴅ ʙʏ {query.from_user.mention}.**")

        
        
