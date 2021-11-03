from packagebuilder import packagebuilder as pb
import sys, logging
logging.basicConfig(level = logging.DEBUG, format = "%(message)s")
def init_arguments():
	arguments = []
	for index, each in enumerate(sys.argv):
		if (index):
			arguments.append(each)
	return arguments
def build_package(arguments, limit_argument = 3):
	if (len(arguments) > limit_argument):
		logging.debug(f"Error: Expected at most {limit_argument} arguments but received {len(arguments)}.\n")
	elif (len(arguments)):
		pb.Builder(*arguments)
build_package(init_arguments())
