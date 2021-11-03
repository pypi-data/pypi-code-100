
#####################################################################
#
# s_confg.py
#
# Project   : SAPIADAPTER
# Author(s) : Zafar Iqbal < zaf@sparc.space >
# Copyright : (C) 2021 SPARC PC < https://sparc.space/ >
#
# All rights reserved. No warranty, explicit or implicit, provided.
# SPARC PC is and remains the owner of all titles, rights
# and interests in the Software.
#
#####################################################################

import os
import sys
import json
import time

#####################################################################

from . import get_version
from . import s_log  , s_util

#####################################################################

config = { }
config_alt = { }

config_ready = False

#####################################################################

def setup( ) :
    global config_ready
    if init( ) :
        config_ready = True
        return

    s_log.write( "Not ready!" )

def config_ready_get( ) :
    return(config_ready)


def get_config( ) :
    return config

def set_key( config_key , config_val ) :
    global config
    #s_log.write( "CONFIG SET_KEY " + config_key + " = " + str( config_val ) )
    config[ config_key ] = config_val
    return True

def set_key_alt( config_key , config_val ) :
    global config_alt
    #s_log.write( "CONFIG SET_KEY " + config_key + " = " + str( config_val ) )
    config_alt[ config_key ] = config_val
    return True

def del_key_alt( kn ) :
    global config_alt
    #s_log.write_msg("GET KEY "+config_key)
    if( kn in config_alt ) :
        #s_log.write_msg("GET KEY FOUND")
        config_alt.pop( kn )
        return True
            
    #s_log.write_msg("GET KEY NULL")
    return False

def get_key( config_key , default_val = None ) :

    if( config_key in config_alt ) :
        #s_log.write_msg("GET KEY FOUND")
        if config_alt[ config_key ] != None :
            return config_alt[ config_key ]
 

    #s_log.write_msg("GET KEY "+config_key)
    if( config_key in config ) :
        #s_log.write_msg("GET KEY FOUND")
        if config[ config_key ] != None :
            return config[ config_key ]
            
    #s_log.write_msg("GET KEY NULL")
    return default_val

def del_key( kn ) :
    #s_log.write_msg("GET KEY "+config_key)
    if( kn in config ) :
        #s_log.write_msg("GET KEY FOUND")
        config.pop( kn )
        return True
            
    #s_log.write_msg("GET KEY NULL")
    return False

def init_fromfile( config_path , config_key = "sapiadapter" ) :

    global config

    #s_log.write( os.getcwd( ) + "," + config_path )

    try :

        with open( config_path ) as f :
            config_all = json.load( f )
    
    except IOError :

        s_log.write( "config init_fromfile IOError " + config_path )
        return False

    ####################################################################

    if config_key in config_all :
        config.update( config_all[ config_key ] )
        config["config/init_fromfile" ] = "yes"
        config["config/init_fromfile_path"] = config_path
    else :
        s_log.write( "ERROR config_key " + config_key )
        return False

    ####################################################################

    #s_log.write( "LOADED " + config_path )

    #s_log.write( config )

    return True

################################################################

def init( config_user = None ) :

    global config

    config = { }

    # Use "/..." for internal config keys...

    config[ "/config/init/time" ] = time.time( )
    config[ "/config/version" ] = get_version( )
    config[ "/config/cwd" ] = os.getcwd( )
    config[ "/config/scriptdir" ] = os.path.dirname( os.path.realpath( __file__ ) )
    config[ "/config/maindir" ] = os.path.dirname( sys.modules[ "__main__" ].__file__ )
    config[ "/config/session" ] = s_util.uhash( )

    s_log.write( config )

    if( config_user ) :
        config.update( config_user )
        config[ "/config/init/user" ] = "yes"
        return( True ) 

    ################################################################

    # First check env variable SAPIADAPTER
    if( "SAPIADAPTER " in os.environ ) :
        s_log.write( "Found env var SAPIADAPTER_CONFIGURATION" )
        if( init_fromfile( os.environ[ "SAPIADAPTER_CONFIGURATION" ] ) ) :
            s_log.write( "Loaded SAPIADAPTER_CONFIGURATION " + os.environ[ "SAPIADAPTER_CONFIGURATION" ] )
            config[ "/config/init/init_fromfile" ] = "environ"
            return( True )
        else :
            return( False )

    s_log.write( "Not found env var SAPIADAPTER_CONFIGURATION" )

    ################################################################

    config_default_filename = "local_sapiadapter_config.json"

    # Lets check current directory for config file

    if os.path.isfile( config_default_filename ) :
        if( init_fromfile( config_default_filename ) ) :
            s_log.write( "Loaded " + config_default_filename )
            config[ "/config/init/init_fromfile" ] = "cwd"
            return( True )
        return( False )

    s_log.write( "Not found " + os.getcwd( ) + "/" + config_default_filename )

    ################################################################

    # Lets check tests directory for config file
    testpath = "tests/data/"
    if os.path.isfile( testpath + config_default_filename ) :
        if( init_fromfile( testpath + config_default_filename ) ) :
            s_log.write( "Loaded " + testpath + config_default_filename )
            config[ "/config/init/init_fromfile" ] = "tests"
            return( True )
        return( False )

    ################################################################

    # Lets check 'main' directory for config file
    testpath = config[ "/config/maindir" ] +"/" + config_default_filename
    if os.path.isfile( testpath ) :
        if( init_fromfile( testpath ) ) :
            s_log.write( "Loaded " + testpath )
            config[ "/config/init/init_fromfile" ] = "main"
            return( True )
        return( False )

    s_log.write( "Not found " + os.getcwd( ) + "/" + testpath + config_default_filename )

    return( True )
