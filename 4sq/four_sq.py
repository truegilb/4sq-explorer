import json
import logging
import util as u

D_4SQ_SECRET=""
D_4SQ_ID=""
D_4SQ_VER="v=20131107"

def init_secret():
    global D_4SQ_SECRET, D_4SQ_ID
    j = u.loadfile( 'secret.json')
    D_4SQ_SECRET = "client_secret=" + j['4sq_secret'] 
    D_4SQ_ID= "client_id=" + j['4sq_id']
    logging.info( D_4SQ_SECRET )
    logging.info( D_4SQ_ID )

def venue_categories():
    global D_4SQ_SECRET, D_4SQ_ID, D_4SQ_VER
    vcategories_url = "https://api.foursquare.com/v2/venues/categories?" + \
        D_4SQ_VER + "&" + D_4SQ_ID + "&" + D_4SQ_SECRET
    return vcategories_url

