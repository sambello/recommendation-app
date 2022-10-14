# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 11:29:28 2022

@author: rrastogi
"""

import spotipy
from sklearn.metrics.pairwise import cosine_similarity


def recommend_similar_song_set(
        playlist,
        playlist_features_summary,
        songpool_features_set,
        similar_song_set_size):

    # ensure songpool does not contain the songs present within the input playlist
    
    songpool_features_set = playlist[playlist['id'].isin(songpool_features_set['id'].values)]
    
    # utilize cosine similarity metric between the playlist and the complete song set
    songpool_features_set['Similarity'] = cosine_similarity(songpool_features_set.drop('id', axis = 1).values, playlist_features_summary.values.reshape(1, -1))[:,0]
    output = songpool_features_set.sort_values('Similarity',ascending = False).head(similar_song_set_size)
    
    return output