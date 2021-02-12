""" Pagermaid xtao-some plugin base. """
import json, requests
from urllib.parse import urlparse
from modules.system import attach_log
from pyrogram import Client, filters
from main import cmd, par, des, prefix_str

cmd.extend(["guess"])
par.extend(["upload <filepath>` 或 `download <filepath>"])
des.extend(["能不能好好说话？ - 拼音首字母缩写释义工具（需要回复一句话）"])


@Client.on_message(filters.me & filters.command("guess", list(prefix_str)))
async def guess(bot, context):
    reply = context.reply_to_message
    await context.edit("获取中 . . .")
    if not reply:
        context.edit("宁需要回复一句话")
        return True
    text = {'text': str(reply.text.replace("/guess ", ""))}
    guess_json = json.loads(
        requests.post("https://lab.magiconch.com/api/nbnhhsh/guess", data=text, verify=False).content.decode("utf-8"))
    guess_res = []
    if not len(guess_json) == 0:
        for num in range(0, len(guess_json)):
            guess_res1 = json.loads(json.dumps(guess_json[num]))
            guess_res1_name = guess_res1['name']
            try:
                guess_res1_ans = ", ".join(guess_res1['trans'])
            except:
                try:
                    guess_res1_ans = ", ".join(guess_res1['inputting'])
                except:
                    guess_res1_ans = "尚未录入"
            guess_res.extend(["词组：" + guess_res1_name + "\n释义：" + guess_res1_ans])
        await context.edit("\n\n".join(guess_res))
    else:
        await context.edit("没有匹配到拼音首字母缩写")


cmd.extend(["wiki"])
par.extend(["<词组>"])
des.extend(["查询维基百科词条。"])


@Client.on_message(filters.me & filters.command("wiki", list(prefix_str)))
async def wiki(bot, context):
    lang = 'zh'
    await context.edit("获取中 . . .")
    try:
        message = context.text.split()[1]
    except ValueError:
        await context.edit("出错了呜呜呜 ~ 无效的参数。")
        return
    try:
        wiki_json = json.loads(requests.get("https://zh.wikipedia.org/w/api.php?action=query&list=search&format=json"
                                            "&formatversion=2&srsearch=" + message).content.decode(
            "utf-8"))
    except:
        await context.edit("出错了呜呜呜 ~ 无法访问到维基百科。")
        return
    if not len(wiki_json['query']['search']) == 0:
        wiki_title = wiki_json['query']['search'][0]['title']
        wiki_content = wiki_json['query']['search'][0]['snippet'].replace('<span class=\"searchmatch\">', '**').replace(
            '</span>', '**')
        wiki_time = wiki_json['query']['search'][0]['timestamp'].replace('T', ' ').replace('Z', ' ')
        await context.edit("正在生成翻译中 . . .")
        USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
        headers = {"user-agent": USER_AGENT}
        wiki_content = json.loads(requests.get("https://xtaolink.cn/git/m/t.php?lang=" + lang + '&text=' +
                                               wiki_content, headers=headers)
                                  .content.decode("utf-8"))['data']['target_text']
        message = '词条： [' + wiki_title + '](https://zh.wikipedia.org/zh-cn/' + wiki_title + ')\n\n' + \
                  wiki_content + '...\n\n此词条最后修订于 ' + wiki_time
        await context.edit(message)
    else:
        await context.edit("没有匹配到相关词条")


cmd.extend(["ip"])
par.extend(["<ip/域名>"])
des.extend(["IPINFO （或者回复一句话）。"])


@Client.on_message(filters.me & filters.command("ip", list(prefix_str)))
async def ipinfo(bot, context):
    reply = context.reply_to_message
    await context.edit('正在查询中...')
    try:
        if reply:
            text = request_ip(reply.entities)
        else:
            text = request_ip(context.entities)
        await context.edit(text)
    except:
        await context.edit('没有找到要查询的 ip/域名 ...')


cmd.extend(["ipping"])
par.extend(["<ip/域名>"])
des.extend(["Ping （或者回复一句话）。"])


@Client.on_message(filters.me & filters.command("ipping", list(prefix_str)))
async def ipping(bot, context):
    reply = context.reply_to_message
    await context.edit('正在查询中...')
    try:
        if reply:
            pinginfo = get_ipping(reply.entities)
            await context.edit(pinginfo)
            return True
        else:
            pinginfo = get_ipping(context.entities)
            await context.edit(pinginfo)
            return True
    except:
        await context.edit('没有找到要查询的 ip/域名 ...')


cmd.extend(["t"])
par.extend(["<文本>"])
des.extend(["通过腾讯AI开放平台将目标消息翻译成中文。"])


@Client.on_message(filters.me & filters.command("t", list(prefix_str)))
async def tx_t(bot, context):
    """ PagerMaid universal translator. """
    reply = context.reply_to_message
    message = context.split()
    lang = 'zh'
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent": USER_AGENT}
    if not len(message) == 1:
        pass
    elif reply:
        message = reply.text
    else:
        await context.edit("出错了呜呜呜 ~ 无效的参数。")
        return

    await context.edit("正在生成翻译中 . . .")
    tx_json = json.loads(requests.get(
        "https://xtaolink.cn/git/m/t.php?lang=" + lang + '&text=' + message,
        headers=headers).content.decode(
        "utf-8"))
    if not tx_json['msg'] == 'ok':
        context.edit("出错了呜呜呜 ~ 翻译出错")
        return True
    else:
        result = '文本翻译：\n' + 'zh-cn'

    if len(result) > 4096:
        await context.edit("输出超出 TG 限制，正在尝试上传文件。")
        await attach_log(bot, result, context.chat.id, "translation.txt", context.message_id)
        return
    await context.edit(result)


async def request_ip(entities):
    url = False
    if not len(entities) == 0:
        for i in entities:
            if i.type == 'text_link':
                url = i.url
                url = urlparse(url)
                if url.hostname:
                    url = url.hostname
                else:
                    url = url.path
    if url:
        ipinfo_json = json.loads(requests.get(
            "http://ip-api.com/json/" + url + "?fields=status,message,country,regionName,city,lat,lon,isp,"
                                              "org,as,mobile,proxy,hosting,query").content.decode(
            "utf-8"))
        if ipinfo_json['status'] == 'fail':
            return '没有找到要查询的 ip/域名 ...'
        elif ipinfo_json['status'] == 'success':
            ipinfo_list = []
            ipinfo_list.extend(["查询目标： `" + url + "`"])
            if ipinfo_json['query'] == url:
                pass
            else:
                ipinfo_list.extend(["解析地址： `" + ipinfo_json['query'] + "`"])
            ipinfo_list.extend(["地区： `" + ipinfo_json['country'] + ' - ' + ipinfo_json['regionName'] + ' - ' +
                                ipinfo_json['city'] + "`"])
            ipinfo_list.extend(["经纬度： `" + str(ipinfo_json['lat']) + ',' + str(ipinfo_json['lon']) + "`"])
            ipinfo_list.extend(["ISP： `" + ipinfo_json['isp'] + "`"])
            if not ipinfo_json['org'] == '':
                ipinfo_list.extend(["组织： `" + ipinfo_json['org'] + "`"])
            try:
                ipinfo_list.extend(
                    ['[' + ipinfo_json['as'] + '](https://bgp.he.net/' + ipinfo_json['as'].split()[0] + ')'])
            except:
                pass
            if ipinfo_json['mobile']:
                ipinfo_list.extend(['此 IP 可能为**蜂窝移动数据 IP**'])
            if ipinfo_json['proxy']:
                ipinfo_list.extend(['此 IP 可能为**代理 IP**'])
            if ipinfo_json['hosting']:
                ipinfo_list.extend(['此 IP 可能为**数据中心 IP**'])
            return '\n'.join(ipinfo_list)
    else:
        return '没有找到要查询的 ip/域名 ...'


async def get_ipping(entities):
    if not len(entities) == 0:
        for i in entities:
            if i.type == 'text_link':
                url = i.url
                url = urlparse(url)
                if url.hostname:
                    url = url.hostname
                else:
                    url = url.path
                pinginfo = requests.get(
                    "https://steakovercooked.com/api/ping/?host=" + url).content.decode("utf-8")
                if pinginfo == 'null':
                    return '没有找到要查询的 ip/域名 ...'
                elif not pinginfo == 'null':
                    pinginfo = pinginfo.replace('"', '').replace("\/", '/').replace('\\n', '\n', 7).replace(
                        '\\n', '')
                return pinginfo
