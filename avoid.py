""" PagerMaid module for different ways to avoid users. """

from main import bot, reg_handler, des_handler, par_handler, redis
from plugins.status import redis_status


async def ghost(message, args, origin_text):
    """ Toggles ghosting of a user. """
    if not redis_status():
        await message.edit("出错了呜呜呜 ~ Redis 好像离线了，无法执行命令。")
        return
    if len(message.text.split()) != 2:
        await message.edit("出错了呜呜呜 ~ 无效的参数。")
        return
    myself = await bot.get_me()
    self_user_id = myself.id
    if message.text.split()[1] == "true":
        if message.chat.id == self_user_id:
            await message.edit("在？为什么要在收藏夹里面用？")
            return
        redis.set("ghosted.chat_id." + str(message.chat.id), "true")
        await message.delete()
    elif message.text.split()[1] == "false":
        if message.chat.id == self_user_id:
            await message.edit("在？为什么要在收藏夹里面用？")
            return
        try:
            redis.delete("ghosted.chat_id." + str(message.chat.id))
        except:
            await message.edit("emm...当前对话不存在于自动已读对话列表中。")
            return
        await message.delete()
    elif message.text.split()[1] == "status":
        if redis.get("ghosted.chat_id." + str(message.chat.id)):
            await message.edit("emm...当前对话存在于自动已读对话列表中。")
        else:
            await message.edit("emm...当前对话不存在于自动已读对话列表中。")
    else:
        await message.edit("出错了呜呜呜 ~ 无效的参数。")


async def deny(message, args, origin_text):
    """ Toggles denying of a user. """
    if not redis_status():
        await message.edit("出错了呜呜呜 ~ Redis 离线，无法运行。")
        return
    if len(message.text.split()) != 2:
        await message.edit("出错了呜呜呜 ~ 无效的参数。")
        return
    myself = await bot.get_me()
    self_user_id = myself.id
    if message.text.split()[1] == "true":
        if message.chat.id == self_user_id:
            await message.edit("在？为什么要在收藏夹里面用？")
            return
        redis.set("denied.chat_id." + str(message.chat.id), "true")
        await message.delete()
    elif message.text.split()[1] == "false":
        if message.chat.id == self_user_id:
            await message.edit("在？为什么要在收藏夹里面用？")
            return
        redis.delete("denied.chat_id." + str(message.chat.id))
        await message.delete()
    elif message.text.split()[1] == "status":
        if redis.get("denied.chat_id." + str(message.chat.id)):
            await message.edit("emm...当前对话已被加入自动拒绝对话列表中。")
        else:
            await message.edit("emm...当前对话已从自动拒绝对话列表移除。")
    else:
        await message.edit("出错了呜呜呜 ~ 无效的参数。")


reg_handler('ghost', ghost)
reg_handler('deny', deny)
des_handler('ghost', "开启对话的自动已读，需要 Redis。")
des_handler('deny', '拒绝聊天功能，需要 Redis。')
par_handler('ghost', '<true|false|status>')
par_handler('deny', '<true|false|status>')
