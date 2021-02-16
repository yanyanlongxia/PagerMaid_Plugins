""" PagerMaid module to handle sticker collection. """

from PIL import Image
from os.path import exists
from os import remove
from requests import get
from random import randint
from struct import error as StructError
from main import bot, reg_handler, des_handler, par_handler

positions = {
    "1": [297, 288],
    "2": [85, 368],
    "3": [127, 105],
    "4": [76, 325],
    "5": [256, 160],
}
max_number = 5


def eat_it(base, mask, photo, number):
    mask_size = mask.size
    photo_size = photo.size
    if mask_size[0] < photo_size[0] and mask_size[1] < photo_size[1]:
        scale = photo_size[1] / mask_size[1]
        photo = photo.resize((int(photo_size[0] / scale), int(photo_size[1] / scale)), Image.LANCZOS)
    photo = photo.crop((0, 0, mask_size[0], mask_size[1]))
    mask1 = Image.new('RGBA', mask_size)
    mask1.paste(photo, mask=mask)
    base.paste(mask1, (positions[str(number)][0], positions[str(number)][1]), mask1)
    temp = base.size[0] if base.size[0] > base.size[1] else base.size[1]
    if temp != 512:
        scale = 512 / temp
        base = base.resize((int(base.size[0] * scale), int(base.size[1] * scale)), Image.LANCZOS)
    return base


async def eat(context, args, origin_text):
    if len(args) > 2:
        await context.edit("出错了呜呜呜 ~ 无效的参数。")
        return
    diu_round = False
    reply_message = False
    await context.edit("正在生成 吃头像 图片中 . . .")
    if context.reply_to_message:
        reply_message = context.reply_to_message
        target_user = reply_message.from_user
        if len(args) == 1:
            diu_round = True
    else:
        if len(args) == 1 or len(args) == 2:
            user = args[0].replace('@', '')
            target_user = await bot.get_users(user)
        else:
            target_user = await bot.get_me()
        if context.mentioned:
            for i in context.entities:
                if i.type == 'text_mention':
                    target_user = i.user
    try:
        photo = await bot.download_media(
            target_user.photo.big_file_id,
            "plugins/plugins/eat/" + str(target_user.id) + ".jpg"
        )
    except:
        await context.edit("此用户未设置头像或头像对您不可见。")
        return
    if exists("plugins/plugins/eat/" + str(target_user.id) + ".jpg"):
        for num in range(1, max_number + 1):
            print(num)
            if not exists('plugins/plugins/eat/eat' + str(num) + '.png'):
                re = get('https://raw.githubusercontent.com/FlowerSilent/Photo/master/photo/eat' + str(num) + '.png')
                with open('plugins/plugins/eat/eat' + str(num) + '.png', 'wb') as bg:
                    bg.write(re.content)
            if not exists('plugins/plugins/eat/mask' + str(num) + '.png'):
                re = get('https://raw.githubusercontent.com/FlowerSilent/Photo/master/photo/mask' + str(num) + '.png')
                with open('plugins/plugins/eat/mask' + str(num) + '.png', 'wb') as ms:
                    ms.write(re.content)
        number = randint(1, max_number)
        markImg = Image.open("plugins/plugins/eat/" + str(target_user.id) + ".jpg")
        eatImg = Image.open("plugins/plugins/eat/eat" + str(number) + ".png")
        maskImg = Image.open("plugins/plugins/eat/mask" + str(number) + ".png")
        if len(args) == 2:
            diu_round = True
        if diu_round:
            markImg = markImg.rotate(180)  # 对图片进行旋转
        result = eat_it(eatImg, maskImg, markImg, number)
        result.save('plugins/plugins/eat/eat.webp')
        if reply_message:
            try:
                await bot.send_document(
                    context.chat.id,
                    "plugins/plugins/eat/eat.webp",
                    reply_to_message_id=reply_message.message_id
                )
                await context.delete()
                remove("plugins/plugins/eat/eat.webp")
                try:
                    remove(photo)
                except:
                    pass
                return
            except TypeError:
                await context.edit("此用户未设置头像或头像对您不可见。")
        else:
            try:
                await bot.send_document(
                    context.chat.id,
                    "plugins/plugins/eat/eat.webp"
                )
                await context.delete()
                remove("plugins/plugins/eat/eat.webp")
                try:
                    remove(photo)
                except:
                    pass
                return
            except TypeError:
                await context.edit("此用户未设置头像或头像对您不可见。")
        try:
            remove("plugins/plugins/eat/" + str(target_user.id) + ".jpg")
            remove("plugins/plugins/eat/" + str(target_user.id) + ".png")
            remove("plugins/plugins/eat/eat.webp")
            remove(photo)
        except:
            pass
    else:
        await context.edit("此用户未设置头像或头像对您不可见。")
        return


reg_handler('eat', eat)
des_handler('eat', '生成一张 吃头像 图片，（可选：当第二个参数存在时，旋转用户头像 180°）')
par_handler('eat', '<username/uid> [随意内容]')
