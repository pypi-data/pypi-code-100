
#####################################################################
#
# s_net.py
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

import time
import requests
import gzip
import socket
import urllib3

urllib3.disable_warnings( urllib3.exceptions.InsecureRequestWarning )

#from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout 

from . import s_log , s_config , s_util , s_db

session = requests.Session( )

#####################################################################

# FIXME TODO - Should really check all the way through to OMNIBUS

check_connectivity_done = False

def check_connectivity( ) :

    global check_connectivity_done

    if( check_connectivity_done ) : return( True )

    ################################################################

    flag_networkok = True

    ################################################################

    endpoint_url =  s_config.get_key( "endpoint/url" )
    if( not endpoint_url ):
        s_log.write( "False endpoint_url" )
        return( False )

    endpoint_parseurl = urllib3.util.parse_url( endpoint_url )

    if( endpoint_parseurl.scheme == None ) :
        s_log.write( "False endpoint_url scheme " + endpoint_url )
        return( False )


    #s_log.write( endpoint_parseurl.scheme)
    #s_log.write( endpoint_parseurl.hostname )
    #s_log.write( endpoint_parseurl.port )

    ################################################################

    if( s_util.is_ip( endpoint_parseurl.hostname ) ) :
        #s_log.write("check_connectivity s_util.is_ip")
        s_config.set_key_alt( "endpoint/sslverify" , "no" )
    
    ################################################################

    endpoint_url_port = endpoint_parseurl.port
    if( endpoint_url_port == None ) :
        endpoint_url_port = 443

    ################################################################

    #s_log.write( endpoint_parseurl.hostname )
    #s_log.write( endpoint_parseurl.port )

    if( s_config.get_key( "endpoint/skipnetworkcheck1" ) != "yes" ) : 
        try :

            host = socket.gethostbyname( endpoint_parseurl.hostname ) 
            s = socket.create_connection( ( host , endpoint_url_port ) , 30 )
            s.close( )

        except Exception as e :
            s_log.write( "False check_connectivity 1" )
            flag_networkok = False


    ################################################################

    headers =   {
                    "User-Agent" : "sapiadapter" ,
                    "X-Omni-Authorization" : s_config.get_key( "endpoint/token" ) ,
                    "X-Omni-Action": "mwget" ,
                }

    endpoint_host = s_config.get_key( "endpoint/host" )

    if endpoint_host != None and endpoint_host != "" :
        headers[ "Host" ] = endpoint_host

    if( flag_networkok and get_request_response( headers ) == False ) :
        s_log.write( "False check_connectivity 2" )
        flag_networkok = False

    ################################################################

    check_connectivity_done = flag_networkok

    if flag_networkok :
        return( True )

    endpoint_host =  s_config.get_key( "endpoint/host" , "HOST_NOT_SET")
    s_log.write( endpoint_parseurl.hostname + "," + endpoint_parseurl.hostname + "," + str( endpoint_url_port ) + "," + endpoint_host )

    return( False )

#####################################################################


def job_request( ) :

    db_filecontents = s_db.file_contents( )

    payload = gzip.compress( db_filecontents  )

    mw = mw_get( )
    if( not mw ) : return( False )

    #####################################################################

    headers =   {
                    "User-Agent" : "sapiadapter" ,
                    "X-Omni-Mw": mw ,
                    "X-Omni-Authorization": s_config.get_key( "endpoint/token" ) ,
                    "X-Omni-Action": "job_request" ,
                }

    endpoint_host = s_config.get_key( "endpoint/host" )
    if endpoint_host != None and endpoint_host != "" :
        headers[ "Host" ] = endpoint_host

    #s_log.write( headers )

    res = get_request_response( headers , payload )

    if( res == False ) :
        s_log.write( "res??" )
        return( False )

    #s_log.write( str( res.headers ))

    #####################################################################

    if( not "X-Omni-Jid" in res.headers ) :
        s_log.write( "Not found X-Omni-Jid" )
        return( False )

    if( len( res.headers[ "X-Omni-Jid" ] ) != 67 ) :
        s_log.write( "X-Omni-Jid!=67" )
        return( False )

    jid = res.headers[ "X-Omni-Jid" ]

    s_log.write( "job_request [" + jid + "]" )

    return( jid )


def job_responsewait( jid , timeout = 60 ) :

    s_log.write( "job_wait " + str( timeout ) )
    
    time_start = time.time( )

    while True :
        jr = job_response( jid )
        if( jr == False ) : return( False )
        if( jr == True ) : return( True )
        if( time.time( ) - time_start ) > timeout : return( None )

def job_response( jid ) :

    s_db.setup( )

    #time.sleep(1)

    #s_db.reset( )

    #####################################################################

    mw = mw_get( )
    if( not mw ) : return( False )

    #####################################################################

    endpoint_host = s_config.get_key( "endpoint/host" )
    endpoint_token = s_config.get_key( "endpoint/token" )

    headers =   {
                    "User-Agent" : "sapiadapter" ,
                    "X-Omni-Mw": mw ,
                    "X-Omni-Authorization": endpoint_token ,
                    "X-Omni-Action": "job_response" ,
                    "X-Omni-Jid": jid ,
                }

    if endpoint_host != None  and endpoint_host != "" :
        headers[ "Host" ] = endpoint_host

    #s_log.write( headers )

    res = get_request_response( headers )

    if( res == False ) :
        s_log.write( "res??" )
        return( False )

    #s_log.write( str(res.headers ) )


    if( not "X-Omni-State" in res.headers ) :
        s_log.write( "Not found X-Omni-State" )
        return( False )

    if( res.headers[ "X-Omni-State" ] != "done" ) :
        s_log.write( "job_response !=Done [" + jid + "]" )
        return( None )


    #b1 = res.content[ -4: ].hex()
    #s_log.write("HEX "+b1)

    payload = gzip.decompress( res.content )

    #s_log.write(hex(len(payload)))

    s_db.rewrite( payload )

    return( True )


def job_get( ) :

    mw = mw_get( )
    if( not mw ) : return( False )

    #####################################################################

    endpoint_host = s_config.get_key( "endpoint/host" )
    endpoint_token = s_config.get_key( "endpoint/token" )

    headers =   {
                    "User-Agent" : "sapiadapter" ,
                    "X-Omni-Mw": mw ,
                    "X-Omni-Authorization": endpoint_token ,
                    "X-Omni-Action": "job_get" ,
                }

    if endpoint_host != None  and endpoint_host != "" :
        headers[ "Host" ] = endpoint_host

    #s_log.write( headers )

    res = get_request_response( headers )

    if( res == False ) :
        s_log.write( "ERROR False res??" )
        return( False )

    #s_log.write( str(res.headers ) )

    if( not "X-Omni-Jid" in res.headers ) :
        s_log.write( "Not found X-Omni-Jid" )
        return( None )

    payload = gzip.decompress( res.content )
    #s_log.write( payload )

    s_db.rewrite( payload )

    if( "X-Omni-Context" in res.headers ) :
        #s_log.write( "Found X-Omni-Context" )
        #s_log.write( res.headers[ "X-Omni-Context" ] )
        s_log.write( "FIXME TODO context json to meta add" )
#        context_json = base64.b64decode( res.headers[ "X-Omni-Context" ] ).decode( "utf-8" )
        context_json = s_util.base64_decode( res.headers[ "X-Omni-Context" ] )
        #s_db.meta_create( "_server_getjob_context_json" , context_json ) 

    if( "X-Omni-Jid" in res.headers ) :
        s_db.meta_create( "_jid" , res.headers[ "X-Omni-Jid" ] ) 
        s_log.write( "job_get [" + res.headers[ "X-Omni-Jid" ] + "]" )

    return( True )

def job_set( jid ) :

    s_db.sys_rev_inc( )

    db_filecontents = s_db.file_contents( )

    payload = gzip.compress( db_filecontents  )
    payload_size = len( payload )
    #s_log.write("YYY "+str(payload_size))

    #####################################################################

    mw = mw_get( )
    if( not mw ) : return( False )

    #####################################################################

    endpoint_host = s_config.get_key( "endpoint/host" )
    endpoint_token = s_config.get_key( "endpoint/token" )

    headers =   {
                    "User-Agent" : "sapiadapter" ,
                    "X-Omni-Mw": mw ,
                    "X-Omni-Authorization": endpoint_token ,
                    "X-Omni-Action": "job_set" ,
                    "X-Omni-Jid": jid ,

                }

    if endpoint_host != None  and endpoint_host != "" :
        headers[ "Host" ] = endpoint_host

    #s_log.write( headers )

    res = get_request_response( headers , payload )

    #####################################################################

    if( res == False ) :
        # Remember res is false!
        s_log.write( "ERROR res??" )
        return( False )

    #s_log.write( str(res.headers ) )

    #s_log.write( "job_set [" + jid + "]" )

    return( True )

#####################################################################


def mw_get( ) :
    mw1 = get_mw( )
    if( mw1 == False ) :
        s_log.write( "ERROR False get_mw" )
        return( False )
    mw = "MWCf068980781d390b52666900ee6d4cce11ac2e9e8e175a9c3293e35659911df5a" + mw1
    mw = s_util.hash( mw.encode( "utf-8" ) , "MWH" )
    #s_log.write(mw)
    return( mw )

def get_mw( ) :

    headers =   {
                    "User-Agent" : "sapiadapter" ,
                    "X-Omni-Authorization" : s_config.get_key( "endpoint/token" ) ,
                    "X-Omni-Action": "mwget" ,
                }

    endpoint_host = s_config.get_key( "endpoint/host" )
    if endpoint_host != None and endpoint_host != "" :
        headers[ "Host" ] = endpoint_host

    #s_log.write( headers )

    res = get_request_response( headers )

    if( res == False ) :
        s_log.write( "ERROR get_mw false res" )
        return( False )

    #s_log.write(str(res.headers))

    if( not "X-Omni-Mw" in res.headers ) :
        s_log.write( "ERROR Not found X-Omni-Mw" )
        return( False )

    if( len( res.headers[ "X-Omni-Mw" ] ) != 67 ) :
        s_log.write( "ERROR X-Omni-Mw!=67" )
        return( False )

    mw = res.headers[ "X-Omni-Mw" ]

    #s_log.write(mw)

    if( "X-Omni-Wait" in res.headers ) :
        #s_log.write( "Found X-Omni-Wait " + res.headers[ "X-Omni-Wait" ] )
        time.sleep( int( res.headers[ "X-Omni-Wait" ] ) )

    return( mw )

#####################################################################

def get_request_response( request_headers = { }  , payload = "" ) :

    # When empty headers the host must be set
    if( request_headers == { } ) :
        request_headers[ "User-Agent" ] = "sapiadapter" 
        endpoint_host = s_config.get_key( "endpoint/host" )
        if endpoint_host != None and endpoint_host != "" :
            request_headers[ "Host" ] = endpoint_host

    request_headers[ "X-Omni-Traceid" ] = s_log.get_traceid( )   

    ################################################################ 

    endpoint_sslverify = s_config.get_key( "endpoint/sslverify" )

    if endpoint_sslverify == None :

        endpoint_sslverify = True
    else :        
        if endpoint_sslverify == "yes":
            endpoint_sslverify = True
        else :
            endpoint_sslverify = False

    ################################################################ 

    endpoint_timeout = s_config.get_key( "endpoint/timeout" )
    if endpoint_timeout == None or ( not endpoint_timeout.isdigit( ) ) :
        endpoint_timeout = 60 
    else:
        endpoint_timeout = int( endpoint_timeout )

    endpoint_url = s_config.get_key( "endpoint/url" ) 
    if( not endpoint_url ) :
        s_log.write( "false endpoint_url" )
        return( False )

    if(not endpoint_url.endswith("/")):
        endpoint_url=endpoint_url+"/"

    endpoint_url = endpoint_url + "api.html"
    #s_log.write(endpoint_url)

    #####################################################################

    try :
        #response = requests.post( endpoint_url , data = payload , headers = request_headers , timeout = endpoint_timeout , verify = endpoint_sslverify )
        response = session.post( endpoint_url , data = payload , headers = request_headers , timeout = endpoint_timeout , verify = endpoint_sslverify )

    except requests.exceptions.SSLError as e :
        s_log.write( "ERROR requests.exceptions.SSLError:" + str( e ) )
        return( False )    
    except requests.exceptions.ReadTimeout as e :
        s_log.write( endpoint_url)
        s_log.write( "ERROR requests.exceptions.ReadTimeout:" + str( e ) )
        return( False )    
    except requests.exceptions.ConnectionError as e :
        s_log.write( "ERROR requests.exceptions.ConnectionError::" + str( e ) )
        s_log.write( "ERROR Maybe no omnibus..?" )
        s_log.write( endpoint_url )
        s_log.write( request_headers )
        return( False )  

    #####################################################################

    if( ( response.status_code != 200 ) and ( response.status_code != 418 ) ) :
        s_log.write( "ERROR status_code" )
        s_log.write( endpoint_url )
        s_log.write( request_headers )
        s_log.write( response.status_code )
        if( response.status_code == 404 ) :
            s_log.write( "Check endpoint url" )
        if( response.status_code == 502 ) :
            s_log.write( "ERROR 502" )

        return( False )

    #####################################################################

    return( response )

#####################################################################

    