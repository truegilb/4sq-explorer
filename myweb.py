# http://docs.webob.org/en/latest/do-it-yourself.html
# 
import webapp2
# import Request

### these classes are just for testing
#
class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello, give me some routes!')

class AnotherWebapp2(webapp2.RequestHandler):
    def get(self):
        get_name = self.request.get("name")
        self.response.write('Hello, this is one level deep!' + get_name )

# popid, then a tuple containing rating info
#
rating_dict = { '100' : ( '5 star' ), '200' : ( '3 star' ) }

# for readability
#
class ShowRatings( webapp2.RequestHandler ):
    def get(self):
        for k in rating_dict.keys():
            self.response.write( k + ' ' + rating_dict[ k ] + '\n' )

# for submission
#
class SubmitRating( webapp2.RequestHandler ):
    def get(self):
        return

# for retrieve to display by client
#
class GetRating( webapp2.RequestHandler ):
    def get(self):
        networkId = self.request.get( "networkID" )
        if networkId not in rating_dict.keys():
            rating = -1
        else:
            rating = rating_dict[ networkId ]
        self.response.write( '( rating : ' + rating + '\n' )
        return

app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),
    ('/submit', SubmitRating),
    ('/show', ShowRatings),
    ('/get', GetRating),
], debug=True)

myhost = '127.0.0.1'
#myhost = '10.10.200.18'
def main():
    from paste import httpserver
    httpserver.serve(app, myhost, port='8080')

if __name__ == '__main__':
    main()
