import datetime
import json
import os
import random
import re
import time
import zlib
from math import ceil
from subprocess import call, Popen, PIPE

from playwright.sync_api import sync_playwright, Browser
from tqdm import tqdm

import requests


# 把毫秒数据转化成时间字符串
def getTime(seconds):
    msec = int(seconds % 1000 / 10)
    seconds = seconds / 1000
    h = int(seconds / 60 / 60)
    m = (seconds - h * (60 * 60)) / 60
    s = (seconds - h * (60 * 60)) % 60
    return '%d:%02d:%02d.%d' % (h, m, s, msec)


def save_data_by_json(data, filePath):
    json.dump(data, open(filePath, 'w', encoding='utf8'), ensure_ascii=False, indent=2)


def read_data_by_json(filePath):
    return json.load(open(filePath, 'r', encoding='utf8'))


def judgeEXERunning(exe='IDMan'):
    pp = Popen(f'tasklist | findstr "{exe}"', stdout=PIPE, shell=True)
    pp.wait()
    out = pp.stdout.read()
    out = str(out, encoding='utf8')
    pp.kill()
    if len(out) == 0:
        return False
    return True


# --------------------------------变量定义------------------------------------
settingPath = 'setting.json'
conf = read_data_by_json(settingPath)
IDMPath = conf['path_section']['IDMPath']
nodePath = conf['path_section']['nodePath']
browserPath = conf['path_section']['browserPath']
m3u8DLPath = os.getcwd() + '\\tool\\N_m3u8DL-CLI_v3.0.2.exe'
bzJSPath = './js/ScrapeBiliDm.js'
videoListPath = './temp/list.json'

videoType = conf['video_section']['availableType']
videoUrlType = re.compile(".*(%s).*" % '|'.join(['\.' + x for x in videoType]))
jk = conf['parse_interface_section']
videoList = []

dmRow = conf['barrage_section']['barrageMaxRow']  # 弹幕行数
width = conf['barrage_section']['width']
height = conf['barrage_section']['height']
fontSize = conf['barrage_section']['fontSize']  # 弹幕字体大小
delay = conf['barrage_section']['delay']  # 弹幕移动速度为1/delay像素每毫秒
color = conf['barrage_section']['color']
assList = [f"""
[Script Info]
ScriptType: v4.00
Collisions: Normal
PlayResX: {width}
PlayResY: {height}
Timer: 100.0000


[V4 Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding

Style: Default,宋体,{fontSize},&H{color},&H00000000,&H00FFFFFF,&H00FFFFFF,-1,0,0,0,100,100,0,0,1,0,0,2,0,0,2,134

[Events]
Format: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""]
ss = f'Dialogue: Marked=0,%s,%s,Default,,0000,0000,%04d,Banner;{delay};0,%s\n'

is_scrape_dm = conf['param_section']['is_scrape_dm']
is_scrape_video = conf['param_section']['is_scrape_video']
is_headless = conf['param_section']['is_headless']
is_auto_clear_temp = conf['param_section']['is_auto_clear_temp']


def parseSelectedPart(selectedPart: str = conf['param_section']['selectedPart']):
    result = []
    if selectedPart == 'all':
        return 'all'
    else:
        for x in selectedPart.split(','):
            x = x.split('-')
            if len(x) == 1:
                result.append(int(x[0]) - 1)
            elif len(x) == 2:
                result += [x_ - 1 for x_ in range(int(x[0]), int(x[1]) + 1)]
    return result


urlDomain = {
    'tx': 'v.qq.com',
    'bz': 'www.bilibili.com',
    'aqy': 'www.iqiyi.com',
    'youtube': 'www.youtube.com'
}
#  必须的参数
downPath = conf['param_section']['downPath']
URL = conf['param_section']['url']
needList = parseSelectedPart()

TYPE = None
for x in urlDomain:
    if urlDomain[x] in URL:
        TYPE = x
if TYPE == 'youtube':
    jk = jk['youtube']
else:
    jk = jk['normal']
is_start_playwright = False
if is_scrape_video or TYPE == 'tx':
    is_start_playwright = True
p = None
browser = None
if is_start_playwright:
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=is_headless,
                                executable_path=browserPath,
                                )

hhh = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38',
}
# --------------------------------腾讯视频------------------------------------


txUrl = 'https://v.qq.com/x/cover/mzc00200iqko65a/s0041x6yrhq.html'
dmjg = 30000  # 弹幕出现时间间隔


def on_response(response):
    if re.match(videoUrlType, response.url) is not None:
        print(response.url)


# 爬取腾讯视频弹幕
def scrape_txdm(url='https://v.qq.com/x/cover/mzc00200iqko65a/y0041ulfwap.html', name=2):
    PageId = re.search('(.*)/(.*?)\.html', url).group(2)
    txdm = f'https://dm.video.qq.com/barrage/segment/{PageId}/'
    txdm_base = f'https://dm.video.qq.com/barrage/base/{PageId}'
    r = requests.get(txdm_base, headers=hhh)
    j = r.json()
    segment_index = j['segment_index']
    assList_ = assList.copy()
    for x in tqdm(segment_index):
        x = segment_index[x]
        startTime = int(x['segment_start'])
        # todo
        dms = requests.get(txdm + x['segment_name'], headers=hhh)
        time.sleep(0.5)
        if dms:
            dms = dms.json()
            dms = dms['barrage_list']
            if len(dms) == 0: continue
            listWait = [xx for xx in range(0, len(dms))]
            pre_dms = [0] * dmRow
            while len(listWait) > 0:
                jj = random.choice(listWait)
                listWait.remove(jj)
                dm = dms[jj]
                isFull = False
                for j in range(0, dmRow):
                    tempTime = pre_dms[j] + len(dm['content']) * fontSize * delay
                    if tempTime < dmjg:
                        beginTime = getTime(startTime + pre_dms[j])
                        endTime = getTime(startTime + tempTime + width * delay)
                        s = ss % (beginTime, endTime, height - (j + 1) * fontSize - 3, dm['content'])
                        assList_.append(s)
                        pre_dms[j] = tempTime + fontSize * 5 * delay
                        isFull = True
                        break
                if isFull:
                    break
        else:
            print('scrape error', txdm + x['segment_name'])
    with open(f'{downPath}\\{name}.ass', 'w', encoding='utf8') as f:
        f.writelines(assList_)
    print('爬取 %s 弹幕成功' % name)


# 爬取视频合集vid
def scrape_by_playwright_txVideoList(browser: Browser, url='https://v.qq.com/x/cover/mzc00200iqko65a/y0041ulfwap.html'):
    global videoList
    page = browser.new_page()
    page.goto(url)
    try:
        r = page.evaluate('window.__pinia')
        r = r['episodeMain']['listData']
        if len(r) > 0:
            for x in r[0]:
                videoList.append({
                    'title': x['item_params']['title'],
                    'cid': x['item_params']['cid'],
                    'url': f"https://v.qq.com/x/cover/{x['item_params']['cid']}/{x['item_params']['vid']}.html"
                })

    except Exception as e:
        print('爬取失败 %s' % url)
        print('错误原因', e)
        page.close()
        return
    print('videoList', videoList)
    page.close()
    save_data_by_json(videoList, videoListPath)
    print('爬取腾讯视频合集成功')


# ------------------------------------------B站视频----------------------------------------
def scrape_bzsp_data(url='https://www.bilibili.com/video/BV1Jv411C7H7/'):
    r = requests.get(url, headers=hhh)
    if r.status_code == 200:
        text = r.text
        rr = re.search("<script>window.__INITIAL_STATE__=(.*?);\(function\(\)\{(.*?)\}\(\)\);</script>", text)
        rrr = rr.group(1)
        j = json.loads(rrr)
        return j
    else:
        return False


# aid == pid   ,    cid == oid
bzUrl = 'https://www.bilibili.com/bangumi/play/ep276682?from_spmid=666.25.episode.0&from_outer_spmid=333.1007.top_right_bar_window_default_collection.content.click'


def scrape_bzVideoList(bzVideoData):
    if 'videoData' in bzVideoData:  # 普通视频
        aid = bzVideoData['videoData']['aid']
        for x in bzVideoData['videoData']['pages']:
            videoList.append(
                {'title': x['part'], 'url': f"https://www.bilibili.com/video/{bzVideoData['bvid']}/?p={x['page']}",
                 'cid': x['cid'], 'aid': aid})
    elif 'epList' in bzVideoData:  # 番剧
        aid = bzVideoData['epInfo']['aid']
        for x in bzVideoData['epList']:
            videoList.append(
                {'title': x['share_copy'], 'url': x['share_url'],
                 'cid': x['cid'], 'aid': aid})
    save_data_by_json(videoList, videoListPath)


def scrape_bzdm(cid, aid, name):
    p = Popen([nodePath, bzJSPath, os.getcwd() + '\\temp', str(cid), str(aid)], stdout=PIPE)
    out = p.stdout.readlines()
    if b'success' in out[0]:
        assList_ = assList.copy()
        biliPath = str(out[1], encoding='utf8').replace('\n', '')
        dms = read_data_by_json(biliPath)
        if len(dms) == 0: return
        dms = sorted(dms, key=lambda x: x['progress'])
        dmRowMax = int(height / fontSize) - 1
        pre_dms = [0] * dmRowMax
        for i in range(0, len(dms)):
            dm = dms[i]
            for j in range(0, dmRowMax):
                if pre_dms[j] < dm['progress']:
                    beginTime = getTime(dm['progress'])
                    endTime = getTime(dm['progress'] + (len(dm['content']) * fontSize + width) * delay)
                    s = ss % (beginTime, endTime, height - (j + 1) * fontSize - 3, dm['content'])
                    assList_.append(s)
                    pre_dms[j] = dm['progress'] + len(dm['content']) * fontSize * delay
                    break
        with open(f"{downPath}\\{name}.ass", 'w', encoding='utf8') as f:
            f.writelines(assList_)
        os.remove(biliPath)
        print('爬取 %s 弹幕成功' % name)
    else:
        print('爬取 %s 弹幕失败' % name)
        print(str(out[0], encoding='utf8'))
        print(str(out[1], encoding='utf8'))


# 下载字幕
if False:
    if 'subtitle' in bzVideoData:
        subtitle = bzVideoData['subtitle']
        subtitleData = []
        if subtitle['allow_submit']:
            for x in subtitle['list']:
                subtitleData.append({'name': x['lan_doc'], 'url': x['subtitle_url']})
        print(subtitleData)


def findTag(tagName, content):
    res = re.search(f'<{tagName}>(.*?)</{tagName}>', content)
    if res is not None:
        return res.group(1)
    else:
        return None


# ------------------------------------------爱奇艺一----------------------------------------
aqyUrl = 'https://www.iqiyi.com/a_sn8astnfot.html'


def scrape_aqydm(tvid: str = '8784217387413500', duration: str = '45:23', name='test'):
    res = duration.split(':')
    if len(res) == 1:
        durationSec = int(res[0])
    elif len(res) == 2:
        durationSec = int(res[0]) * 60 + int(res[1])
    elif len(res) == 3:
        durationSec = int(res[0]) * 60 * 60 + int(res[1]) * 60 + int(res[2])
    else:
        print('爬取 %s 弹幕失败' % name, '无法解析duration:' + duration)
        return
    url_format = f'https://cmts.iqiyi.com/bullet/{tvid[-4:-2]}/{tvid[-2:]}/{tvid}_300_%d.z'
    max_num = ceil(durationSec / 300)
    assList_ = assList.copy()
    for i in tqdm(range(1, max_num)):
        url = url_format % i
        rep = requests.get(url, headers=hhh)
        data = zlib.decompress(bytearray(rep.content), 15 + 32).decode('utf-8')
        bullets = re.findall('<bulletInfo>(.*?)</bulletInfo>', data, re.S)
        time.sleep(0.5)
        pre_dms = [0] * 7
        for x in bullets:
            dm = {
                'content': findTag('content', x),
                'showTime': findTag('showTime', x)
            }
            for j in range(0, 7):
                if pre_dms[j] < (int(dm['showTime']) + (i - 1) * 300) * 1000:
                    beginTime = getTime((int(dm['showTime']) + (i - 1) * 300) * 1000)
                    endTime = getTime((int(dm['showTime']) + (i - 1) * 300) * 1000 +
                                      (len(dm['content']) * fontSize + width) * delay)
                    s = ss % (beginTime, endTime, height - (j + 1) * fontSize - 3, dm['content'])
                    assList_.append(s)
                    pre_dms[j] = (int(dm['showTime']) + (i - 1) * 300) * 1000 + len(dm['content']) * fontSize * delay
                    break
    with open(f"{downPath}\\{name}.ass", 'w', encoding='utf8') as f:
        f.writelines(assList_)
    print('爬取 %s 弹幕成功' % name)


def scrape_by_playwright_aqyVideoList(browser: Browser, url=aqyUrl):
    page = browser.new_page()
    page.goto(url)
    try:
        videoListData = page.eval_on_selector('#album-avlist-data', 'e => e.value')
        videoListData = json.loads(videoListData)['epsodelist']
    except Exception:
        videoListData = [page.evaluate('window.Q.PageInfo.playPageInfo')]
    for x in videoListData:
        if x['subtitle'] != '':
            x['name'] += '：' + x['subtitle']
        videoList.append(
            {'title': x['name'],
             'url': x['playUrl'],
             'tvId': x['tvId'],
             'duration': x['duration']})
    save_data_by_json(videoList, videoListPath)


# ----------------------------------运行汇总----------------------------------
def clearDir(dir_path):
    dir = os.walk(dir_path)
    for x, y, z in dir:  # 当前主目录 当前主目录下的所有目录 当前主目录下的所有文件
        for n in z:
            os.remove(os.path.join(os.path.join(os.getcwd(), dir_path), n))


def startIDMQueue():
    Popen([f'{IDMPath}', '/s'])


def addIDMTask(url, file_name, down_path=downPath):
    if not judgeEXERunning('IDMan'):
        Popen([IDMPath])
        time.sleep(2)
    call([f'{IDMPath}', '/d', f'{url}', '/p', f'{down_path}', '/f', f'{file_name}', '/a', '/n'])


def scrape_by_playwright_net_video(browser: Browser, url='https://v.qq.com/x/cover/mzc00200iqko65a/y0041ulfwap.html',
                                   name=2):
    page = browser.new_page()
    for i, y in enumerate(jk):
        print('当前解析接口：' + y)
        jxurl = jk[y] + url
        try:
            page.goto(jxurl, timeout=15000)
        except Exception as e:
            print(e)
            print('加载页面失败 %s' % jxurl)
            continue
        d = {}
        try:
            with page.expect_response(videoUrlType) as response_info:
                response = response_info.value
                d['url'] = response.url
                d['type'] = re.search(videoUrlType, response.url).group(1)
        except Exception as e:
            print("错误原因", e)
            print('解析失败 %s' % jxurl)
            continue
        if d['type'] == '.m3u8':
            pp = call([m3u8DLPath, d['url'], '--workDir', downPath, '--saveName', name,
                       '--enableDelAfterDone', '--disableIntegrityCheck', '--retryCount', '5'])
            if pp != 0:
                print('call' + str(pp))
                continue
            print('%s 下载链接成功' % name)
            return d['type']
        else:
            # 将下载任务添加到默认队列添加到默认队列
            addIDMTask(d['url'], f"{name}{d['type']}")
            print('%s 添加下载链接成功' % name)
            return d['type']
    page.close()
    return False


def scrape_by_playwright_src_video(browser: Browser, url='https://www.youtube.com/watch?v=MU8xhYgHT0U',
                                   name='test'):
    page = browser.new_page()
    if name is None:
        page.goto(url)
        name = page.title()
    for x in jk:
        jxUrl = jk[x] + url
        try:
            page.goto(jxUrl)
            video_url = page.eval_on_selector('#videoID', 'e => e.src')
        except Exception as e:
            print('爬取视频失败 ' + url)
            print('错误原因', e)
            continue
        page.close()
        addIDMTask(video_url, name)
        print('%s 添加下载链接成功' % url)
        return True
    page.close()
    return False


def run(url=txUrl, domain='tx'):
    global videoList, needList
    if domain == 'youtube':
        scrape_by_playwright_src_video(browser, url, None)
        startIDMQueue()
        print(datetime.datetime.now(), 'IDM开启下载队列')
    else:
        if not os.path.exists(videoListPath):
            if domain == 'tx':
                scrape_by_playwright_txVideoList(browser, url)
            if domain == 'bz':
                bzVideoData = scrape_bzsp_data(bzUrl)
                scrape_bzVideoList(bzVideoData)
            if domain == 'aqy':
                scrape_by_playwright_aqyVideoList(browser, url)
        videoList = read_data_by_json(videoListPath)
        if type(needList) is str:
            needList = list(range(0, len(videoList)))
        needList_suc = needList.copy()  # 列表复制
        needList_err = needList.copy()  # 列表复制
        if is_scrape_video:
            isUsedIDM = False
            for x in tqdm(needList):
                res = scrape_by_playwright_net_video(browser, videoList[x]['url'], videoList[x]['title'])
                if res:
                    needList_err.remove(x)
                    if res != '.m3u8':
                        isUsedIDM = True
                else:
                    needList_suc.remove(x)
            if isUsedIDM:
                startIDMQueue()
                print(datetime.datetime.now(), 'IDM开启下载队列')
            if len(needList_err) > 0:
                print('下载失败:\n' + '\n'.join([videoList[x]['title'] for x in needList_err]))
                print("已为您重新设置选择集数，请重新开始")
                conf['param_section']['selectedPart'] = ','.join([str(x + 1) for x in needList_err])
                save_data_by_json(conf, settingPath)
        if is_scrape_dm:
            if domain == 'tx':
                for x in needList_suc:
                    scrape_txdm(videoList[x]['url'], videoList[x]['title'])
            if domain == 'bz':
                for x in needList_suc:
                    scrape_bzdm(videoList[x]['cid'], videoList[x]['aid'], videoList[x]['title'])
            if domain == 'aqy':
                for x in needList_suc:
                    scrape_aqydm(str(videoList[x]['tvId']), videoList[x]['duration'], videoList[x]['title'])


# ----------------------------------运行代码----------------------------------
if __name__ == '__main__':

    if TYPE is None:
        print('无法识别url：' + URL)
    else:
        run(URL, TYPE)

    if is_auto_clear_temp:
        clearDir("./temp")
        clearDir("./tool/Logs")

    if is_start_playwright:
        try:
            browser.close()
        except Exception:
            pass
