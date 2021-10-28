import os

c="sxbutils"

def do_stuff():
    m=c+".do_stuff"
    print (m+" 0.0.14") # <- Update/Match this with ../*setup*

def validate_envvars(envvars):

    m=c+".validate_envvars"
    print(m+" Starts")

    count=0
    try:
       for envvar in envvars:
          count += 1
          if not envvar.name in os.environ and envvar.required:
              message=m+" missing envvar ("+envvar.name+") and it is required"
              raise Exception(message)
          print(m+" envvar="+envvar.name+" value="+str(os.environ.get(envvar.name)))

    except Exception as e:
       message=m+" An exception occurred, error="+str(e)+""
       raise Exception(message)

    finally:
       print(m+" Finally")

    print(m+" validated "+str(count)+" envvars")

