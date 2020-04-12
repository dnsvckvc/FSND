from app import Venue, Artist, Show, db


show1 = Show(start_time="2019-05-21T21:30:00.000Z")
show1.venue = 1
show1.artist = 1

show2 = Show(start_time="2035-04-01T20:00:00.000Z")
show2.venue = 3
show2.artist = 2

show3 = Show(start_time="2035-04-08T20:00:00.000Z")
show3.venue = 3
show3.artist = 3

show4 = Show(start_time="2035-04-15T20:00:00.000Z")
show4.venue = 3
show4.artist = 3
   
db.session.add(show1)
db.session.add(show2)
db.session.add(show3)
db.session.add(show4)

db.session.commit()