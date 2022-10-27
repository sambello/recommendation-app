import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import seaborn
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import json
import pandas as pd
from sample import recommend_similar_song_set 

with open('spotipy_cred.json','r') as f:
    data = json.load(f) 
    
client_credentials_manager = SpotifyClientCredentials(client_id=data['SPOTIPY_CLIENT_ID'], client_secret=data['SPOTIPY_CLIENT_SECRET'])
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def get_playlist_info(playlist_id, spot):
    info_list = []
    features_list = []
    
    for track in spot.playlist_tracks(playlist_id)["items"]:
         #URI
        track_uri = track["track"]["uri"]

        #Track name
        track_name = track["track"]["name"]

        #Main Artist
        artist_uri = track["track"]["artists"][0]["uri"]
        artist_info = spot.artist(artist_uri)

        #Name, popularity, genre
        artist_name = track["track"]["artists"][0]["name"]
        artist_pop = artist_info["popularity"]
        artist_genres = artist_info["genres"]

        #Album
        album = track["track"]["album"]["name"]

        #Popularity of the track
        track_pop = track["track"]["popularity"]


        info_list.append(
            [track_uri, track_name, artist_uri, artist_info, artist_name, artist_pop, artist_genres, album, track_pop]
        )
        features_list.append(pd.DataFrame(spot.audio_features(track["track"]["uri"])))
        
        
    playlist_df = pd.DataFrame(data = info_list, columns = ['track_uri', 'track_name', 'artist_uri',
                                              'artist_info', 'artist_name', 'artist_pop',
                                              'artist_genres', 'album', 'track_pop'])
    full_music = playlist_df.merge(pd.concat(features_list), left_on = 'track_uri', right_on = 'uri')
    
    return full_music

def genre_list_extractor(genre_series):
    genre_set = set()
    for i in genre_series:
        for gen in i:
            genre_set.add(gen)
    genre_dict = dict()
    for i in genre_set:
         genre_dict[i] = genre_series.apply(lambda x:  1 if i in x else 0)
    return pd.DataFrame(genre_dict)

def get_sum_vector(machine_df):
    trackers = machine_df['track_name']
    vector = machine_df.drop(columns = ['track_name']).sum(axis = 0)
    return np.divide(vector, machine_df.shape[0])

def get_playlist_subsets(playlist_id, spot):
    full_music = get_playlist_info(playlist_id, spot)
    categorical_music = pd.concat([genre_list_extractor(full_music.artist_genres), full_music], axis=1)
    
    #TODO scaling
    typed = categorical_music.dtypes.reset_index()
    catergories = list(typed[typed[0] != 'object']['index'].unique())
    catergories.append('track_name')
    numeric_mus = categorical_music[catergories]
    
    vector = get_sum_vector(numeric_mus)
    
    return categorical_music, numeric_mus, vector


def get_cluster_count(df):
    wcss = []
    for i in range(1,11):
        kmeans = KMeans(n_clusters=i,init='k-means++',max_iter=300,n_init=10,random_state=0)
        kmeans.fit(machine_fields.drop(columns = ['track_name']))
        wcss.append(kmeans.inertia_)
    plt.plot(range(1,11),wcss)
    plt.title('The Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')    
    return plt


def cluster_data(data, n):
    new_df = pd.DataFrame()
    kmeans = KMeans(n_clusters=n, random_state=0)
    new_df['cluster'] = kmeans.fit_predict(data)
    
    centroids = kmeans.cluster_centers_
    
    cen_x = [i[0] for i in centroids] 
    cen_y = [i[1] for i in centroids]
    
    centroids = kmeans.cluster_centers_
    
    x_mapper = dict()
    y_mapper = dict()
    for i in range(0,n):
        x_mapper[i] = cen_x[0]
        y_mapper[i] = cen_y[0]
    
    new_df['cen_x'] = new_df.cluster.apply(lambda x:  x_mapper[x])
    new_df['cen_y'] = new_df.cluster.apply(lambda x:  y_mapper[x])
    
    return new_df, centroids

def plot_axis_cluster(clust, cent, cat1, cat2):
    divisor = 4
    
    plt.scatter(clust[cat1], clust[cat2], c = clust.c, alpha = 0.6, s=10)
    num1 = clust.columns.get_loc(cat1)
    num2 = clust.columns.get_loc(cat2)
    for i in range(0,len(cent)):
        plt.plot(cent[i][num1], cent[i][num2], 'v', c = 'black')
        #print(i[num1], i[num2])
        
    for i, row in clustered.iterrows():
        if i % divisor == 0:
            plt.text(row[cat1], row[cat2], row.track_name)

    plt.xlabel(cat1)
    plt.ylabel(cat2)
    
    return plt
    
def recommend_from_urls(playlist_link, song_pool_link):
    
    #extract uris
    playlist_uri = playlist_link.split("/")[-1].split("?")[0]
    song_pool_uri = song_pool_link.split("/")[-1].split("?")[0]
    
    #get user input playlist summary
    native_fields1, machine_fields1, vector1 = get_playlist_subsets(playlist_uri, sp)
    clus1, centers1 = cluster_data(machine_fields1.drop(columns = ['track_name']), 3)
    clustered1 =  pd.concat([machine_fields1, clus1, native_fields1['track_uri']], axis=1)
    
    #get recommendation source playlist info
    native_fields, machine_fields, vector = get_playlist_subsets(song_pool_uri, sp)
    clus, centers = cluster_data(machine_fields.drop(columns = ['track_name']), 3)
    clustered =  pd.concat([machine_fields, clus, native_fields['track_uri']], axis=1)
    
    #ensure all fields across both df    
    filled_clust = clustered.drop(columns = ['cen_x', 'cen_y', 'cluster']).append(pd.DataFrame(vector1).T).fillna(0).iloc[:-1]
    filled_vect = clustered.drop(columns = ['cen_x', 'cen_y', 'cluster']).append(pd.DataFrame(vector1).T).fillna(0).iloc[-1]
      
    return recommend_similar_song_set(clustered1.drop(columns = ['track_name']), 
                           pd.DataFrame(filled_vect).T.drop(columns = ['track_name', 'track_uri']),
                           filled_clust,
                           10)





