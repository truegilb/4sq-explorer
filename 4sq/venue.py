import webapp2
import requests
import json
# import StringIO

class HelloWebapp2(webapp2.RequestHandler):
    readme = ''
    def get(self):
        try:
            readme = open( 'readme.html', 'r').read()
        except:
            # assign static text if readme file is not there
            readme = 'Hello, the source is from Four Square.'
        self.response.write( readme )

# sample_url = "https://api.foursquare.com/v2/venues/search?ll=37.4828,-122.2361&client_id=5BN0AMHK3WLKIOOTWSUIFFWGWWUN3QERYT5LOT5JNZLQZC4H&client_secret=C3NRU0VFSG2GYXXJXZTZC0NM5A0TTY2FOBFIMEYJBXD44P1S&v=20131011"
sample_url = "https://api.foursquare.com/v2/venues/search?ll=37.4828,-122.2361&client_id=5BN0AMHK3WLKIOOTWSUIFFWGWWUN3QERYT5LOT5JNZLQZC4H&client_secret=C3NRU0VFSG2GYXXJXZTZC0NM5A0TTY2FOBFIMEYJBXD44P1S&v=20131011&limit=1"

_4SQ_SECRET = 'client_secret=C3NRU0VFSG2GYXXJXZTZC0NM5A0TTY2FOBFIMEYJBXD44P1S'
_4SQ_ID="client_id=5BN0AMHK3WLKIOOTWSUIFFWGWWUN3QERYT5LOT5JNZLQZC4H"

vcategories_url = "https://api.foursquare.com/v2/venues/categories?v=1&" + _4SQ_ID + "&" + _4SQ_SECRET

class GetVenue(webapp2.RequestHandler):
    def get(self):
        r = requests.get( sample_url )
        self.response.write( r.content)

class VenueCategories(webapp2.RequestHandler):
    def get(self):
        r = requests.get( vcategories_url )
        print vcategories_url
        j = json.loads( r.content )
#        jstr = json.dump( j, indent=2, separators=(',', ': '))
        jstr = j['response']
        jjstr = json.dumps( jstr, indent=2, separators=(',', ': '))
        self.response.write( jjstr )
        print jjstr

app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),
    ('/venue', GetVenue),
    ('/venuecat', VenueCategories),
], debug=True)

myhost = ''
def main():
    from paste import httpserver
    httpserver.serve(app, myhost, port='8080')

if __name__ == '__main__':
    main()
