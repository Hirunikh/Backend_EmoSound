from flask import Flask, jsonify, request
from flask_cors import CORS
import cv2
import numpy as np
from tensorflow import keras
import base64
from flask_sqlalchemy import SQLAlchemy
import requests  # Add this import statement
import random

# Import Spotipy and its dependencies
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize database connection
app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://dbuser:admin1234@EmoSound"
db = SQLAlchemy(app)


# Define SQLAlchemy model for the 'songs' table
class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    album = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    emotion = db.Column(db.String(255), nullable=False)


# Initialize Spotipy with your Spotify credentials
spotify_client_id = '509e4b42b830425187ace300b8630794'
spotify_client_secret = '740d58e9856b450da009daeb828c54dc'
sp_auth_manager = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
sp = spotipy.Spotify(auth_manager=sp_auth_manager)
print()

# Load the emotion detection model
emotion_model = keras.models.load_model('emotion_model.h5')

# Define the mapping of numerical labels to emotions
emotion_mapping = {0: 'Angry', 1: 'Excited', 2: 'Happy', 3: 'Neutral', 4: 'Sad'}

# Index route
@app.route('/')
def index():
    return 'Welcome to the Emotion Music Backend!'

# Route to get music recommendations based on captured image
@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    # Receive the image data from the frontend
    image_data = request.json.get('image')

    # Convert base64 image data to numpy array
    img_np = np.frombuffer(base64.b64decode(image_data.split(',')[1]), dtype=np.uint8)
    captured_image = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

    # Convert captured colored image to grayscale
    captured_image_grayscale = cv2.cvtColor(captured_image, cv2.COLOR_BGR2GRAY)

    # Preprocess the grayscale image for emotion detection
    img = cv2.resize(captured_image_grayscale, (64, 64))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)
    img = np.expand_dims(img, axis=-1)

    # Predict emotion
    emotion_prediction = emotion_model.predict(img)
    emotion_label = get_emotion_label(emotion_prediction)

    song_names = songs_by_emotion(emotion_label)
    # Get recommended music based on the detected emotion
    recommended_music = get_recommended_music(song_names)

    # Return detected emotion label along with music recommendations
    return jsonify({'emotion': emotion_label, 'music': recommended_music})

# Function to get the emotion label
def get_emotion_label(prediction):
    # Get the index of the highest predicted emotion
    predicted_emotion_index = np.argmax(prediction)
    # Return the corresponding emotion label
    return emotion_mapping[predicted_emotion_index]

# Function to fetch songs by emotion from database
def songs_by_emotion(emotion):
    try:
        # Query the database for songs with the specified emotion
        songs = Song.query.filter_by(emotion=emotion).all()

        # Shuffle the songs list to randomize the order
        random.shuffle(songs)

        # Extract only the name of the songs, limit to 10 songs
        song_names = [song.name for song in songs[:10]]
        return song_names

    except Exception as e:
        return []

# Function to get recommended music from Spotify
def get_recommended_music(song_names):
    if song_names:
        recommended_songs = []
        for song_name in song_names:
            # Search for each song on Spotify
            song_info = get_song_from_spotify(song_name)
            if song_info:
                recommended_songs.append(song_info)
            else:
                recommended_songs.append({'name': song_name, 'error': 'Song not found on Spotify'})
        return recommended_songs
    else:
        return []

# Function to search for a song on Spotify
def get_song_from_spotify(song_name):
    # Search for the song on Spotify
    search_results = sp.search(q=song_name, type='track', limit=1)
    if len(search_results['tracks']['items']) > 0:
        # Extract song details including URL
        track = search_results['tracks']['items'][0]
        song_url = track['external_urls']['spotify']
        # Convert duration from milliseconds to minutes and round to 2 decimal places
        duration_minutes = round(track['duration_ms'] / 60000, 2)
        song_info = {
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'url': song_url,
            'uri': track['uri'],
            'duration': duration_minutes
        }
        return song_info
    else:
        return None

# Route to get popular playlists
def get_popular_playlists(market='US'):
    url = f"https://api.spotify.com/v1/browse/featured-playlists?market={market}"
    headers = {
        'Authorization': 'Bearer ' + sp_auth_manager.get_access_token()['access_token']
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        playlists = data.get("playlists", {}).get("items", [])
        formatted_playlists = []
        for playlist in playlists[:1]:  # Limit to top 1 playlists
            name = playlist.get("name", "Unknown")
            description = playlist.get("description", "")
            tracks = get_tracks_for_playlist(playlist)  # Fetch tracks for the playlist
            formatted_playlist = {"name": name, "description": description, "tracks": tracks}
            formatted_playlists.append(formatted_playlist)
        return formatted_playlists
    else:
        return None

# Function to get tracks for a playlist from Spotify
def get_tracks_for_playlist(playlist):
    playlist_id = playlist.get("id")
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        'Authorization': 'Bearer ' + sp_auth_manager.get_access_token()['access_token']
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        tracks = data.get("items", [])[:10]  # Limit to the first 10 tracks
        formatted_tracks = []
        for track in tracks:
            song_url = track['track']['external_urls']['spotify']
            duration_minutes = round(track['track']['duration_ms'] / 60000, 2)
            track_info = {
                'name': track['track']['name'],
                'artist': track['track']['artists'][0]['name'],
                'album': track['track']['album']['name'],
                'url': song_url,
                'uri': track['track']['uri'],
                'duration': duration_minutes
            }
            formatted_tracks.append(track_info)
        return formatted_tracks
    else:
        return None

# Route to get popular playlists
@app.route('/popular_playlists', methods=['GET'])
def popular_playlists_route():
    # Call the function to get popular playlists
    playlists_us = get_popular_playlists(market='us')

    if playlists_us is not None:
        return jsonify(playlists_us), 200  # Return JSON response with status code 200 (OK)
    else:
        return jsonify({
            "error": "Failed to fetch popular playlists"
        }), 500  # Return error message with status code 500 (Internal Server Error)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
