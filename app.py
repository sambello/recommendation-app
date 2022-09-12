from datetime import date
from flask import Flask, render_template, url_for, request, redirect
# import pandas as pd
# from application.features import *
# from application.model import *

app = Flask(__name__)

def age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
      return render_template('index.html', feedback=True)
    else:
      return render_template('index.html', feedback=False)

@app.route("/about", methods=['GET'])
def about():
  people = [{
    "id": 1,
    "name": "Sam Bello",
    "age": str(age(date(1996, 9, 25))),
    "email": "sambello25@gmail.com",
    "about": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus at gravida justo. In facilisis dictum ante nec efficitur. Mauris quis tellus ultricies, eleifend magna vel, sodales odio. Mauris ornare cursus sapien sit amet facilisis. Cras finibus eget justo vel vehicula. Praesent in risus at erat tincidunt malesuada ut in eros. Phasellus at justo vel est sollicitudin vehicula."
  },
  {
    "id": 2,
    "name": "Rohan Rastogi",
    "age": "27",
    "email": "rrastogi@signifyhealth.com",
    "about": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus at gravida justo. In facilisis dictum ante nec efficitur. Mauris quis tellus ultricies, eleifend magna vel, sodales odio. Mauris ornare cursus sapien sit amet facilisis. Cras finibus eget justo vel vehicula. Praesent in risus at erat tincidunt malesuada ut in eros. Phasellus at justo vel est sollicitudin vehicula."
  },
  {
    "id": 3,
    "name": "Zachary Roga",
    "age": "27",
    "email": "zroga@signifyhealth.com",
    "about": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus at gravida justo. In facilisis dictum ante nec efficitur. Mauris quis tellus ultricies, eleifend magna vel, sodales odio. Mauris ornare cursus sapien sit amet facilisis. Cras finibus eget justo vel vehicula. Praesent in risus at erat tincidunt malesuada ut in eros. Phasellus at justo vel est sollicitudin vehicula."
  }]
  return render_template('about.html', people=people)

@app.route('/recommend', methods=['POST'])
def recommend():
  
  URL = request.form['URL']
  print(URL)

  numsongs = int(request.form['numsongs'])
  print(numsongs)

  if URL == "":
    return render_template('results.html', noLink=True)
  else:
    # df = extract(URL)
    # edm_top40 = recommend_from_playlist(songDF, complete_feature_set, df)

    # Dummy Data
    songs = [
      {
        "artist": "Kendrick Lamar",
        "title": "Alright",
        "link": "https://open.spotify.com/track/3iVcZ5G6tvkXZkZKlMpIUs?si=40b39efaf44e44a9"
      },
      {
        "artist": "Kanye West",
        "title": "Devil in a New Dress [ft. Rick Ross]",
        "link": "https://open.spotify.com/track/1UGD3lW3tDmgZfAVDh6w7r?si=027369268ba64192"
      },
      {
        "artist": "Tyler, the Creator",
        "title": "New Magic Wand",
        "link": "https://open.spotify.com/track/0fv2KH6hac06J86hBUTcSf?si=031fb4ca32d34389"
      },
      {
        "artist": "Mac Demarco",
        "title": "Still Beating",
        "link": "https://open.spotify.com/track/4LpUpiYoZ2M3Z1kmhn4EQo?si=54c0601a27b94bd4"
      },
      {
        "artist": "Men I Trust",
        "title": "Show Me How",
        "link": "https://open.spotify.com/track/01TyFEZu6mHbffsVfxgrFn?si=e70f485643574475"
      },
      {
        "artist": "Denzel Curry",
        "title": "VENGEANCE | VENGEANCE [ft. JPEGMAFIA & ZILLAKAMI | JPEGMAF1A + Z1LLAKAM1]",
        "link": "https://open.spotify.com/track/4d8BSdhx6WT5GtTOWpv4rh?si=bf1994014e5e4991"
      },
      {
        "artist": "The Killers",
        "title": "Mr. Brightside",
        "link": "https://open.spotify.com/track/003vvx7Niy0yvhvHt4a68B?si=2c68c31ce9de41f9"
      },
      {
        "artist": "The Temper Trap",
        "title": "Sweet Disposition",
        "link": "https://open.spotify.com/track/5RoIXwyTCdyUjpMMkk4uPd?si=459aa03e4e9a4e19"
      },
      {
        "artist": "Mac Miller",
        "title": "Love Lost",
        "link": "https://open.spotify.com/track/0N9C80kcgL0xXGduKnYKWi?si=cb1c452d5a2f4fb2"
      },
      {
        "artist": "Harry Styles",
        "title": "Satellite",
        "link": "https://open.spotify.com/track/0rzaRSujxA0bKyjJl6vHYq?si=ae93d92029664b17"
      }
    ]
    
    # for i in range(numsongs):
    #   my_songs.append([str(edm_top40.iloc[i,1]) + ' - '+ '"'+str(edm_top40.iloc[i,4])+'"', "https://open.spotify.com/track/"+ str(edm_top40.iloc[i,-6]).split("/")[-1]])
    
    # if request.method == "GET":
    #   return render_template('results.html', songs=songs, feedback=True)
    
    return render_template('results.html', songs=songs)

@app.route('/feedback', methods=['POST'])
def feedback():
  print(request.form['rating'])
  return redirect("/")

if __name__ == "__main__":
  app.run(debug=True)