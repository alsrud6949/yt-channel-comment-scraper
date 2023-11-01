from pathlib import Path
from init import youtube
import pandas as pd

def get_recent_videos(channel_id, startdate):
    result = []
    try:
        nextPageToken = ''
        while (nextPageToken is not None):
            response = youtube.search().list(part='snippet,id',
                                        channelId=channel_id,
                                        maxResults=50,
                                        order='date',
                                        publishedAfter=f'{startdate}T00:00:00Z',
                                        pageToken=nextPageToken).execute()
            # make response to dictionaries
            items = response.get('items')
            for item in items:
                result_dict = {'videoId': item.get('id').get('videoId')}
                snippet = item.get('snippet')
                result_dict.update(snippet)
                result_dict['thumbnails'] = result_dict['thumbnails'].get('default').get('url')
                del result_dict['publishTime']
                result.append(result_dict)
            try:
                nextPageToken = response['nextPageToken']
            except:
                nextPageToken = None
    except:
        pass
    all_df = pd.DataFrame(result)
    return all_df

def get_video_stats(video_list):
    response = youtube.videos().list(part='statistics',
                                     id=','.join(video_list)).execute()
    result = []
    items = response.get('items')
    for item in items:
        result_dict = {'videoId': item.get('id')}
        statistics = item.get('statistics')
        result_dict.update(statistics)
        result.append(result_dict)

    return result

def get_channel_stats(channel_id):
    response = youtube.channels().list(part='statistics',
                                       id=channel_id).execute()
    statistics = response.get('items')[0].get('statistics')
    return statistics

def make_comment_df(data):
    result = []
    for item in data:
        result_dict = {'commentId': item.get('id')}
        snippet = item.get('snippet')
        replies = item.get('replies')
        comment_snippet = snippet.pop('topLevelComment').get('snippet')
        result_dict.update(snippet)
        result_dict.update(comment_snippet)
        result_dict['authorChannelId'] = result_dict['authorChannelId'].get('value')
        result.append(result_dict)
        if replies != None:
            reply_comment = replies.get('comments')
            for reply in reply_comment:
                result_dict = {'reply':True, 'commentId': reply.get('id')}
                reply_snippet = reply.get('snippet')
                result_dict.update(reply_snippet)
                result_dict['authorChannelId'] = result_dict['authorChannelId'].get('value')
                result.append(result_dict)
    return pd.DataFrame(result)

def get_comments(video_id):
    all_df = pd.DataFrame()
    print(f"The comments of {video_id} are being crawled.")
    try:
        nextPageToken = ''
        while (nextPageToken is not None):

            response = youtube.commentThreads().list(part='id,replies,snippet',
                                                videoId=video_id,
                                                maxResults=100, pageToken=nextPageToken).execute()
            items = response.get('items')
            comment_df = make_comment_df(items)
            all_df = pd.concat([all_df, comment_df])
            try:
                nextPageToken = response['nextPageToken']
            except:
                nextPageToken = None
    except:
        pass
    return all_df

def main(channel_id, startdate):
    recent_videos = get_recent_videos(channel_id,startdate)
    video_ids = recent_videos['videoId'].unique()
    video_ids_list_of_list = [
        video_ids[i: i + 50] for i in range(0, len(video_ids), 50)
    ]
    video_data_list_of_list = [get_video_stats(video_ids_list) for video_ids_list in video_ids_list_of_list]
    video_data = [item for video_data_list in video_data_list_of_list for item in video_data_list]
    video_df = pd.DataFrame(video_data)
    channel_stats = get_channel_stats(channel_id)
    for key, value in channel_stats.items():
        recent_videos[key] = value
    recent_videos.rename(columns={'viewCount': 'totalviewCount'}, inplace=True)
    result_df = pd.merge(recent_videos, video_df)

    comment_df = pd.DataFrame()
    for video_id in video_ids:
        video_comment = get_comments(video_id)
        comment_df = pd.concat([comment_df, video_comment])

    return result_df, comment_df

if __name__ == '__main__':
    channel_id = input("Put your Channel ID starting with 'UC': ")
    startdate = input("Assign start date you would like to obtain information from (format: %Y-%m-%d): ")
    video_info, comments = main(channel_id, startdate)
    comments["textDisplay"] = comments["textDisplay"].apply(lambda x: x.replace("\n", ""))
    comments["textDisplay"] = comments["textDisplay"].apply(lambda x: x.replace("\r", ""))
    comments["textOriginal"] = comments["textOriginal"].apply(lambda x: x.replace("\n", ""))
    comments["textOriginal"] = comments["textOriginal"].apply(lambda x: x.replace("\r", ""))

    Path(f"output/{channel_id}/recent_from_{startdate}").mkdir(parents=True, exist_ok=True)
    video_info.to_csv(f"output/{channel_id}/recent_from_{startdate}/video_info.csv",index=False)
    comments.to_csv(f"output/{channel_id}/recent_from_{startdate}/comments.csv",index=False)
