# Credits of Plugin @ViperAdnan and @mrconfused(revert)[will add sql soon]
import html

from telethon.tl import functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import DeletePhotosRequest, UploadProfilePhotoRequest
from ... import udB
from ...config import Config
from . import (
    ALIVE_NAME,
    AUTONAME,
    BOTLOG,
    BOTLOG_CHATID,
    DEFAULT_BIO,
    edit_delete,
    get_user_from_event,
    pandaub,
)

plugin_category = "plugins"
DEFAULTUSER = str(AUTONAME) if AUTONAME else str(ALIVE_NAME)
DEFAULTUSERBIO = str(DEFAULT_BIO) if DEFAULT_BIO else ""


@pandaub.ilhammansiz_cmd(
    pattern="clone(?: |$)(.*)",
    command=("clone", plugin_category),
    info={
        "header": "To clone account of mentiond user or replied user",
        "usage": "{tr}clone <username/userid/reply>",
    },
)
async def _(event):
    eve = await edit_or_reply(event, "`Processing...`")
    reply_message = await event.get_reply_message()
    iyelatuh = await get_user_from_event(event)
    whoiam = await event.client(GetFullUserRequest(iyelatuh.id)).full_user
    if whoiam.full_user.about:
        mybio = "" + "01"
        udB.set_key(f"{mybio}", whoiam.full_user.about)  # saving bio for revert
    udB.set_key(f"{mybio}02", whoiam.users[0].first_name)
    if whoiam.users[0].last_name:
        udB.set_key(f"{mybio}03", whoiam.users[0].last_name)
    replied_user, error_i_a = await get_full_user(event)
    if replied_user is None:
        await eve.edit(str(error_i_a))
        return
    user_id = replied_user.users[0].id
    profile_pic = await event.client.download_profile_photo(user_id)
    first_name = html.escape(replied_user.users[0].first_name)
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.users[0].last_name
    if last_name is not None:
        last_name = html.escape(last_name)
        last_name = last_name.replace("\u2060", "")
    if last_name is None:
        last_name = "⁪⁬⁮⁮⁮"
    user_bio = replied_user.full_user.about
    await event.client(UpdateProfileRequest(first_name=first_name))
    await event.client(UpdateProfileRequest(last_name=last_name))
    await event.client(UpdateProfileRequest(about=user_bio))
    if profile_pic:
        pfile = await event.client.upload_file(profile_pic)
        await event.client(UploadProfilePhotoRequest(pfile))
    await eve.delete()
    await event.client.send_message(
        event.chat_id, f"**I am `{first_name}` from now...**", reply_to=reply_message
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#CLONED\nSuccesfully cloned [{first_name}](tg://user?id={user_id })",
        )


@pandaub.ilhammansiz_cmd(
    pattern="unclone$",
    command=("unclone", plugin_category),
    info={
        "header": "To revert back to your original name , bio and profile pic",
        "note": "For proper Functioning of this command you need to set AUTONAME and DEFAULT_BIO with your profile name and bio respectively.",
        "usage": "{tr}unclone",
    },
)
async def _(event):
    "To reset your original details"
    name = f"{DEFAULTUSER}"
    blank = ""
    bio = f"{DEFAULTUSERBIO}"
    await event.client(
        functions.photos.DeletePhotosRequest(
            await event.client.get_profile_photos("me", limit=1)
        )
    )
    await event.client(functions.account.UpdateProfileRequest(about=bio))
    await event.client(functions.account.UpdateProfileRequest(first_name=name))
    await event.client(functions.account.UpdateProfileRequest(last_name=blank))
    await edit_delete(event, "succesfully reverted to your account back")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, f"#REVERT\nSuccesfully reverted back to your profile"
        )

        
        
        
        
async def get_full_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.forward.sender_id
                    or previous_message.forward.channel_id
                )
            )
            return replied_user, None
        replied_user = await event.client(
            GetFullUserRequest(previous_message.sender_id)
        )
        return replied_user, None
    else:
        input_str = None
        try:
            input_str = event.pattern_match.group(1)
        except IndexError as e:
            return None, e
        if event.message.entities is not None:
            mention_entity = event.message.entities
            probable_user_mention_entity = mention_entity[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            try:
                user_object = await event.client.get_entity(input_str)
                user_id = user_object.id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e
        elif event.is_private:
            try:
                user_id = event.chat_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e
        else:
            try:
                user_object = await event.client.get_entity(int(input_str))
                user_id = user_object.id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e      
