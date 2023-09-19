"""Forms for playlist app."""

from wtforms import StringField, SelectField, SubmitField, validators
from flask_wtf import FlaskForm

class PlaylistForm(FlaskForm):
    """Form for adding playlists."""
    name = StringField("Playlist Name", [validators.Length(min=1)])
    submit = SubmitField("Create Playlist")

class SongForm(FlaskForm):
    """Form for adding songs."""
    title = StringField("Song Title", [validators.Length(min=1)])
    artist = StringField("Artist", [validators.Length(min=1)])
    submit = SubmitField("Add Song")

class NewSongForPlaylistForm(FlaskForm):
    """Form for adding a song to playlist."""
    song = SelectField('Song To Add', coerce=int)

