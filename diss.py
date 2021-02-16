from asyncio import sleep
from requests import get
from main import bot, reg_handler, des_handler, par_handler


async def diss(message, args, origin_text):
    await message.edit("获取中 . . .")
    status = False
    for _ in range(20):
        req = get("https://nmsl.shadiao.app/api.php?level=min&from=tntcrafthim")
        if req.status_code == 200:
            res = req.text
            await message.edit(res, parse_mode='html')
            status = True
            break
        else:
            continue
    if status == False:
        await message.edit("出错了呜呜呜 ~ 试了好多好多次都无法访问到 API 服务器 。")
        await sleep(2)
        await message.delete()


async def biss(message, args, origin_text):
    await message.edit("获取中 . . .")
    status = False
    for _ in range(20):
        req = get("https://nmsl.shadiao.app/api.php?from=tntcrafthim")
        if req.status_code == 200:
            res = req.text
            await message.edit(res, parse_mode='html')
            status = True
            break
        else:
            continue
    if status == False:
        await message.edit("出错了呜呜呜 ~ 试了好多好多次都无法访问到 API 服务器 。")
        await sleep(2)
        await message.delete()


reg_handler('diss', diss)
reg_handler('biss', biss)
des_handler('diss', "儒雅随和版祖安语录。")
des_handler('diss', '加带力度版祖安语录。')
par_handler('diss', '')
par_handler('biss', '')
