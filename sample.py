# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 11:29:28 2022

@author: rrastogi
"""

import spotipy
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


def recommend_similar_song_set(
        playlist,
        playlist_features_summary,
        songpool_features_set,
        similar_song_set_size):

    # ensure songpool does not contain the songs present within the input playlist
    
    songpool_features_set = songpool_features_set[~songpool_features_set['track_uri'].isin(playlist['track_uri'])]

    # utilize cosine similarity metric between the playlist and the complete song set
    
   
    songpool_features_set['Similarity'] = pd.DataFrame(cosine_similarity(playlist_features_summary, songpool_features_set.drop(columns = ['track_uri', 'track_name']))).T
    
    output = songpool_features_set.sort_values('Similarity',ascending = False).head(similar_song_set_size)
    
    return output