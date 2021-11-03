
#####################################################################
#
# sapiadapter.py
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

from . import s_log , s_config , s_net , s_util , s_db , s_cleanup

#####################################################################

s_log.write( "    ####    ####    ####    ####\n" )

#####################################################################

s_config.setup( )
s_db.setup( )

#s_log.write( s_config.get_key( "/config/version" ) ) 

#####################################################################

def ready( ) :
    if( not s_config.config_ready_get( ) ) :
        return( False )

    if( not s_net.check_connectivity( ) ) :
        return( False )

    return( True )

def prexit( msg ) :
    s_util.printexit( "FALSE tables" )

def defout( ) :
    return( s_db.files_get_defaultdata( ) )

def uptime( ) :
    return( s_util.uptime( ) )

#####################################################################

# DATA
# TIMEOUT
def express( meta_inputs = { } , wait_timeout = 60 ) :

    if( not ready( ) ) :
        s_log.write( "NOT READY" )
        return( False )

    if( not meta_inputs ) :
        s_log.write( "false meta_inputs " )
        return( False )

    if( not isinstance( meta_inputs , ( dict ) ) ) :
        s_log.write( "false meta_inputs dict" )
        return( False )

    #####################################################################

    s_db.setup( )

    #####################################################################

    f = s_db.meta_create( "_" , meta_inputs ) 

    if( not f ) :
        s_log.write( "false meta_add " + k )
        return( False )

    #####################################################################

    jid = s_net.job_request( )

    #####################################################################

    if( jid == False ) :
        s_log.write( "false job_request jid" )
        return( False )

    #####################################################################

    jr = s_net.job_responsewait( jid , wait_timeout )

    if( jr == False ) :
        s_log.write( "false job_wait" )
        return( False )

    if( jr == None ) :
        s_log.write( "none job_wait" )
        return( None )

    #####################################################################

    #s_log.write(s_util.uptime())

    if( s_db.stdio_has_stderr( ) ) :
        s_log.write( s_db.stdio_get_stderr( ) )
        return( None )

    #####################################################################

    return( s_db.meta_read( "_" ) )
