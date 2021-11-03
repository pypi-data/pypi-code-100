import logging

def omit(filelist):
    try:
        if ".DS_Store" in filelist:
            filelist.remove(".DS_Store")
        return filelist
    except Exception as e:
        logging.error(e)
        logging.error("****")

