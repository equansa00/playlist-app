from flask import Flask, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError

# Local imports
from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__)

# App Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://equansa00:1Chriss1@localhost/playlist-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Connect to database
connect_db(app)

# Migrations
migrate = Migrate(app, db)

# Debug Toolbar
debug = DebugToolbarExtension(app)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()  # rollback any database changes if an error occurs
    return "Internal Server Error", 500


@app.route("/")
def root():
    """Homepage: redirect to /playlists."""
    return redirect("/playlists")


# Playlist routes
@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""
    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)


@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""
    playlist = Playlist.query.get_or_404(playlist_id)
    return render_template("playlist_detail.html", playlist=playlist)


@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form."""
    form = PlaylistForm()
    if form.validate_on_submit():
        name = form.name.data
        new_playlist = Playlist(name=name)
        db.session.add(new_playlist)
        db.session.commit()
        return redirect("/playlists")
    return render_template("add_playlist.html", form=form)


# Song routes
@app.route("/songs")
def show_all_songs():
    """Show list of songs."""
    songs = Song.query.all()
    return render_template("songs.html", songs=songs)


@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """Return a specific song."""
    song = Song.query.get_or_404(song_id)
    return render_template("song_detail.html", song=song)


@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    form = SongForm()
    if form.validate_on_submit():
        title = form.title.data
        artist = form.artist.data
        new_song = Song(title=title, artist=artist)
        try:
            db.session.add(new_song)
            db.session.commit()
            return redirect("/songs")
        except IntegrityError:
            db.session.rollback()
            # Handle the error, maybe notify the user that the song already exists
    return render_template("add_song.html", form=form)


@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a song to a playlist."""
    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()

    # Restrict form to songs not already on this playlist
    curr_on_playlist = [s.id for s in playlist.songs]
    form.song.choices = (db.session.query(Song.id, Song.title)
                         .filter(Song.id.notin_(curr_on_playlist))
                         .all())

    if form.validate_on_submit():
        song = Song.query.get(form.song.data)
        playlist.songs.append(song)
        db.session.commit()
        return redirect(f"/playlists/{playlist_id}")

    return render_template("add_song_to_playlist.html", playlist=playlist, form=form)


if __name__ == "__main__":
    app.run(debug=True)