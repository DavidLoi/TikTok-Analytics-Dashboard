# Imports for tiktok SDK
from TikTokApi import TikTokApi
import asyncio
import os
# Import JSON for data export
import json
# Import data processing helper
from helpers import process_results, save, key_exists, load
# Import pandas for dataframes
import pandas as pd
# Import sys dependency to extract command line args
import sys

async def search_videos(name):
    # Set ms_token
    ms_token = os.environ.get("26t4a1kDv8o_N8WX7eFCxQah3FxEMaANV7a1x_96hybAP8eLCBackVA0aQ4-52hFo_LaLiPTjjqXITmOcPpPv7YZ1DYidTSSEMQP0GRpKpMEdaIPYroi3X94D4BVfQv_Oa_7Z9Cc", None)
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False, starting_url='https://www.tiktok.com/search?lang=en&q='+name)
        users = []
        async for video in api.trending.videos():
            users.append(video.as_dict)
        with open('export.json', 'w') as f:
            json.dump(users, f)
    return users

async def get_hashtag_videos(name):
    # Set ms_token
    ms_token = os.environ.get("gd_wzoKZirqCiQQZ5g2Az23Bm7XT0CySfinRDRWB6iGvGJa4bktQdZIrnmm1wd85yDzob3LMko1EaeDq4DyRUmQCfUfKDNE7cjW3ZYBJOlZdvFyVZS-8Sssxl2Fe-gbrDqkB9KzN", None)
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False)
        tag = api.hashtag(name=name)
        data = []
        # Get video data for each video
        async for video in tag.videos(count=30):
            data.append(video.as_dict)
        # with open('export.json', 'w') as f:
        #     json.dump(data, f)
    return data

async def sound_videos(df):
    # Set ms_token
    ms_token = os.environ.get("gd_wzoKZirqCiQQZ5g2Az23Bm7XT0CySfinRDRWB6iGvGJa4bktQdZIrnmm1wd85yDzob3LMko1EaeDq4DyRUmQCfUfKDNE7cjW3ZYBJOlZdvFyVZS-8Sssxl2Fe-gbrDqkB9KzN", None)
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False)
        data = []
        for sound_id in df['music_id'].unique():
            if key_exists(sound_id+'.csv'):
                song_df = load(sound_id+'.csv')

            else:
                duration = []
                saves = []
                comments = []
                likes = []
                plays = []
                shares = []
                name = ""

                async for sound in api.sound(id=sound_id).videos(count=30):
                    song = sound.as_dict
                    duration.append(song['music']['duration'])
                    if len(duration) == 0:
                        duration.append(0)
                    saves.append(song['stats']['collectCount'])
                    comments.append(song['stats']['commentCount'])
                    likes.append(song['stats']['diggCount'])
                    plays.append(song['stats']['playCount'])
                    shares.append(song['stats']['shareCount'])
                    name = song['music']['title'] + '-' + song['music']['authorName']

                song_dict = {'id': [sound_id],
                            'song': [name],
                            'count': [len(duration)],
                            'duration': [sum(duration)/len(duration)],
                            'saves': [sum(saves)],
                            'comments': [sum(comments)],
                            'likes': [sum(likes)],
                            'plays': [sum(plays)],
                            'shares': [sum(shares)],
                            'mean_saves': [sum(saves)/len(saves)],
                            'mean_comments': [sum(comments)/len(comments)],
                            'mean_likes': [sum(likes)/len(likes)],
                            'mean_plays': [sum(plays)/len(plays)],
                            'mean_shares': [sum(shares)/len(shares)]}
                song_df = pd.DataFrame.from_dict(song_dict)
                save(song_df, sound_id+'.csv')

            data.append(song_df)
    
    # Export data
    df = pd.concat(data)
    save(df, hashtag+'_song_data.csv')

def get_users(name):
    # Get tiktok data
    data = asyncio.run(search_videos(name))

    # Process data
    flattened_data = data #process_results(data)

    # Convert processed data to dataframe
    df = pd.DataFrame.from_dict(flattened_data, orient='index')
    df.to_csv('searchdata.csv', index=False)
 
def get_hashtag(hashtag):
    # Get tiktok data
    data = asyncio.run(get_hashtag_videos(hashtag))

    # Process data
    flattened_data = process_results(data)

    # Convert processed data to dataframe
    df = pd.DataFrame.from_dict(flattened_data, orient='index')
    df['normalized_collectCount'] = df['stats_collectCount']/df['authorStats_followerCount']
    df['normalized_commentCount'] = df['stats_commentCount']/df['authorStats_followerCount']
    df['normalized_diggCount'] = df['stats_diggCount']/df['authorStats_followerCount']
    df['normalized_playCount'] = df['stats_playCount']/df['authorStats_followerCount']
    df['normalized_shareCount'] = df['stats_shareCount']/df['authorStats_followerCount']
    df['count'] = 1
    
    save(df, hashtag+'_data.csv')
    return df

def description_stats(hashtag, df):
    # Columns for new dataframe
    length = []
    saves = []
    comments = []
    likes = []
    plays = []
    shares = []

    # Iterate through data
    for i in range(len(df)):
        # Add length of description
        if (pd.isnull(df.iloc[i]['desc'])):
            length.append(0)
        else:
            length.append(len(df.iloc[i]['desc']))
    
        # Add number of saves
        saves.append(df.iloc[i]['normalized_collectCount'])

        # Add number of comments
        comments.append(df.iloc[i]['normalized_commentCount'])

        # Add number of likes
        likes.append(df.iloc[i]['normalized_diggCount'])

        # Add number of plays
        plays.append(df.iloc[i]['normalized_playCount'])

        # Add number of shares
        shares.append(df.iloc[i]['normalized_shareCount'])

    # Create description dataframe
    desc_list = [length, saves, comments, likes, plays, shares]
    desc_df = pd.DataFrame(desc_list).transpose()
    desc_df.columns = ['length', 'saves', 'comments', 'likes', 'plays', 'shares']

    # Sort by ascending length and average entries with same description length
    desc_df.sort_values(by=['length'], inplace=True)
    count = [desc_df.groupby(['length']).count().iloc[i]['saves'] for i in range(len(desc_df.groupby(['length'])))]
    desc_df = desc_df.groupby('length').mean().reset_index()
    desc_df['count'] = count
    
    # Export dataframe
    # desc_df.to_csv(hashtag+'_desc_data.csv')
    save(desc_df, hashtag+'_desc_data.csv')

def hashtag_stats(hashtag, df):
    # Columns for new dataframe
    hashtags = []
    saves = []
    comments = []
    likes = []
    plays = []
    shares = []

    # Iterate through data
    for i in range(len(df)):
        # Add length of description
        if (pd.isnull(df.iloc[i]['desc'])):
            hashtags.append(0)
        else:
            hashtags.append(df.iloc[i]['desc'].count('#'))
    
        # Add number of saves
        saves.append(df.iloc[i]['normalized_collectCount'])

        # Add number of comments
        comments.append(df.iloc[i]['normalized_commentCount'])

        # Add number of likes
        likes.append(df.iloc[i]['normalized_diggCount'])

        # Add number of plays
        plays.append(df.iloc[i]['normalized_playCount'])

        # Add number of shares
        shares.append(df.iloc[i]['normalized_shareCount'])

    # Create description dataframe
    tags_list = [hashtags, saves, comments, likes, plays, shares]
    tags_df = pd.DataFrame(tags_list).transpose()
    tags_df.columns = ['hashtags', 'saves', 'comments', 'likes', 'plays', 'shares']

    # Sort by ascending hashtags and average entries with same description hashtags
    tags_df.sort_values(by=['hashtags'], inplace=True)
    count = [tags_df.groupby(['hashtags']).count().iloc[i]['saves'] for i in range(len(tags_df.groupby(['hashtags'])))]
    tags_df = tags_df.groupby('hashtags').mean().reset_index()
    tags_df['count'] = count
    
    # Export dataframe
    # tags_df.to_csv(hashtag+'_tags_data.csv')
    save(tags_df, hashtag+'_tags_data.csv')

def duration_stats(hashtag, df):
    # Columns for new dataframe
    duration = []
    saves = []
    comments = []
    likes = []
    plays = []
    shares = []

    # Iterate through data
    for i in range(len(df)):
        # Add duration
        duration.append(df.iloc[i]['video_duration'])
    
        # Add number of saves
        saves.append(df.iloc[i]['normalized_collectCount'])

        # Add number of comments
        comments.append(df.iloc[i]['normalized_commentCount'])

        # Add number of likes
        likes.append(df.iloc[i]['normalized_diggCount'])

        # Add number of plays
        plays.append(df.iloc[i]['normalized_playCount'])

        # Add number of shares
        shares.append(df.iloc[i]['normalized_shareCount'])

    # Create description dataframe
    duration_list = [duration, saves, comments, likes, plays, shares]
    duration_df = pd.DataFrame(duration_list).transpose()
    duration_df.columns = ['duration', 'saves', 'comments', 'likes', 'plays', 'shares']

    # Sort by ascending duration and average entries with same description duration
    duration_df.sort_values(by=['duration'], inplace=True)
    count = [duration_df.groupby(['duration']).count().iloc[i]['saves'] for i in range(len(duration_df.groupby(['duration'])))]
    duration_df = duration_df.groupby('duration').mean().reset_index()
    duration_df['count'] = count
    
    # Export dataframe
    # duration_df.to_csv(hashtag+'_tags_data.csv')
    save(duration_df, hashtag+'_duration_data.csv')

if __name__ == '__main__':    
    hashtag = sys.argv[1]
    # get_users(hashtag)
    # if not os.path.isfile(hashtag + '_data.csv'):
    # Get data
    if key_exists(hashtag+'_data.csv'):
        print("GET DATA")
        df = get_hashtag(hashtag)
        asyncio.run(sound_videos(df))
        description_stats(hashtag, df)
        hashtag_stats(hashtag, df)
        duration_stats(hashtag, df)
    else:
        print("DATA EXISTS")
    