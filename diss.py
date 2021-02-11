from asyncio import sleep
from requests import get
from pyrogram import Client, filters
from main import cmd, par, des, prefix_str

cmd.extend(["diss", "biss"])
par.extend(["", ""])
des.extend(["儒雅随和版祖安语录。", "加带力度版祖安语录。"])

@Client.on_message(filters.me & filters.command("diss", list(prefix_str)))
async def diss(clinet, message):
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

@Client.on_message(filters.me & filters.command("biss", list(prefix_str)))
async def biss(client, message):
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