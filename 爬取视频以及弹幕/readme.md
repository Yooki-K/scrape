# 支持腾讯、B站、爱奇艺视频和弹幕下载，油管视频下载

#### 需要IDM、Node、浏览器

注：

1. IDM下载磁力链接：magnet:?xt=urn:btih:AD009A2E6B7F5E77A9B8C024CFB32F71D4E815D2&tr=http%3A%2F%2Fbt2.t-ru.org%2Fann%3Fmagnet&dn=Internet%20Download%20Manager%20v6.36%20Build%207%20Final%20%5B2020%2C%20MULTI%2FRUS%5D
2. node可以直接用playwright自带的node，如果已经下载过node，playwright可以直接使用自己安装的node，步骤如下：到python的安装路径>Lib>site-packages>playwright>driver中找到playwright.cmd，更改PLAYWRIGHT_NODEJS_PATH
3. 安装playwright默认自动安装浏览器，如果取消安装浏览器，步骤如下：到python的安装路径>Lib>site-packages>playwright>driver>package中找到browser.json,将相关installByDefault该成false即可
#### 使用方法

1. 使用设置setting.json的param_section进行参数设置

```
"path_section": {
    "IDMPath": "",
    "nodePath": "",
    "browserPath": "" 
  }
```

2. 使用设置setting.json的param_section进行参数设置

```
"downPath": "",#下载路径
   "is_scrape_dm": false,#是否下载弹幕
   "is_scrape_video": true,#是否下载视频
   "is_headless": false,#浏览器是否开启无头模式（即是否显示不浏览器）
   "is_auto_clear_temp": true,#是否自动清空缓存
   "url": "https://www.youtube.com/watch?v=MU8xhYgHT0U",#下载链接
   "selectedPart": "1"#选择内容格式 1. 如：1-3,4,5-6 2. all
```

+ v4.1
  + B站、腾讯、爱奇艺下载直接复制url，如：https://v.qq.com/x/cover/cp1qbee79qtg0w3/l0041l957r2.html 或者 https://www.bilibili.com/video/BV1Rt4y1M7Hc/ 或者 https://www.iqiyi.com/v_265kuc1ijco.html
  + 爱奇艺下载视频集需要使用电视剧首页的url  如：https://www.iqiyi.com/a_sn8astnfot.html
  + 支持youtube视频下载，仅支持单个视频下载

