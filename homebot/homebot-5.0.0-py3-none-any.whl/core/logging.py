from logging import basicConfig, debug, info, error, warning, INFO

basicConfig(format='[%(asctime)s] [%(filename)s:%(lineno)s %(levelname)s] %(funcName)s: %(message)s',
					level=INFO)

LOGD = debug
LOGI = info
LOGE = error
LOGW = warning
