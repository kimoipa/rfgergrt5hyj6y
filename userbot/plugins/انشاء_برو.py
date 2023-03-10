from telethon.tl import functions

from .. import catub
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..utils.tools import create_supergroup

plugin_category = "tools"


@catub.cat_cmd(
    pattern="انشاء (b|g|c) ([\s\S]*)",
    command=("انشاء", plugin_category),
    info={
        "header": "To create a private group/channel with userbot.",
        "description": "Use this cmd to create super group , normal group or channel.",
        "flags": {
            "b": "to create a private super group",
            "g": "To create a private basic group.",
            "c": "to create a private channel",
        },
        "usage": "{tr}create (b|g|c) <name of group/channel>",
        "examples": "{tr}create b catuserbot",
    },
)
async def _(event):
    "To create a private group/channel with userbot"
    type_of_group = event.pattern_match.group(1)
    group_name = event.pattern_match.group(2)
    if type_of_group == "c":
        descript = "This is a Test Channel created using catuserbot"
    else:
        descript = "This is a Test Group created using catuserbot"
    if type_of_group == "g":
        try:
            result = await event.client(
                functions.messages.CreateChatRequest(
                    users=[Config.TG_BOT_USERNAME],
                    # Not enough users (to create a chat, for example)
                    # Telegram, no longer allows creating a chat with ourselves
                    title=group_name,
                )
            )
            created_chat_id = result.chats[0].id
            result = await event.client(
                functions.messages.ExportChatInviteRequest(
                    peer=created_chat_id,
                )
            )
            await edit_or_reply(
                event, f"المجموعة `{group_name}` أنشئت بنجاح. دخول المجموعة {result.link}"
            )
        except Exception as e:
            await edit_delete(event, f"**خطأ:**\n{str(e)}")
    elif type_of_group == "c":
        try:
            r = await event.client(
                functions.channels.CreateChannelRequest(
                    title=group_name,
                    about=descript,
                    megagroup=False,
                )
            )
            created_chat_id = r.chats[0].id
            result = await event.client(
                functions.messages.ExportChatInviteRequest(
                    peer=created_chat_id,
                )
            )
            await edit_or_reply(
                event,
                f"القناة `{group_name}` أنشئت بنجاح. دخول القناة {result.link}",
            )
        except Exception as e:
            await edit_delete(event, f"**خطأ:**\n{str(e)}")
    elif type_of_group == "b":
        answer = await create_supergroup(
            group_name, event.client, Config.TG_BOT_USERNAME, descript
        )
        if answer[0] != "error":
            await edit_or_reply(
                event,
                f"المجموعة `{group_name}` أنشئت بنجاح. دخول المجموعة {answer[0].link}",
            )
        else:
            await edit_delete(event, f"**خطأ:**\n{str(answer[1])}")
    else:
        await edit_delete(event, "ارسل الأمر `.مساعدة انشاء` لمعرفة كيفية الاستخدام")
