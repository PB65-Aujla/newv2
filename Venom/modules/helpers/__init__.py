from typing import Callable

from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message

from Venom import OWNER, VenomX


def is_admins(func: Callable) -> Callable:
    async def non_admin(c: VenomX, m: Message):
        if m.from_user.id == OWNER:
            return await func(c, m)

        admin = await c.get_chat_member(m.chat.id, m.from_user.id)
        if admin.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            return await func(c, m)

    return non_admin


from .inline import *
from .read import *



#GIMNI
from motor.motor_asyncio import AsyncIOMotorClient
import config

# Database connection
ChatBot = AsyncIOMotorClient(config.MONGO_URL)
db = ChatBot["ChatBot"]  # Database
usersdb = db["users"]    # Users Collection
chatsdb = db["chats"]    # Chats Collection

# Import functions for use in other parts of the application
from .admin import *
from .shizu import *
from .chatbot import *
