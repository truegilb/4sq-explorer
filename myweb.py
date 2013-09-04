# http://webapp-improved.appspot.com/guide/request.html#post-data
# http://docs.webob.org/en/latest/do-it-yourself.html
# 
import webapp2
# import Request

### these classes are just for testing
#
class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello, this is a prototype for Rating backend for iPass Hackathon.')

class AnotherWebapp2(webapp2.RequestHandler):
    def get(self):
        get_name = self.request.get("name")
        self.response.write('Hello, this is one level deep!' + get_name )

# network id (bssid is used here), then a tuple containing rating info and other stuff
#
rating_dict = { 
                'd4:a0:2a:cc:e2:60' : ( 3.0 ),
                'd8:c7:c8:20:14:80' : ( 3.0 ),
                'c4:01:7c:08:12:68' : ( 3.0 ),
                '02:02:6f:ed:52:5c' : ( 3.0 ),
                'e4:ce:8f:40:e3:56' : ( 3.0 ),
                '00:0f:12:82:0a:b7' : ( 3.0 ),
                }

class RatingBase:
    def get():
        return

# for readability
#
class ShowRatings( webapp2.RequestHandler ):
    def get(self):
        for k in rating_dict.keys():
            self.response.write( '<p> id=' + k + ' => rating=' + rating_dict[ k ] + '</p>' )

# for submission
# http://127.0.0.1:8080/submit?networkID=411&rating=2.0
#
class SubmitRating( webapp2.RequestHandler ):
    def get(self):
        networkId = str(self.request.get( "networkID" ))
        rating = self.request.get( "rating" )
        rating_dict[ networkId ] = rating
        self.response.write( 'OK' )

# for retrieval to display by client
#
class GetRating( webapp2.RequestHandler ):
    def get(self):
        networkId = self.request.get( "networkID" )
        if str(networkId) not in rating_dict.keys():
            rating = 'id not found'
        else:
            rating = rating_dict[ networkId ]
        self.response.write( '{ \'rating\' : \'' + str(rating) + '\' }\n' )

class GetAllRatings( webapp2.RequestHandler ):
    def get(self):
        self.response.write( '[ ' )
        for k in rating_dict.keys():
            self.response.write( '{ \"networkID\" : \'' + k + '\" ,')
            self.response.write( '  \"rating\" : \"' + str(rating_dict[k]) + '\" }, ')
        self.response.write( ' ]' )

app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),
    ('/submit', SubmitRating),
    ('/show', ShowRatings),
    ('/get', GetRating),
    ('/getall', GetAllRatings),
], debug=True)

#myhost = '127.0.0.1'
myhost = '192.168.42.15'
def main():
    from paste import httpserver
    httpserver.serve(app, myhost, port='8080')

if __name__ == '__main__':
    main()
