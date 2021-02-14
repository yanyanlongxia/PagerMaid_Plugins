import asyncio, zipfile, os
from os.path import exists, isfile
from pyrogram import Client, filters
from main import cmd, par, des, prefix_str


time = 0


async def make_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, "w")
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)
            zipf.write(pathfile, arcname)
    zipf.close()


async def del_msg(context, t_lim):
    await asyncio.sleep(t_lim)
    try:
        await context.delete()
    except:
        pass


async def down_progress(current, total, *argv):
    global time
    size = total / 1024 / 1024
    if 1000000 * time < current:
        time += 1
        download = current / 1024 / 1024
        if 1000000 * time > total:
            download = total / 1024 / 1024
        await argv[1].edit('已下载：' + str(100 * download / size)[:5] + ' %')


async def updown_progress(current, total, *argv):
    global time
    size = total / 1024 / 1024
    if argv[1] == 'upload':
        text = '上传进度：'
    else:
        text = '下载进度：'
    if 1000000 * time < current:
        time += 1
        download = current / 1024 / 1024
        if 1000000 * time > total:
            download = total / 1024 / 1024
        await argv[0].edit(text + str(100 * download / size)[:5] + ' %')


cmd.extend(["transfer"])
par.extend(["upload <filepath>` 或 `download <filepath>"])
des.extend(["上传 / 下载文件。"])


@Client.on_message(filters.me & filters.command("transfer", list(prefix_str)))
async def transfer(bot, context):
    global time
    time = 0
    params = context.text.split(" ")[1:]
    if len(params) < 2:
        await context.edit("参数缺失")
        await del_msg(context, 3)
        return
    params[1] = " ".join(params[1:])
    file_list = params[1].split("\n")
    chat_id = context.chat.id
    if params[0] == "upload":
        index = 1
        for file_path in file_list:
            await context.edit(f"正在上传第 {index} 个文件")
            if exists(file_path):
                if isfile(file_path):
                    await bot.send_document(chat_id, file_path,
                                            progress=updown_progress, progress_args=(context,'upload'))
                else:
                    token = file_path.split("/")
                    token = token[len(token) - 1]
                    await make_zip(file_path, f"/tmp/{token}.zip")
                    await bot.send_document(chat_id, f"/tmp/{token}.zip",
                                            progress=updown_progress, progress_args=(context, 'upload'))
                    os.remove(f"/tmp/{token}.zip")
            index += 1
        await context.edit("上传完毕")
        await del_msg(context, 3)
    elif params[0] == "download":
        msg = context.reply_to_message
        if msg and msg.media:
            if not exists(file_list[0]):
                await bot.download_media(msg, file_list[0], progress=updown_progress, progress_args=(context, 'download'))
                await context.edit(f"保存成功, 保存路径 {file_list[0]}")
                await del_msg(context, 5)
            else:
                await context.edit("路径已存在文件")
                await del_msg(context, 3)
        else:
            await context.edit("未回复消息或回复消息中不包含文件")
            await del_msg(context, 3)
    else:
        await context.edit("未知命令")
        await del_msg(context, 3)
