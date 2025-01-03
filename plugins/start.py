import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, FORCE_MSG, OWNER_ID, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, START_PIC, FORCE_PIC, SHORT_MSG, AUTO_DEL, DEL_TIMER, DEL_MSG
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user, is_premium
from plugins.shorturl import get_short
from plugins.autodel import convert_time

async def delete_message(msg, delay_time):
    if AUTO_DEL.lower() == "true": 
        await asyncio.sleep(delay_time)    
        await msg.delete()

async def auto_del_notification(client, msg, delay_time):
    if AUTO_DEL.lower() == "true":  
        await msg.reply_text(DEL_MSG.format(time=convert_time(DEL_TIMER))) 
        await asyncio.sleep(delay_time)
        await msg.delete()

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    try:
        if not await present_user(user_id):
            await add_user(user_id)
    except Exception as e:
        print(f"Error adding user: {e}")

    text = message.text

    if len(text) > 7:
        try:
            basic = text.split(" ", 1)[1]
            if basic.startswith("yu3elk"):
                base64_string = basic[6:-1]
            else:
                base64_string = text.split(" ", 1)[1]

        except Exception as e:
            print(f"Error processing message: {e}")
            return

        is_user_premium = await is_premium(user_id)
        if not is_user_premium and user_id != OWNER_ID and not basic.startswith("yu3elk"):
            await short_url(client, message, base64_string)
            return

        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except Exception as e:
                print(f"Error calculating start/end: {e}")
                return
            if start <= end:
                ids = range(start, end + 1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except Exception as e:
                print(f"Error processing argument: {e}")
                return
        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except Exception as e:
            print(f"Error getting messages: {e}")
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()

        for idx, msg in enumerate(messages):
            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html,
                                                filename=msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                copied_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML,
                               reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                await asyncio.sleep(0.5)
                asyncio.create_task(delete_message(copied_msg, DEL_TIMER))
                if idx == len(messages) - 1 and AUTO_DEL:
                    last_message = copied_msg
            except FloodWait as e:
                await asyncio.sleep(e.x)
                copied_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML,
                               reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                await asyncio.sleep(0.5)
                asyncio.create_task(delete_message(copied_msg, DEL_TIMER))
                if idx == len(messages) - 1 and AUTO_DEL:
                    last_message = copied_msg

            except Exception as e:
                print(f"Error copying message: {e}")

        if AUTO_DEL and last_message:
            asyncio.create_task(auto_del_notification(client, last_message, DEL_TIMER))

        return
    else:
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("ʜᴇʟᴘ", callback_data='help'),
             InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data='about')],
            [InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data='close')]
        ])
        try:
            await message.reply_photo(
                photo=START_PIC,
                caption=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=None if not message.from_user.username else '@' + message.from_user.username,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,

            )
        except Exception as e:
            print(f"Error replying to message: {e}")
        return


#=====================================================================================##

WAIT_MSG = "<b>Working....</b>"
REPLY_ERROR = "<code>Use this command as a reply to any telegram message without any spaces.</code>"

#=====================================================================================##
async def short_url(client: Client, message: Message, base64_string):
    try:
        prem_link = f"https://t.me/{client.username}?start=yu3elk{base64_string}7"
        short_link = get_short(prem_link)

        buttons = [
            [
                InlineKeyboardButton(text="• ᴏᴘᴇɴ ʟɪɴᴋ", url=short_link),
                InlineKeyboardButton(text="ᴛᴜᴛᴏʀɪᴀʟ •", url="https://t.me/+ZLu08PF-JUIzMjFl")
            ],
            [
                InlineKeyboardButton(text="• ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ •", callback_data="premium")
            ]
        ]

        await message.reply_photo(
            photo=START_PIC,
            caption=SHORT_MSG.format(
                total_count="N/A"
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    except IndexError:
        pass


@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(text="ᴄʜᴀɴɴᴇʟ 1", url=client.invitelink1),
            InlineKeyboardButton(text="ᴄʜᴀɴɴᴇʟ 2", url=client.invitelink2)
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text='• ᴛʀʏ ᴀɢᴀɪɴ •',
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply_photo(
        photo=FORCE_PIC,
        caption=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Bot.on_message(filters.command('request') & filters.private)
async def request_command(client: Client, message: Message):
    user_id = message.from_user.id

    # Check if the user is a premium user
    if not await is_premium(user_id):
        await message.reply("You are not a premium user. Upgrade to premium to access this feature.")
        return

    # Check if the request has text
    if len(message.command) < 2:
        await message.reply("Send me your request in this format: /request your_request_here")
        return

    # Get the request text
    requested = " ".join(message.command[1:])

    # Forward the request to the owner
    owner_message = f"{message.from_user.first_name} ({message.from_user.id})\n\nRequest: {requested}"
    await client.send_message(OWNER_ID, owner_message)

    await message.reply("Thanks for your request! Your request will be reviewed soon. Please wait.")

@Bot.on_message(filters.command('my_plan') & filters.private)
async def my_plan(client: Client, message: Message):
    user_id = message.from_user.id
    is_user_premium = await is_premium(user_id)

    if is_user_premium:
        await message.reply_text("Ads : Disable\nPremium : Unlocked\n\nNice Dude you're a premium user..!")
    else:
        await message.reply_text("Ads : Enable\nPremium : Locked\n\nUnlock Premium to get more benefits\nContact - @WhiteBeard_Sama..!")

@Bot.on_message(filters.command('users') & filters.private & filters.user(OWNER_ID))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcast Processing Till Wait Dude... </i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>ʙʀᴏᴀᴅᴄᴀꜱᴛ...</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
