# -*- coding: utf-8 -*-

import webapp2
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
import json
import re

### Util functions
###
def newline( string ):
    return( '<p>' + string + '</p>' )

def srcimg( url ):
    return( '<img src="' + url + '"/>' )

def obfuscate_url( url ):
    p = re.compile( r'client_.*?\=.*?\&' )
    return p.sub( '***', url )

def photo_details_url( photo_id ):
    return (vphotos_details_prefix + photo_id + '?' + _4SQ_ID + '&' + 
            _4SQ_SECRET + '&' + _4SQ_VER )

### Handle routes
###
class RootWebapp2(webapp2.RequestHandler):
    readme = ''
    def get(self):
        try:
            readme = open( 'readme.html', 'r').read()
        except:
            # assign static text if readme file is not there
            readme = 'Source of photo is from Four Square.'
        self.response.write( readme )

_4SQ_SECRET = 'client_secret=C3NRU0VFSG2GYXXJXZTZC0NM5A0TTY2FOBFIMEYJBXD44P1S'
_4SQ_ID="client_id=5BN0AMHK3WLKIOOTWSUIFFWGWWUN3QERYT5LOT5JNZLQZC4H"
_4SQ_VER="v=20131011" # random version number for now, req'd by 4sq API
_4SQ_LIMIT="limit=6"

#venuesearch_prefix = "https://api.foursquare.com/v2/venues/search?ll=37.4828,-122.2361"
venuesearch_prefix = "https://api.foursquare.com/v2/venues/search?"

vcategories_url = "https://api.foursquare.com/v2/venues/categories?v=1&" + _4SQ_ID + "&" + _4SQ_SECRET

# https://developer.foursquare.com/docs/venues/photos
# e.g. https://api.foursquare.com/v2/venues/VENUE_ID/photos
#
vphotos_url_prefix = "https://api.foursquare.com/v2/venues/"
vphotos_url_suffix = "/photos"

# Photo details
# https://developer.foursquare.com/docs/photos/photos
# e.g. https://api.foursquare.com/v2/photos/PHOTO_ID
#
vphotos_details_prefix = "https://api.foursquare.com/v2/photos/"

class GetVenue(webapp.RequestHandler):
    def get(self):
        nearstr = self.request.get("near")
        if (not nearstr):
            locstr="ll=37.4828,-122.2361"
        else:
            locstr="near=" + nearstr

        querystr = ""
        try: 
            querystr = self.request.get( "query" )
        except:
            print "get err"

        self.response.write(  newline( 'query =' + querystr ))
        # search for venue first
        #
        venue_search_url = (venuesearch_prefix + _4SQ_ID + '&' + 
                            _4SQ_SECRET + "&limit=5" + "&" + _4SQ_VER + '&' + locstr)
        if (querystr ):
            venue_search_url = venue_search_url + "&query=" + querystr 
            
        r = urlfetch.fetch( venue_search_url )
        j = json.loads( r.content )        

        if (j['meta']['code'] != 200):
            self.response.write( newline("API error"))
            self.response.write( newline( r.content ))
            return

        numVenues = len(j['response']['venues'] )
        if ( numVenues == 0): # search returns nothing
            self.response.write( newline( "No venue found with that query"))
            return
        else:
            self.response.write( newline( str(numVenues) + 
                                          ' venue found. Showing the first one.'))

        first_result = j['response']['venues'][0]
        venue_id = j['response']['venues'][0]['id']
        self.response.write( newline( obfuscate_url(venue_search_url ) ))
        self.response.write( newline( 'venue id = ' + venue_id) )
        self.response.write( newline( 'venue name = ' + first_result['name'] ) )
        self.response.write( newline( str(first_result['location']) ) )

        # get some photos
        rr = urlfetch.fetch( vphotos_url_prefix + venue_id + '/photos?' + _4SQ_VER + '&' + 
                             _4SQ_ID + "&" + _4SQ_SECRET)
 #        self.response.write (rr.content )

        jj = json.loads( rr.content)
        jjstr = jj['response']
        jjstr_pretty = json.dumps( jjstr, indent=2, separators=(',',':'))
#       self.response.write( jjstr_pretty) 

        # now let's get the photos
        # there maybe a level 'groups' between photos and items (if ver unmatched)
        #
        jjphotos = jj['response']['photos']['items']
        if ( len(jjphotos) < 1):
            self.response.write( newline( 'No photos found at this venue.' ))
        for p in jjphotos:
            p_url = p['prefix'] + 'original' + p['suffix']
            # self.response.write( newline(p['visibility']) )
            self.response.write( newline(str(p['source']) ))
            self.response.write( srcimg( p_url ))

class VenueCategories(webapp2.RequestHandler):
    def get(self):
        r = request.get( vcategories_url )
        print vcategories_url
        j = json.loads( r.content )
        jstr = j['response']
        jjstr = json.dumps( jstr, indent=2, separators=(',', ': '))
        self.response.write( jjstr )

        # list the categories
        numCategories = len(j['response']['categories'])
        print numCategories
        for v in j['response']['categories']:
            print "> " + v['name']
            # then sub-categories
            for vv in v['categories']:
                if ( vv ):
                    # need utf8 encode because of words like Cafes
                    print " >> " + vv['name'].encode('utf-8')

app = webapp2.WSGIApplication([
    ('/', RootWebapp2),
    ('/venue', GetVenue),
    ('/venuecat', VenueCategories),
], debug=True)

myhost = ''
def main():
    from paste import httpserver
    httpserver.serve(app, myhost, port='8080')

if __name__ == '__main__':
    main()
