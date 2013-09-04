# http://webapp-improved.appspot.com/guide/request.html#post-data
# http://docs.webob.org/en/latest/do-it-yourself.html
# 
import webapp2

### top level class
#
class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello, this is a prototype for Rating backend for iPass Hackathon.')

# network id (bssid is used here), then a tuple containing average rating and 
# number of rating submissions
#

class RatingBase():
    rating_base = { 
                'd4:a0:2a:cc:e2:60' : ( 3.0, 1 ),
                'd8:c7:c8:20:14:80' : ( 3.0, 1 ),
                'c4:01:7c:08:12:68' : ( 3.0, 1 ),
                '02:02:6f:ed:52:5c' : ( 3.0, 1 ),
                'e4:ce:8f:40:e3:56' : ( 3.0, 1 ),
                '00:0f:12:82:0a:b7' : ( 3.0, 1 ),
                '18:3d:a2:2c:ea:88' : ( 3.0, 1 ),
                }
    def getRatingByNetwork( self, network_key ):
        if network_key not in self.rating_base.keys():
            return -1
        else:
            return self.rating_base[ network_key ][0]

    def getAllRatings(self):
        r = {}
        for k in self.rating_base.keys():
            r[ k ] = self.rating_base[k][0]
        return r

    def submitRating( self, networkId, rating):
        k = networkId
        if k not in self.rating_base.keys():
            rating_base[ k ] = ( rating, 1 )
        else:
            old_rating = self.rating_base[ k ][ 0 ]
            old_occurrence = self.rating_base[ k ][ 1 ]
            new_rating = (old_rating * old_occurrence + float(rating)) / ( old_occurrence + 1)
            # update
            self.rating_base[ k ] = ( new_rating, (old_occurrence + 1) )
        return

    def showAllRatings(self):
        r = {}
        for k in self.rating_base.keys():
            r[ k ] = self.rating_base[ k ]

        return r

# Instantiate the rating "database"
#
x = RatingBase()

# for readability - display just the rating
#
class ShowRatings( webapp2.RequestHandler ):
    def get(self):
        ratings = x.getAllRatings()
        for k in ratings.keys():
            self.response.write( '<p> id=' + k + ' => rating=' + str(ratings[ k ]) + '</p>' )

# display rating and # of submissions
#
class ShowAllRatings( webapp2.RequestHandler):
    def get(self):
        r = x.showAllRatings()
        for k in r.keys():
            self.response.write( '<p> id=' + k + ' => rating=' + str(r[k]) + '</p>' )

# for submission
# http://127.0.0.1:8080/submit?networkID=411&rating=2.0
# http://127.0.0.1:8080/submit?networkID=00:0f:12:82:0a:b7&rating=5.0
#
class SubmitRating( webapp2.RequestHandler ):
    def get(self):
        networkId = str(self.request.get( "networkID" ))
        rating = self.request.get( "rating" )
        x.submitRating( networkId, rating)
        self.response.write( 'OK' )

# for retrieval to display by client
# http://127.0.0.1:8080/get?networkID=00:0f:12:82:0a:b7
# 
class GetRating( webapp2.RequestHandler ):
    def get(self):
        networkId = self.request.get( "networkID" )
        r = x.getRatingByNetwork( str(networkId) )
        self.response.write( '{ \"networkID\" : \"' + networkId + '\" ,' )
        self.response.write( '  \"rating\" : \"' + str(r) + '\" }\n' )

class GetAllRatings( webapp2.RequestHandler ):
    def get(self):
        self.response.write( '[ ' )
        ratings = x.getAllRatings()
        for k in ratings.keys():
            self.response.write( '{ \"networkID\" : \"' + k + '\" ,')
            self.response.write( '  \"rating\" : \"' + str(ratings[k]) + '\" } ')
            if k != ratings.keys()[-1]:
                self.response.write( ',' )
        self.response.write( ' ]' )

app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),
    ('/submit', SubmitRating),
    ('/show', ShowRatings),
    ('/showall', ShowAllRatings),
    ('/get', GetRating),
    ('/getall', GetAllRatings),
], debug=True)

#myhost = '127.0.0.1'
myhost=''
#myhost = '192.168.42.15'
def main():
    from paste import httpserver
    httpserver.serve(app, myhost, port='8080')

if __name__ == '__main__':
    main()
