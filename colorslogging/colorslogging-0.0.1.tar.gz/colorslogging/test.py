from colorslogging import ColoredFormatter

logger = ColoredFormatter.CusGetLogger(cus_color = 35 ,cus_level = 'NMD' , cus_level_name = 'nmd' , custom_level_num = 29 )
logger.nmd('awesome')
logger = ColoredFormatter.GetLogger()
logger.success('awesome')