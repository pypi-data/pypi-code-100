



from io import BytesIO
import struct
from Crypto import Random




class BinContainer1(object):

	################################################################################################################################
	## Constants
	################################################################################################################################

	__MAGIC = b"BLKJK10\x00"
	__RNG = Random.new()

	################################################################################################################################
	## Constructor Methods
	################################################################################################################################

	def __init__(self):
		self.__blocks = []
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __pad(self, rawBinData) -> tuple:
		assert isinstance(rawBinData, (bytes, bytearray))

		alignmentInBytes = 4

		nOrgDataLen = len(rawBinData)
		assert nOrgDataLen <= 2147483647
		orgMsgLenByteArray = struct.pack("<I", nOrgDataLen)

		nPaddingBytes = (alignmentInBytes - nOrgDataLen) % alignmentInBytes
		paddingData = BinContainer1.__RNG.read(nPaddingBytes)

		return bytes(orgMsgLenByteArray), bytes(rawBinData), bytes(paddingData)
	#

	def __unpad(self, rawBinData) -> bytes:
		assert isinstance(rawBinData, (bytes, bytearray))

		orgMsgLenByteArray = rawBinData[0:4]
		assert len(orgMsgLenByteArray) == 4

		nOrgDataLen = struct.unpack("<I", orgMsgLenByteArray)[0]

		ret = rawBinData[4:4 + nOrgDataLen]
		assert len(ret) == nOrgDataLen
		return bytes(ret)
	#

	def __byteKeyToStrKey(self, raw) -> str:
		assert isinstance(raw, (bytes, bytearray))
		assert len(raw) == 4
		return raw.decode("ascii")
	#

	def __strKeyToByteKey(self, s:str) -> bytes:
		assert isinstance(s, str)
		binKey = s.encode("ascii")
		assert len(binKey) == 4
		return binKey
	#

	def __blockTypeStrToID(self, s:str) -> bytes:
		assert isinstance(s, str)
		while len(s) < 4:
			s += " "
		binKey = s.encode("ascii")
		assert len(binKey) == 4
		return binKey
	#

	def __blockTypeIDToStr(self, raw) -> str:
		assert isinstance(raw, (bytes, bytearray))
		assert len(raw) == 4
		return raw.decode("ascii").strip()
	#

	################################################################################################################################
	## Magic Methods
	################################################################################################################################

	def __bytes__(self):
		return bytes(self.toByteArray())
	#

	def __len__(self):
		return len(self.__blocks)
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def toBytes(self) -> bytes:
		return bytes(self.toByteArray())
	#

	def toByteArray(self) -> bytes:
		ret = bytearray(BinContainer1.__MAGIC)

		for binKey, blockType, data in self.__blocks:
			ret.extend(binKey)
			ret.extend(self.__blockTypeStrToID(blockType))
			if blockType == "bin":
				for x in self.__pad(data):
					ret.extend(x)
			else:
				raise Exception()

		return ret
	#

	def clear(self):
		self.__blocks.clear()
	#

	def writeToFile(self, filePath:str):
		assert isinstance(filePath, str)

		with open(filePath, "wb") as fout:
			fout.write(bytes(self))
	#

	def loadFromFile(self, filePath:str):
		assert isinstance(filePath, str)

		with open(filePath, "rb") as fin:
			self.loadFromData(fin.read())
	#

	def dump(self):
		print("BinContainer1[")
		for binKey, blockType, data in self.__blocks:
			print("\tid=" + repr(self.__byteKeyToStrKey(binKey)) + ", type=" + repr(blockType) + ", length=" + str(len(data)))
		print("]")
	#

	def loadFromData(self, bytedata):
		assert isinstance(bytedata, (bytes, bytearray))

		blocks = []
		b = BytesIO(bytedata)
		
		if b.read(len(BinContainer1.__MAGIC)) != BinContainer1.__MAGIC:
			raise Exception("Not a binary container.")

		alignmentInBytes = 4

		while True:
			binKey = b.read(4)
			if not binKey:
				break
			assert len(binKey) == 4

			binTypeID = b.read(4)
			if not binTypeID:
				break
			assert len(binTypeID) == 4
			typeID = self.__blockTypeIDToStr(binTypeID)

			orgMsgLenByteArray = b.read(4)
			assert len(orgMsgLenByteArray) == 4
			nOrgDataLen = struct.unpack("<I", orgMsgLenByteArray)[0]
			nPaddingBytes = (alignmentInBytes - nOrgDataLen) % alignmentInBytes
			nBlockSize = nOrgDataLen + nPaddingBytes

			raw = b.read(nBlockSize)
			blocks.append((binKey, typeID, raw[:nOrgDataLen]))

		self.__blocks = blocks
	#

	def addBinaryBlock(self, key:str, bytedata):
		binKey = self.__strKeyToByteKey(key)
		assert isinstance(bytedata, (bytes, bytearray))
		bytedata = bytes(bytedata)

		self.__blocks.append((binKey, "bin", bytedata))
	#

	def getBlockByKey(self, key:str) -> tuple:
		binKey = self.__strKeyToByteKey(key)

		for binKeyStored, blockType, dataStored in self.__blocks:
			if binKeyStored == binKey:
				return blockType, dataStored

		return None
	#

	def getBlockByIndex(self, index:int) -> tuple:
		assert isinstance(index, int)
		if (index >= 0) and (index < len(self.__blocks)):
			raw = self.__blocks[index]
			return self.__byteKeyToStrKey(raw[0]), raw[1], raw[2]

		return None
	#

	def getBlockByKeyE(self, key:str) -> tuple:
		binKey = self.__strKeyToByteKey(key)

		for binKeyStored, blockType, dataStored in self.__blocks:
			if binKeyStored == binKey:
				return blockType, dataStored

		raise Exception("No such block: " + repr(key))
	#

	def getBlockByIndexE(self, index:int) -> tuple:
		assert isinstance(index, int)
		if (index >= 0) and (index < len(self.__blocks)):
			raw = self.__blocks[index]
			return self.__byteKeyToStrKey(raw[0]), raw[1], raw[2]

		raise Exception("No such block: " + str(index))
	#

#














