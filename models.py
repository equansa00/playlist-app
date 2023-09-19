# models.py

from flask_sqlalchemy import SQLAlchemy

# Initialize a database object. We will initialize the app for this in app.py.
db = SQLAlchemy()

# Models

class Playlist(db.Model):
    """Playlist."""
    __tablename__ = 'playlists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    songs = db.relationship('PlaylistSong', backref='playlist')

class Song(db.Model):
    """Song."""
    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    playlists = db.relationship('PlaylistSong', backref='song')

class PlaylistSong(db.Model):
    """Mapping of a playlist to a song."""
    __tablename__ = 'playlists_songs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), nullable=False)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), nullable=False)

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)
