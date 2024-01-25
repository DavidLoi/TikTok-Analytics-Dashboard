# Import base streamlit dependency
import streamlit as st
# Import pandas to load analytics data
import pandas as pd
# Import subprocess to run tiktok script from command line
from subprocess import call
# Import sys to get path to Python interpreter
import sys
# Import plotly for visualizations
import plotly.express as px
# Import os for checking if file exists
import os
# Import time to wait for file to be created
import time
# Import load from helpers
from helpers import load


# Set page width wide
st.set_page_config(layout='wide')

# Create sidebar
st.sidebar.markdown("<img src='https://upload.wikimedia.org/wikipedia/en/thumb/a/a9/TikTok_logo.svg/640px-TikTok_logo.svg.png' width=200 />", unsafe_allow_html=True)
st.sidebar.markdown("This dashboard allows you to analyse trending tiktoks using Python and Streamlit.")
st.sidebar.markdown("To get started <ol><li>Enter the <i>hashtag</i> you wish to analyse.</li> <li>Hit <i>Get Data</i>.</li> <li>Get analyzing.</li></ol>", unsafe_allow_html=True)
st.sidebar.markdown("*Note that video stats (saves, comments, etc.) have been normalized by account size (number of followers) to account for varying account sizes.*")

# Input
hashtag = st.text_input('Search for a hashtag here', value="")

# Button
if st.button('Get Data'):
  # Run get data function here
  # Use sys.executable to get correct Python interpreter
  call([sys.executable, '-m', 'tiktok', hashtag])

  # Load in data
  df = load(hashtag+'_data.csv')
  description_df = load(hashtag+'_desc_data.csv')
  hashtag_df = load(hashtag+'_tags_data.csv')
  song_df = load(hashtag+'_song_data.csv')
  duration_df = load(hashtag+'_duration_data.csv')

  # Account size
  st.markdown("<h1>Account Size</h1>", unsafe_allow_html=True)
  st.write("Average account size: ", df['authorStats_followerCount'].mean().item())
  st.write("Median account size: ", df['authorStats_followerCount'].median().item())
  acc_counts = px.histogram(df, x='authorStats_followerCount', y='count', nbins=1000)
  st.plotly_chart(acc_counts, use_container_width=True)

  # Description section
  st.markdown("<h1>Description</h1>", unsafe_allow_html=True)

  desc_counts = px.histogram(description_df, x='length', y='count', nbins=100)
  st.plotly_chart(desc_counts, use_container_width=True)
  desc_saves = px.scatter(description_df, x='length', y='saves', hover_data=['length'])
  st.plotly_chart(desc_saves, use_container_width=True)
  desc_comments = px.scatter(description_df, x='length', y='comments', hover_data=['length'])
  st.plotly_chart(desc_comments, use_container_width=True)
  desc_likes = px.scatter(description_df, x='length', y='likes', hover_data=['length'])
  st.plotly_chart(desc_likes, use_container_width=True)
  desc_plays = px.scatter(description_df, x='length', y='plays', hover_data=['length'])
  st.plotly_chart(desc_plays, use_container_width=True)
  desc_shares = px.scatter(description_df, x='length', y='shares', hover_data=['length'])
  st.plotly_chart(desc_shares, use_container_width=True)

  # Hashtag section
  st.markdown("<h1>Hashtag</h1>", unsafe_allow_html=True)

  tags_counts = px.histogram(hashtag_df, x='hashtags', y='count', nbins=100)
  st.plotly_chart(tags_counts, use_container_width=True)
  tags_saves = px.scatter(hashtag_df, x='hashtags', y='saves', hover_data=['hashtags'])
  st.plotly_chart(tags_saves, use_container_width=True)
  tags_comments = px.scatter(hashtag_df, x='hashtags', y='comments', hover_data=['hashtags'])
  st.plotly_chart(tags_comments, use_container_width=True)
  tags_likes = px.scatter(hashtag_df, x='hashtags', y='likes', hover_data=['hashtags'])
  st.plotly_chart(tags_likes, use_container_width=True)
  tags_plays = px.scatter(hashtag_df, x='hashtags', y='plays', hover_data=['hashtags'])
  st.plotly_chart(tags_plays, use_container_width=True)
  tags_shares = px.scatter(hashtag_df, x='hashtags', y='shares', hover_data=['hashtags'])
  st.plotly_chart(tags_shares, use_container_width=True)

  # Duration section
  st.markdown("<h1>Duration</h1>", unsafe_allow_html=True)

  duration_counts = px.histogram(duration_df, x='duration', y='count', nbins=100)
  st.plotly_chart(duration_counts, use_container_width=True)
  duration_saves = px.scatter(duration_df, x='duration', y='saves', hover_data=['duration'])
  st.plotly_chart(duration_saves, use_container_width=True)
  duration_comments = px.scatter(duration_df, x='duration', y='comments', hover_data=['duration'])
  st.plotly_chart(duration_comments, use_container_width=True)
  duration_likes = px.scatter(duration_df, x='duration', y='likes', hover_data=['duration'])
  st.plotly_chart(duration_likes, use_container_width=True)
  duration_plays = px.scatter(duration_df, x='duration', y='plays', hover_data=['duration'])
  st.plotly_chart(duration_plays, use_container_width=True)
  duration_shares = px.scatter(duration_df, x='duration', y='shares', hover_data=['duration'])
  st.plotly_chart(duration_shares, use_container_width=True)

  # Sound section
  st.markdown("<h1>Sound</h1>", unsafe_allow_html=True)
  song_counts = px.pie(song_df, values='count', names='song')
  st.plotly_chart(song_counts, use_container_width=True)
  song_saves = px.pie(song_df, values='mean_saves', names='song')
  st.plotly_chart(song_saves, use_container_width=True)
  song_comments = px.pie(song_df, values='mean_comments', names='song')
  st.plotly_chart(song_comments, use_container_width=True)
  song_likes = px.pie(song_df, values='mean_likes', names='song')
  st.plotly_chart(song_likes, use_container_width=True)
  song_plays = px.pie(song_df, values='mean_plays', names='song')
  st.plotly_chart(song_plays, use_container_width=True)
  song_shares = px.pie(song_df, values='mean_shares', names='song')
  st.plotly_chart(song_shares, use_container_width=True)


  # # Plotly visualizations
  # fig = px.histogram(df, x='desc', hover_data=['desc'], y='stats_diggCount', height=300)
  # st.plotly_chart(fig, use_container_width=True)

  # # Split columns
  # left_col, right_col = st.columns(2)

  # # Video stats
  # scatter1 = px.scatter(df, x='stats_shareCount', y='stats_commentCount', hover_data=['author_nickname'], size='stats_playCount', color='stats_playCount')
  # left_col.plotly_chart(scatter1, use_container_width=True)

  # scatter2 = px.scatter(df, x='authorStats_videoCount', y='authorStats_heartCount', hover_data=['author_nickname'], size='authorStats_followerCount', color='authorStats_followerCount', )
  # right_col.plotly_chart(scatter2, use_container_width=True)

  # Show tabular dataframe in streamlit
  df