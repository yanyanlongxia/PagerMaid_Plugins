# PagerMaid_Plugins

这个 repo 用于存储 PagerMaid-Modify Beta 的插件。

## 如何上传插件？

欢迎加入 [讨论群](https://t.me/joinchat/FLV4ZFXq9nUFLLe0HDxfQQ) 探讨你的疑问。

> 开始编写 PagerMaid 插件前请确认 repo 没有对应功能的插件。

### pypi 包引入须知

额外不在 PagerMaid-Modify `requirements.txt` 下的包，请通过 `try` 来进行引入，在用户运行命令时判断包是否引入，如未引入则编辑消息提醒用户安装相应的 pypi 包。

代码参照：https://github.com/xtaodada/PagerMaid_Plugins/blob/master/sendat.py

### 调试

使用 `-apt install` 回复你的插件即可进行本地安装，请在本地测试基本无报错后进行下一步。

### 添加文件

您可以使用的文件目录为：
 - `/` 根目录放置 插件的 python 源文件
 - `/插件名/` 子目录放置 插件的资源文件（可选）

### 添加插件到库

您需要参照 `list.json` 的相关格式，在 `list` (`object`) 下 创建一个 `list`

下面是对应参数的介绍：
 - `name` : 插件名
 - `version` : 版本号
 - `section` : 分类
 - `maintainer` : 作者
 - `size` : 插件大小
 - `supported` : 插件是否允许 issue
 - `des-short` : 短介绍（用于 `-apt search`）
 - `des` : 详细介绍（用于 `-apt show`）

## Plugins 文件结构介绍

- 插件名
    - `*.*` : 插件对应的资源文件
- `插件名.py` : 插件源文件
- `version.json` : 通过 `-apt install` 命令安装的插件版本记录文件

## 目前已有的插件

- chat （聊天类）
    - `avoid` : 自动已读。
    - `dme` : 反 TG desktop 防撤回插件。
    - `vip` : vip 捐赠用户功能。
    - `keyword` : 群组关键词自动回复插件。
    - `ghs` : 搞颜色。
- profile （资料类）
    - 暂无
- daily （便民类）
    - `rate` : 汇率转换。
    - `neteasemusic` : 网易云搜歌/随机热歌/点歌。
    - `transfer` : 上传和下载文件。
