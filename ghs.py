import random
from time import sleep
from requests import get
from os import remove
from pyrogram import Client, filters
from main import cmd, par, des, prefix_str

cmd.extend(['ghs'])
par.extend([''])
des.extend(['随机获取涩情写真'])


@Client.on_message(filters.me & filters.command('ghs', list(prefix_str)))
async def ghs(client, context):
    await context.edit("搞颜色中 . . .")
    status = False
    for _ in range(20):  # 最多重试20次
        website = random.randint(0, 0)
        filename = "ghs" + str(random.random())[2:] + ".png"
        try:
            if website == 0:
                img = get("https://se.jiba.xyz/api.php")
            if img.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(img.content)
                await context.edit("传颜色中 . . .")
                await client.send_photo(context.chat.id, filename, caption="#NSFW ⚠️色图警告⚠️")
                status = True
                break  # 成功了就赶紧结束啦！
        except:
            try:
                remove(filename)
            except:
                pass
            continue
    try:
        remove(filename)
    except:
        pass
    try:
        await context.delete()
    except:
        pass
    if not status:
        await client.send_message(context.chat.id, "出错了呜呜呜 ~ 试了好多好多次都无法访问到服务器（没有颜色搞啦！） 。")
