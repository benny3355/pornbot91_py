import asyncio
import datetime
import os
import random
import re
import shutil

import aiohttp
import ffmpy3
import jieba

# 分词
from tenacity import retry, stop_after_attempt, wait_fixed


async def seg(str):
    try:
        jieba.load_userdict("/config/word.txt")
        jieba.set_dictionary("/config/dict.txt")
    except:
        print('自定应词典不存在')
    seg_list = jieba.cut(str, cut_all=False)
    return '#' + " #".join(seg_list)




@retry(stop=stop_after_attempt(4), wait=wait_fixed(10))
async def imgCover(input, output):
    # ffmpeg -i 001.jpg -vf 'scale=320:320'  001_1.jpg
    ff = ffmpy3.FFmpeg(
        inputs={input: None},
        outputs={output: '-y'}
    )
    await ff.run_async()
    await ff.wait()


async def genIpaddr():
    m = random.randint(0, 255)
    n = random.randint(0, 255)
    x = random.randint(0, 255)
    y = random.randint(0, 255)
    return str(m) + '.' + str(n) + '.' + str(x) + '.' + str(y)


# 下载任务
@retry(stop=stop_after_attempt(4), wait=wait_fixed(10))
async def run(url, viewkey):
    if '.mp4' in url:
        os.makedirs(viewkey)
        filename = viewkey + '.mp4'
    else:
        filename = re.search('([a-zA-Z0-9-_]+.ts)', url).group(1).strip()

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            with open(viewkey + '/' + filename, "wb") as fp:
                while True:
                    chunk = await r.content.read(64 * 1024)
                    if not chunk:
                        break
                    fp.write(chunk)
                print("\r", '任务文件 ', filename, ' 下载成功', end="", flush=True)

    # print("\r", '任务文件 ', filename, ' 下载成功', end="", flush=True)


# 读出ts列表，并写入文件列表到文件，方便后面合并视频
async def down(url, viewkey):
    async with aiohttp.request("GET", url) as r:
        m3u8_text = await r.text()
        base_url = re.split(r"[a-zA-Z0-9-_\.]+\.m3u8", url)[0]
        lines = m3u8_text.split('\n')
        s = len(lines)
        ts_list = list()
        concatfile = viewkey + '/' + viewkey + '.txt'
        if not os.path.isdir(viewkey):
            # 尝试删除目录先
            try:
                shutil.rmtree(viewkey)
            except:
                pass
            os.makedirs(viewkey)
        open(concatfile, 'w').close()
        t = open(concatfile, mode='a')
        for i, line in enumerate(lines):
            if '.ts' in line:
                if 'http' in line:
                    # print("ts>>", line)
                    ts_list.append(line)
                else:
                    line = base_url + line
                    ts_list.append(line)
                    # print('ts>>',line)
                filename = re.search('([a-zA-Z0-9-_]+.ts)', line).group(1).strip()
                t.write("file %s\n" % filename)
                print("\r", '文件写入中', i, "/", s - 3, end="", flush=True)
        print(ts_list)
        return ts_list, concatfile


# 视频合并方法，使用ffmpeg
def merge(concatfile, viewkey):
    try:
        path = viewkey + '/' + viewkey + '.mp4'
        # command = 'ffmpeg -y -f concat -i %s -crf 18 -ar 48000 -vcodec libx264 -c:a aac -r 25 -g 25 -keyint_min 25 -strict -2 %s' % (concatfile, path)
        command = 'ffmpeg -y -f concat -i %s -bsf:a aac_adtstoasc -c copy %s' % (concatfile, path)
        os.system(command)
        print('视频合并完成')
    except:
        print('合并失败')


async def download91(url, viewkey):
    start = datetime.datetime.now().replace(microsecond=0)
    ts_list, concatfile = await down(url, viewkey)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = []
    for url in ts_list:
        tasks.append(run(url, viewkey))

    await asyncio.wait(tasks)
    merge(concatfile, viewkey)
    end = datetime.datetime.now().replace(microsecond=0)
    print('写文件及下载耗时：' + str(end - start))



