import json
import re

### Utility functions
###
def srcimg( url ):
    """Insert the <img src/> tag for html output
    """
    return( '<img src="' + url + '"/>' )

def newline( string ):
    """Insert the <p/> tag for html output
    """
    return( '<p>' + string + '</p>' )

def loadfile( filename ):
    """Utility function to load a JSON object from said file name
    """
    try:
        fp = file( filename, 'r')
        try:
            obj = json.load(fp)
        finally:
            fp.close()
    except IOError:
        raise
    return obj

def unittest():
    j = loadfile( 'secret.json' )
    print j['4sq_id']
