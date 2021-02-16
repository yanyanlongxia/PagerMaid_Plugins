import random
from requests import get
from os import remove
from main import bot, reg_handler, des_handler, par_handler


async def ghs(context, args, origin_text):
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
                await bot.send_photo(context.chat.id, filename, caption="#NSFW ⚠️色图警告⚠️")
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
        await bot.send_message(context.chat.id, "出错了呜呜呜 ~ 试了好多好多次都无法访问到服务器（没有颜色搞啦！） 。")


reg_handler('ghs', ghs)
des_handler('ghs', '随机获取涩情写真')
par_handler('ghs', '')
