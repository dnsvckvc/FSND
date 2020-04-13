#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import datetime
from sqlalchemy import func
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
# CHECK
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'
    __table_args__ = (db.UniqueConstraint('city', 'state', 'address', name='total_address'),
                      db.UniqueConstraint('city', 'state', 'name', name='name_city_state'))

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    shows = db.relationship('Show', backref='show_venue', lazy=True, cascade = 'all, delete-orphan')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    shows = db.relationship('Show', backref='show_artist', lazy=True, cascade='all, delete-orphan')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
  __tablename__ = 'shows'

  id = db.Column(db.Integer, primary_key=True)
  venue = db.Column(db.Integer, db.ForeignKey('venues.id', ondelete="CASCADE"), nullable=False)
  artist = db.Column(db.Integer, db.ForeignKey('artists.id', ondelete="CASCADE"), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # Check
  result = []
  for city in Venue.query.distinct('city').all():
    result_item = {}
    result_item['city'] = city.city
    result_item['state'] = city.state
    result_venues = []
    for venue in Venue.query.filter_by(city=city.city).all():
      result_venue_item = {}
      result_venue_item['id'] = venue.id
      result_venue_item['name'] = venue.name
      result_venue_item['num_upcoming_shows'] = 0
      result_venues.append(result_venue_item)
    result_item['venues'] = result_venues
    result.append(result_item)
  return render_template('pages/venues.html', areas=result);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  # Check
  results = Venue.query.filter(func.lower(Venue.name).contains(func.lower(request.form['search_term']))).all()
  response = {}
  data = []
  for result in results:
    temp = {}
    temp['id'] = result.id
    temp['name'] = result.name
    shows = Show.query.filter_by(artist = result.id)
    current_date_raw = str(datetime.now())
    shows_upcoming = shows.filter(Show.start_time > current_date_raw).all()
    temp['num_upcoming_shows'] = len(shows_upcoming)
    data.append(temp)
  response['data'] = data
  response['count'] = len(data)
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # Check
  venue = Venue.query.filter_by(id=venue_id).first()

  current_date_raw = str(datetime.now())

  shows = Show.query.filter_by(venue = venue_id)

  shows_upcoming = shows.filter(Show.start_time > current_date_raw).all()
  shows_past = shows.filter(Show.start_time < current_date_raw).all()

  
  output = {}
  output['id'] = venue.id
  output['name'] = venue.name
  output['city'] = venue.city
  output['state'] = venue.state
  output['phone'] = venue.phone
  output['website'] = 'www.dummy.com'
  output['facebook_link'] = venue.facebook_link
  output['seeking_talent'] = True
  output['seeking_description'] = 'Looking for fancy shows'
  output['image_link'] = venue.image_link
  output_past_shows = [] 
  output_upcoming_shows = []
  for show in shows_upcoming:
    show_dict = {}
    show_dict['artist_id'] = show.artist
    show_dict['artist_name'] = show.show_artist.name
    show_dict['artist_image_link'] = show.show_artist.image_link
    show_dict['start_time'] = str(show.start_time)
    output_upcoming_shows.append(show_dict)

  for show in shows_past:
    show_dict = {}
    show_dict['venue_id'] = show.venue
    show_dict['artist_name'] = show.show_artist.name
    show_dict['artist_image_link'] = show.show_artist.image_link
    show_dict['start_time'] = str(show.start_time)
    output_past_shows.append(show_dict)

  output['past_shows'] = output_past_shows
  output['upcoming_shows'] = output_upcoming_shows
  output['past_shows_counts'] = len(output_past_shows)
  output['upcoming_shows_counts'] = len(output_upcoming_shows)

  genre_list = []
  for show in shows.all():
    genre_list.append(show.show_artist.genres)
  
  output['genres'] = set(genre_list)

  return render_template('pages/show_venue.html', venue=output)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # Check
  try:
    print(request.form)
    form_input = request.form
    venue = Venue(name = form_input['name'],
                  city = form_input['city'],
                  state = form_input['state'],
                  address = form_input['address'],
                  phone = form_input['phone'],
                  facebook_link = form_input['facebook_link'])
    db.session.add(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # Check
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  # Check
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    flash('Successful. Venue ' + venue_id + ' deleted.')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + ' could not be deleted.')
  finally:
    db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  # Check
  artists = Artist.query.all()
  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  # Check
  results = Artist.query.filter(func.lower(Artist.name).contains(func.lower(request.form['search_term']))).all()
  response = {}
  data = []
  for result in results:
    temp = {}
    temp['id'] = result.id
    temp['name'] = result.name
    shows = Show.query.filter_by(artist = result.id)
    current_date_raw = str(datetime.now())
    shows_upcoming = shows.filter(Show.start_time > current_date_raw).all()
    temp['num_upcoming_shows'] = len(shows_upcoming)
    data.append(temp)
  response['data'] = data
  response['count'] = len(data)
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # Check
  artist = Artist.query.filter_by(id=artist_id).first()
  current_date_raw = str(datetime.now())
  # current_date = format_datetime(current_date_raw)
  shows = Show.query.filter_by(artist = artist_id)
  shows_upcoming = shows.filter(Show.start_time > current_date_raw).all()
  shows_past = shows.filter(Show.start_time < current_date_raw).all()

  output = {}
  output['id'] = artist.id
  output['name'] = artist.name
  output['genres'] = artist.genres
  output['city'] = artist.city
  output['state'] = artist.state
  output['phone'] = artist.phone
  output['website'] = 'www.dummy.com'
  output['facebook_link'] = artist.facebook_link
  output['seeking_venue'] = True
  output['seeking_description'] = 'Looking for fancy shows'
  output['image_link'] = artist.image_link
  output_past_shows = [] 
  output_upcoming_shows = []
  for show in shows_upcoming:
    show_dict = {}
    show_dict['venue_id'] = show.venue
    show_dict['venue_name'] = show.show_venue.name
    show_dict['venue_image_link'] = show.show_venue.image_link
    show_dict['start_time'] = str(show.start_time)
    output_upcoming_shows.append(show_dict)

  for show in shows_past:
    show_dict = {}
    show_dict['venue_id'] = show.venue
    show_dict['venue_name'] = show.show_venue.name
    show_dict['venue_image_link'] = show.show_venue.image_link
    show_dict['start_time'] = str(show.start_time)
    output_past_shows.append(show_dict)

  output['past_shows'] = output_past_shows
  output['upcoming_shows'] = output_upcoming_shows
  output['past_shows_counts'] = len(output_past_shows)
  output['upcoming_shows_counts'] = len(output_upcoming_shows)
  
  return render_template('pages/show_artist.html', artist=output)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  data = {}
  data['id'] = artist.id
  data['name'] = artist.name
  data['genres'] = artist.genres
  data['city'] = artist.city
  data['state'] = artist.state
  data['phone'] = artist.phone
  data['website'] = 'www.whyistherenowebsitelink.com'
  data['facebook_link'] = artist.facebook_link
  data['seeking_venue'] = True
  data['seeking_description'] = 'Looking for someone'
  data['image_link'] = artist.image_link
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  try:
    form_input = request.form
    artist = Artist.query.get(artist_id)
    artist.name = form_input['name']
    artist.city = form_input['city']
    artist.state = form_input['state']
    artist.genres = form_input['genres']
    artist.home = form_input['phone']
    artist.facebook_link = form_input['facebook_link']
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + artist_id + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # Check
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + artist_id + ' could not be updated.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  data = {}
  data['id'] = venue.id
  data['name'] = venue.name
  data['address'] = venue.address
  data['city'] = venue.city
  data['state'] = venue.state
  data['phone'] = venue.phone
  data['website'] = 'www.whyistherenowebsitelink.com'
  data['facebook_link'] = venue.facebook_link
  data['seeking_venue'] = True
  data['seeking_description'] = 'Looking for someone'
  data['image_link'] = venue.image_link
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  try:
    form_input = request.form
    venue = Venue.query.get(venue_id)
    venue.name = form_input['name']
    venue.city = form_input['city']
    venue.state = form_input['state']
    venue.address = form_input['address']
    venue.home = form_input['phone']
    venue.facebook_link = form_input['facebook_link']
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + venue_id + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # Check
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + venue_id + ' could not be updated.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # Check
  try:
    form_input = request.form
    artist = Artist(name = form_input['name'],
                  city = form_input['city'],
                  state = form_input['state'],
                  genres = form_input['genres'],
                  phone = form_input['phone'],
                  facebook_link = form_input['facebook_link'])
    db.session.add(artist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # Check
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
    db.session.close()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # Check
  show_query_items = Show.query.all()
  data = []
  for show in show_query_items:
    show_dict = {}
    show_dict['venue_id'] = show.venue
    show_dict['venue_name'] = show.show_venue.name
    show_dict['artist_id'] = show.artist
    show_dict['artist_name'] = show.show_artist.name
    show_dict['artist_image_link'] = show.show_artist.image_link
    show_dict['start_time'] = str(show.start_time)
    data.append(show_dict)

  # data=[{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 5,
  #   "artist_name": "Matt Quevedo",
  #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "start_time": "2019-06-15T23:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-01T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-08T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-15T20:00:00.000Z"
  # }]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  # Check
  try:
    form_input = request.form
    show = Show(start_time = form_input['start_time'])
    show.artist = form_input['artist_id']
    show.venue = form_input['venue_id']
    db.session.add(show)
    db.session.commit()
  # on successful db insert, flash success
    flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # Check
  except:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
