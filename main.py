from bilibili_api import rank, sync
import asyncio
import os
import json
from bilibili_api import comment, sync, Credential, settings

settings.proxy = 'http://luowubeigui.tpddns.cn:10086'
member_names = ["All", "Bangumi", "GuochuangAnime", "Guochuang", "Documentary",
                    "Douga", "Music", "Dance", "Game", "Knowledge", "Technology",
                    "Sports", "Car", "Life", "Food", "Animal",
                    "Fashion", "Ent", "Cinephile", "Movie", "TV", "Variety",
                    "Original", "Rookie"]
credential = Credential(sessdata="f2c03ea3%2C1728030024%2C14374%2A41CjBTLiWN3ega4EyPm9XuY7MPP16oS5OlZbz4A4QtxiYg3LLysmNGgiF8HOujsI8sejcSVmszeFdKY19nRlNTZlVvOF9ySUhMUko2TVNwM01HLTVYTDBkMThFYVdfcTNhcGJUc2ltM3h0dHBaNjF5VWF0anNPd2ZQeU4xNUdhSzBPZGM5ZGVvOWlnIIEC", bili_jct="7fda3e6039cd86f614eedc2dd0995276", ac_time_value="f2d0889655b9dca1d826ff09414b6641")

async def example():


    # 批量调用RankType中的成员
    for member_name in member_names:
        member = eval("rank.RankType." + member_name)
        result = await rank.get_rank(type_=member)
        os.makedirs(f'./data/{member_name}', exist_ok=True)
        index = 0
        for video in result['list']:
            video_name = video['title']
            comments = []
            processed_comments = []
            # 页码
            page = 1
            # 当前已获取数量
            count = 0
            while True:
                # 获取评论
                c = await comment.get_comments(video['stat']['aid'], comment.CommentResourceType.VIDEO, page, credential=credential)
                l = c['replies']
                if l is None:
                    break
                # 存储评论
                comments.extend(l)
                # 增加已获取数量
                count += c['page']['size']
                # 增加页码
                page += 1
                await asyncio.sleep(0.5)

                if count >= c['page']['count'] - 100:
                    # 当前已获取数量已达到评论总数，跳出循环
                    break

            # 处理评论
            for cmt in comments:
                processed_comments.append({'content': cmt['content']['message'], 'like': cmt['like']})
            dic = {'title': video_name, 'stat': video['stat'], 'comments': processed_comments}
            with open(f'./data/{member_name}/{index}.json', 'w') as json_file:
                json.dump(dic, json_file)

asyncio.run(example())



