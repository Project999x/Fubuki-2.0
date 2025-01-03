from pyrogram import Client, filters
from pyrogram.types import Message

from bot import Bot
from database.database import is_premium, remove_premium, get_premium_users, add_premium
from config import OWNER_ID

@Bot.on_message(filters.command('add_premium') & filters.user(OWNER_ID))
async def add_premium_command(client: Client, message: Message):
    if len(message.command) != 2:
        await message.reply_text("Please use the correct format: /add_premium {user_id}")
        return

    try:
        user_id = int(message.command[1])
    except ValueError:
        await message.reply_text("Invalid user ID. Please check and try again.")
        return

    # Fetch user information
    try:
        user = await client.get_users(user_id)
        user_name = user.first_name + (" " + user.last_name if user.last_name else "")
    except Exception as e:
        await message.reply_text(f"Error fetching user information: {e}")
        return

    if not await is_premium(user_id):
        await add_premium(user_id)
        await message.reply(f"User {user_name} - {user_id} has been added as a premium user.")
        # Notify the user
        try:
            await client.send_message(user_id, "Congratulations! Your premium membership has been activated...!")
        except Exception as e:
            await message.reply(f"Failed to notify the user: {e}")
    else:
        await message.reply(f"User {user_name} - {user_id} is already a premium user.")

@Bot.on_message(filters.command('remove_premium') & filters.user(OWNER_ID))
async def remove_premium_command(client: Client, message: Message):
    if len(message.command) != 2:
        await message.reply_text("Please use the correct format: /remove_premium {user_id}")
        return

    try:
        user_id = int(message.command[1])
    except ValueError:
        await message.reply_text("Invalid user ID. Please check and try again.")
        return

    # Fetch user information
    try:
        user = await client.get_users(user_id)
        user_name = user.first_name + (" " + user.last_name if user.last_name else "")
    except Exception as e:
        await message.reply_text(f"Error fetching user information: {e}")
        return

    if await is_premium(user_id):
        await remove_premium(user_id)
        await message.reply(f"User {user_name} - {user_id} has been removed from premium users.")
        # Notify the user
        try:
            await client.send_message(user_id, "Your Premium membersip has been ended contact admins to renew here - @WhiteBeard_Sama")
        except Exception as e:
            await message.reply(f"Failed to notify the user: {e}")
    else:
        await message.reply(f"User {user_name} - {user_id} is not a premium user.")

@Bot.on_message(filters.command('list_premium') & filters.user(OWNER_ID))
async def list_premium_command(client: Client, message: Message):
    premium_users = await get_premium_users()
    if not premium_users:
        await message.reply("There are no premium users.")
        return

    user_list = []
    for user_id in premium_users:
        try:
            user = await client.get_users(user_id)
            user_name = user.first_name + (" " + user.last_name if user.last_name else "")
            user_list.append(f"{user_name} - {user_id}")
        except Exception as e:
            user_list.append(f"User ID: {user_id} (Name: Could not fetch - {e})")

    user_list_text = "\n".join(user_list)
    await message.reply(f"Premium Users:\n{user_list_text}")
