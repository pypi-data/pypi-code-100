

from io import BytesIO


def fileOpen(fileName: BytesIO | str) -> tuple[str, bytes]:
	if isinstance(fileName, str):
		fileName = fileName
		file = open(fileName, "rb")
	else:
		fileName = fileName.name
		file = fileName
	data = file.read()
	file.close()
	return fileName, data


def save(data:bytes, tofileName: BytesIO|str=None):
	"""Save this gimp image to a file."""
	if hasattr(tofileName, "write"):
		file = tofileName
	else:
		file = open(tofileName, "wb")
	file.write(data)
	file.close()
