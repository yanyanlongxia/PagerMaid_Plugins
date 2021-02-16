""" PagerMaid module to handle sticker collection. """

from PIL import Image, ImageDraw, ImageFilter
from os.path import exists
from os import remove
from requests import get
from random import randint
from struct import error as StructError
from main import bot, reg_handler, des_handler, par_handler


def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def mask_circle_transparent(pil_img, blur_radius, offset=0):
    offset = blur_radius * 2 + offset
    mask = Image.new("L", pil_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

    result = pil_img.copy()
    result.putalpha(mask)
    return result


async def throwit(context, args, origin_text):
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
            "plugins/plugins/diu/" + str(target_user.id) + ".jpg"
        )
    except:
        await context.edit("此用户未设置头像或头像对您不可见。")
        return
    if exists("plugins/plugins/diu/" + str(target_user.id) + ".jpg"):
        if not exists('plugins/plugins/diu/1.png'):
            r = get('https://raw.githubusercontent.com/xtaodada/PagerMaid_Plugins/beta/diu/1.png')
            with open("plugins/plugins/diu/1.png", "wb") as code:
                code.write(r.content)
        if not exists('plugins/plugins/diu/2.png'):
            r = get('https://raw.githubusercontent.com/xtaodada/PagerMaid_Plugins/beta/diu/2.png')
            with open("plugins/plugins/diu/2.png", "wb") as code:
                code.write(r.content)
        if not exists('plugins/plugins/diu/3.png'):
            r = get('https://raw.githubusercontent.com/xtaodada/PagerMaid_Plugins/beta/diu/3.png')
            with open("plugins/plugins/diu/3.png", "wb") as code:
                code.write(r.content)
        # 随机数生成
        randint_r = randint(1, 3)
        # 将头像转为圆形
        markImg = Image.open("plugins/plugins/diu/" + str(target_user.id) + ".jpg")
        if randint_r == 1:
            thumb_width = 136
        elif randint_r == 2:
            thumb_width = 122
        elif randint_r == 3:
            thumb_width = 180
        im_square = crop_max_square(markImg).resize((thumb_width, thumb_width), Image.LANCZOS)
        im_thumb = mask_circle_transparent(im_square, 0)
        im_thumb.save("plugins/plugins/diu/" + str(target_user.id) + ".png")
        # 将头像复制到模板上
        if randint_r == 1:
            background = Image.open("plugins/plugins/diu/2.png")
        elif randint_r == 2:
            background = Image.open("plugins/plugins/diu/1.png")
        elif randint_r == 3:
            background = Image.open("plugins/plugins/diu/3.png")
        foreground = Image.open("plugins/plugins/diu/" + str(target_user.id) + ".png")
        if len(args) == 2:
            diu_round = True
        if diu_round:
            foreground = foreground.rotate(180)  # 对图片进行旋转
        if randint_r == 1:
            background.paste(foreground, (19, 181), foreground)
        elif randint_r == 2:
            background.paste(foreground, (368, 16), foreground)
        elif randint_r == 3:
            background.paste(foreground, (331, 281), foreground)
        background.save('plugins/plugins/diu/throwout.webp')
        if reply_message:
            try:
                await bot.send_document(
                    context.chat.id,
                    "plugins/plugins/diu/throwout.webp",
                    reply_to_message_id=reply_message.message_id
                )
                await context.delete()
                remove("plugins/plugins/diu/throwout.webp")
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
                    "plugins/plugins/diu/throwout.webp"
                )
                await context.delete()
                remove("plugins/plugins/diu/throwout.webp")
                try:
                    remove(photo)
                except:
                    pass
                return
            except TypeError:
                await context.edit("此用户未设置头像或头像对您不可见。")
        try:
            remove("plugins/plugins/diu/" + str(target_user.id) + ".jpg")
            remove("plugins/plugins/diu/" + str(target_user.id) + ".png")
            remove("plugins/plugins/diu/throwout.webp")
            remove(photo)
        except:
            pass
    else:
        await context.edit("此用户未设置头像或头像对您不可见。")
        return


reg_handler('diu', throwit)
des_handler('diu', '生成一张 扔头像 图片，（可选：当第二个参数存在时，旋转用户头像 180°）')
par_handler('diu', '<username/uid> [随意内容]')
