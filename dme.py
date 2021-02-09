""" Module to automate message deletion. """
from asyncio import sleep
from os import path, remove, getcwd
from os.path import exists
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto
from main import cmd, par, des, prefix_str, redis
from modules.status import redis_status

cmd.extend(['dme'])
par.extend(['<数量> [文本]'])
des.extend(['编辑并删除当前对话您发送的特定数量的消息。限制：基于消息 ID 的 1000 条消息，大于 1000 条可能会触发删除消息过快限制。'
            '入群消息非管理员无法删除。（倒序）当数字足够大时即可实现删除所有消息。'])


@Client.on_message(filters.me & filters.command('dme', list(prefix_str)))
async def selfprune(client, context):
    """ Deletes specific amount of messages you sent. """
    reply = context.reply_to_message
    if reply and reply.photo:
        if exists('modules/plugins/dme.jpg'):
            remove('modules/plugins/dme.jpg')
        target_file = reply.photo
        await client.download_media(reply, file_name=f"{getcwd()}/modules/plugins/dme.jpg")
        await context.edit("替换图片设置完成。")
    elif reply and reply.sticker:
        if exists('modules/plugins/dme.jpg'):
            remove('modules/plugins/dme.jpg')
        await client.download_media(reply, file_name=f"{getcwd()}/modules/plugins/dme.webp")
        im = Image.open("modules/plugins/dme.webp")
        im.save('modules/plugins/dme.png', "png")
        remove('modules/plugins/dme.webp')
        target_file = 'modules/plugins/dme.png'
        await context.edit("替换图片设置完成。")
    elif path.isfile("modules/plugins/dme.jpg"):
        target_file = "modules/plugins/dme.jpg"
    elif path.isfile("modules/plugins/dme.png"):
        target_file = "modules/plugins/dme.png"
    else:
        target_file = False
        await context.edit("注意：没有图片进行替换。")
    try:
        count = int(context.text.split()[1]) + 1
    except ValueError:
        await context.edit("出错了呜呜呜 ~ 无效的参数。")
        return
    except IndexError:
        await context.edit("出错了呜呜呜 ~ 无效的参数。")
        return
    dme_msg = "别搁这防撤回了。。。"
    if len(context.text.split()) == 2:
        if not redis_status:
            pass
        else:
            try:
                dme_msg = redis.get("dme_msg").decode()
            except:
                pass
    elif len(context.text.split()) == 3:
        dme_msg = context.text.split()[2]
        if not redis_status():
            pass
        elif not dme_msg == str(count):
            try:
                redis.set("dme_msg", dme_msg)
            except:
                pass
    count_buffer = 0
    async for message in client.iter_history(context.chat.id):
        if message.from_user.id == context.from_user.id:
            if count_buffer == count:
                break
            if message.forward_from or message.via_bot or message.sticker or message.contact \
                    or message.poll or message.game or message.location:
                pass
            elif message.text or message.voice:
                if not message.text == dme_msg:
                    try:
                        await message.edit(dme_msg)
                    except:
                        pass
            elif message.document or message.photo or message.audio or message.video or message.gif:
                if target_file:
                    if not message.text == dme_msg:
                        await client.edit_message_media(message.chat.id, message.message_id,
                                                        InputMediaPhoto(target_file))
                        await message.edit(dme_msg)
                else:
                    if not message.text == dme_msg:
                        try:
                            await message.edit(dme_msg)
                        except:
                            pass
            else:
                pass
            await message.delete()
            count_buffer += 1
        else:
            pass
    count -= 1
    count_buffer -= 1
    notification = await send_prune_notify(client, context, count_buffer, count)
    await sleep(.5)
    await notification.delete()


async def send_prune_notify(client, context, count_buffer, count):
    return await client.send_message(
        context.chat.id,
        "删除了 "
        + str(count_buffer) + " / " + str(count)
        + " 条消息。"
    )
