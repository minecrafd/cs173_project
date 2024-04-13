from bilibili_api import rank, sync, video
import asyncio
import os
import json
from bilibili_api import comment, sync, Credential, settings
from tqdm import tqdm


# settings.proxy = 'http://luowubeigui.tpddns.cn:10086'
# member_names = ["Douga", "Music", "Dance", "Game", "Knowledge", "Technology",
#                     "Sports", "Life", "Food", "Animal",
#                     "Fashion", "Ent", "Movie"]
member_names = ["All"]
credential = Credential(sessdata="38259e0c%2C1728457244%2C034de%2A42CjDLfIjnB-qE7TmXtONb8Kju2SRhy8nqBZ4A8-vAFU2P8tquaH8AqZO3L-yc2P5KUdcSVk5LcWFfZnQySFZUZ0tJRkdKYnZYelRCWEJ3QmdsV0NjZlg3UFVpTWpGb2dnemoydk00dUpIb185MTJSX09sMVlURE11MDlOZHJkWG5TZ2FKakxXTXR3IIEC", 
                        bili_jct="9ea610c9f466855e31f4ceb07d1edbaf", ac_time_value="ad2cc5aa5dc70c2aefb3b83f64c39442")

async def example():


    # 批量调用RankType中的成员
    for member_name in member_names:
        member = eval("rank.RankType." + member_name)
        result = await rank.get_rank(type_=member)
        os.makedirs(f'./data2/{member_name}', exist_ok=True)
        index = 0
        for video_item in result['list']:
            try:
                video_name = video_item['title']
                cid = video_item['cid']
                aid = video_item['aid']
                vid = video.Video(aid=aid, credential=credential)
                desc = await vid.get_info()
                desc = desc["desc"]
                subtitles = await vid.get_subtitle(cid=cid)
                hashtags = await vid.get_tags()
                comments = []
                processed_comments = []
                # 页码
                # 当前已获取数量
                count = 0
                c = await comment.get_comments(video_item['stat']['aid'], comment.CommentResourceType.VIDEO, 1, order=comment.OrderType.LIKE,
                                                credential=credential)
                for page in tqdm(range(1, min(c["page"]["count"] // 20 - 1, 26)), desc='Processing'):
                # for page in tqdm(range(1, c["page"]["count"] // 20 - 1), desc='Processing'):
                    # print(c["page"])
                    # 获取评论
                    try:
                        c = await comment.get_comments(video_item['stat']['aid'], comment.CommentResourceType.VIDEO, page, order=comment.OrderType.LIKE, credential=credential)
                    except Exception as e:
                        print(e)
                        break
                    else:
                        l = c['replies']
                        if l is None:
                            break
                        # 存储评论
                        comments.extend(l)
                        # 增加已获取数量
                        count += c['page']['size']
                        # 增加页码
                        await asyncio.sleep(0.3)
                        if count >= c['page']['count']:
                            # 当前已获取数量已达到评论总数，跳出循环
                            break

                # 处理评论
                for cmt in comments:
                    processed_comments.append({'content': cmt['content']['message'], 'like': cmt['like']})
                dic = {'title': video_name, 'stat': video_item['stat'], 'desc': desc, 'cid': cid, 'hashtag': hashtags, 'subtitles': subtitles, 'comments': processed_comments}
                with open(f'./data2/{member_name}/{index}.json', 'w', encoding='utf-8') as json_file:
                    json.dump(dic, json_file, ensure_ascii=False)
                
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except Exception as e:
                print(f"Jumping video #{index} due to {e}")
                pass

            finally:
                index += 1

async def example2():
    vid = video.Video(bvid='BV1yA4m1F7cP', credential=credential)
    result = await vid.get_info()
    # result = await vid.get_subtitle(cid=1496143412)
    print(result["desc"])
asyncio.run(example())



