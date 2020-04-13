from app import Venue, Artist 
# from app import Show
import psycopg2

connection = psycopg2.connect("dbname = fyyur")
cursor = connection.cursor()

SQL_VENUES = '''
INSERT INTO venues 
      (name, 
      city, 
      state, 
      address, 
      phone, 
      image_link, 
      facebook_link) 
    VALUES 
      (%(name)s,
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
        'state': 'CA',
        'address':'Dummy Road 1',
        'phone':'123456789',
        'image_link': 'https://i.pinimg.com/originals/9e/d8/de/9ed8de2926da9936d7161c5aba3b7ab5.jpg',
        'facebook_link':'https://facebook.com/randomlink_sf'},
        {'id': 2, 
        'name': 'The Dueling Pianos Bar',
        'city': 'New York',
        'state': 'NY',
        'address':'Default Avenue 3',
        'phone':'013444555',
        'image_link':'https://www.schatzalp.ch/wp-content/uploads/PianoBar2-1200x800.jpg',
        'facebook_link':'https://facebookdummylink.de'},
        {'id': 3, 
        'name': 'Park Square Live Music & Coffee',
        'city': 'San Francisco',
        'state': 'CA',
        'address':'Random Way 333',
        'phone':'123444999',
        'image_link':'https://images.toubiz.de/image/big2/40497_04.jpg',
        'facebook_link':'https://www.facebook.com'},
        {'id': 4, 
        'name': 'Kafana',
        'city': 'New York',
        'state': 'NY',
        'address':'Belgrade Street 3',
        'phone':'444555666',
        'image_link':'https://i1.wp.com/tasteserbia.com/wp-content/uploads/2014/12/kafana.jpg?fit=1300%2C697&ssl=1',
        'facebook_link':'https://linktofacebook.com'}]

cursor.executemany(
  SQL_VENUES, 
  data_venues
  )


SQL_ARTISTS = '''
INSERT INTO artists 
      (name, 
      city, 
      state, 
      phone, 
      genres, 
      image_link, 
      facebook_link) 
    VALUES 
      (%(name)s,
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
        'image_link': 'https://chesterfieldsbarandgrill.com/wp-content/uploads/2017/07/Band-2007-760222.jpg',
        'facebook_link':'https://facebook.com/randomlink_sf'},
        {'id': 2, 
        'name': 'Matt Quevedo',
        'city': 'New York',
        'state': 'New York',
        'phone':'013444555',
        'genres':'Pop',
        'image_link':'https://upload.wikimedia.org/wikipedia/commons/a/aa/Bob_Dylan_and_The_Band_-_1974.jpg',
        'facebook_link':'https://facebookdummylink.de'},
        {'id': 3, 
        'name': 'Park Square Live Music & Coffee',
        'city': 'San Francisco',
        'state': 'California',
        'phone':'123444999',
        'genres':'Jazz',
        'image_link':'https://xspass.ch/media/cache/fb_image_thumb/product-images/11/07/3/20er%20Jahre%20Jazz%20Band%20Wanddeko%20521781550743206.6896.jpg?1550743206',
        'facebook_link':'https://www.facebook.com'},
        {'id': 4, 
        'name': 'The Singing Scots',
        'city': 'Boston',
        'state': 'Massachusets',
        'phone':'444555666',
        'genres':'Folk',
        'image_link':'https://upload.wikimedia.org/wikipedia/commons/6/6b/The_Band_of_The_Royal_Regiment_of_Scotland.jpg',
        'facebook_link':'https://linktofacebook.com'}]


cursor.executemany(
  SQL_ARTISTS, 
  data_artists
  )

connection.commit()
connection.close()
cursor.close()
