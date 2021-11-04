# do not forget to keep a three-number version!!!
import datetime
_current_year_ = datetime.datetime.now().year

__SSTool_VERSION__ = "0.0.1"

url = 'https://github.com/JosepFanals/Hyosung'

about_msg = "SSTool v" + str(__SSTool_VERSION__) + '\n\n'

about_msg += """
State Space Tool aimed at stability analysis of power systems.
Developed by CITCEA\n"""

about_msg += """
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to
redistribute it under certain conditions.\n
SSTool is licensed under the MIT license.
The source code can be found at:
""" + url + "\n\n"

copyright_msg = 'Copyright (C) 2021-' + str(_current_year_) + ' CITCEA'
