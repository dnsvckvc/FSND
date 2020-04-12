from app import Venue, Artist 
# from app import Show
import psycopg2

connection = psycopg2.connect("dbname = fyyur")
cursor = connection.cursor()

SQL_VENUES = '''
INSERT INTO venues 
      (id, 
      name, 
      city, 
      state, 
      address, 
      phone, 
      image_link, 
      facebook_link) 
    VALUES 
      (%(id)s, 
      %(name)s,
      %(city)s,
      %(state)s,
      %(address)s,
      %(phone)s,
      %(image_link)s,
      %(facebook_link)s);
'''

# class Venue(db.Model):
#     __tablename__ = 'Venue'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     city = db.Column(db.String(120))
#     state = db.Column(db.String(120))
#     address = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     facebook_link = db.Column(db.String(120))

data_venues = [{'id': 1, 
        'name': 'The Musical Hop',
        'city': 'San Francisco',
        'state': 'California',
        'address':'Dummy Road 1',
        'phone':'123456789',
        'image_link': 'https://findrandomlink.com/sf',
        'facebook_link':'https://facebook.com/randomlink_sf'},
        {'id': 2, 
        'name': 'The Dueling Pianos Bar',
        'city': 'New York',
        'state': 'New York',
        'address':'Default Avenue 3',
        'phone':'013444555',
        'image_link':'https://anotherlink.ch',
        'facebook_link':'https://facebookdummylink.de'},
        {'id': 3, 
        'name': 'Park Square Live Music & Coffee',
        'city': 'San Francisco',
        'state': 'California',
        'address':'Random Way 333',
        'phone':'123444999',
        'image_link':'https://randomlink123.com',
        'facebook_link':'https://www.facebook.com'},
        {'id': 4, 
        'name': 'Kafana',
        'city': 'New York',
        'state': 'New York',
        'address':'Belgrade Street 3',
        'phone':'444555666',
        'image_link':'https://linktosite.com',
        'facebook_link':'https://linktofacebook.com'}]

cursor.executemany(
  SQL_VENUES, 
  data_venues
  )


SQL_ARTISTS = '''
INSERT INTO artists 
      (id, 
      name, 
      city, 
      state, 
      phone, 
      genres, 
      image_link, 
      facebook_link) 
    VALUES 
      (%(id)s, 
      %(name)s,
      %(city)s,
      %(state)s,
      %(phone)s,
      %(genres)s,
      %(image_link)s,
      %(facebook_link)s);
'''

# class Artist(db.Model):
#     __tablename__ = 'Artist'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     city = db.Column(db.String(120))
#     state = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     genres = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     facebook_link = db.Column(db.String(120)


data_artists = [{'id': 1, 
        'name': 'Guns N Petals',
        'city': 'San Francisco',
        'state': 'California',
        'phone':'123456789',
        'genres':'Rock',
        'image_link': 'https://findrandomlink.com/sf',
        'facebook_link':'https://facebook.com/randomlink_sf'},
        {'id': 2, 
        'name': 'Matt Quevedo',
        'city': 'New York',
        'state': 'New York',
        'phone':'013444555',
        'genres':'Pop',
        'image_link':'https://anotherlink.ch',
        'facebook_link':'https://facebookdummylink.de'},
        {'id': 3, 
        'name': 'The Wild Sax Band',
        'city': 'San Francisco',
        'state': 'California',
        'phone':'123444999',
        'genres':'Jazz',
        'image_link':'https://randomlink123.com',
        'facebook_link':'https://www.facebook.com'},
        {'id': 4, 
        'name': 'The Singing Scots',
        'city': 'Boston',
        'state': 'Massachusets',
        'phone':'444555666',
        'genres':'Folk',
        'image_link':'https://linktosite.com',
        'facebook_link':'https://linktofacebook.com'}]


cursor.executemany(
  SQL_ARTISTS, 
  data_artists
  )


connection.commit()
connection.close()
cursor.close()