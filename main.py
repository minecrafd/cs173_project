from bilibili_api import rank, sync, video
import asyncio
import os
import json
from bilibili_api import comment, sync, Credential, settings
from tqdm import tqdm


# settings.proxy = 'http://luowubeigui.tpddns.cn:10086'
member_names = ["Douga", "Music", "Dance", "Game", "Knowledge", "Technology",
                    "Sports", "Life", "Food", "Animal",
                    "Fashion", "Ent", "Movie"]
credential = Credential(sessdata="495336ff%2C1728185870%2Cea1aa%2A42CjCHi9VdJWNmUeK2WX9YoHIl-yCBjhc5rNACQvqMG7YVCMeNpCjGoPAf-08hGEmmMEESVm1nNmw1NHdpQ3I4ZldaTWRjbXBNRmI1WVFyVUdmRkxiYjBtdE9xTG5QUFRWUnZXQ1lSamxjRngzOUdKQzdyRWJIR19qalNqYmc5dnFzbmFhVkVCYmFRIIEC", 
                        bili_jct="216a9cb665e2838ad16414b45599f602", ac_time_value="5a0c0f6f28cc4d1717606d8108b33342")

async def example():


    # 批量调用RankType中的成员
    for member_name in member_names:
        member = eval("rank.RankType." + member_name)
        result = await rank.get_rank(type_=member)
        os.makedirs(f'./data/{member_name}', exist_ok=True)
        index = 0
        for video_item in result['list']:
            try:
                video_name = video_item['title']
                cid = video_item['cid']
                aid = video_item['aid']
                vid = video.Video(aid=aid, credential=credential)
                subtitles = await vid.get_subtitle(cid=cid)
                hashtags = await vid.get_tags()
                comments = []
                processed_comments = []
                # 页码
                # 当前已获取数量
                count = 0
                c = await comment.get_comments(video_item['stat']['aid'], comment.CommentResourceType.VIDEO, 1,
                                                credential=credential)
                for page in tqdm(range(1, min(c["page"]["count"] // 20 - 1, 26)), desc='Processing'):
                    # 获取评论
                    c = await comment.get_comments(video_item['stat']['aid'], comment.CommentResourceType.VIDEO, page, credential=credential)
                    l = c['replies']
                    if l is None:
                        break
                    # 存储评论
                    comments.extend(l)
                    # 增加已获取数量
                    count += c['page']['size']
                    # 增加页码
                    await asyncio.sleep(0.3)
                    if count >= c['page']['count'] - 20:
                        # 当前已获取数量已达到评论总数，跳出循环
                        break

                # 处理评论
                for cmt in comments:
                    processed_comments.append({'content': cmt['content']['message'], 'like': cmt['like']})
                dic = {'title': video_name, 'stat': video_item['stat'], 'comments': processed_comments, 'cid': cid, 'hashtag': hashtags, 'subtitles': subtitles}
                with open(f'./data/{member_name}/{index}.json', 'w', encoding='utf-8') as json_file:
                    json.dump(dic, json_file, ensure_ascii=False)
                
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except Exception as e:
                print(f"Jumping video #{index} due to {e}")
                pass

            finally:
                index += 1

async def example2():
    vid = video.Video(bvid='BV1BH4y1n7Mn', credential=credential)
    result = await vid.get_info()
    result = await vid.get_subtitle(cid=1496143412)
    print(result)
asyncio.run(example())



