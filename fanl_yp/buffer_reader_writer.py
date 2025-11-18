from fanl_yp.types import Vector3Uint8, Vector3Uint16, Vector3Float
import struct
import zlib

class BufferReader:
    def __init__(self, buffer):
        self.view = buffer
        self.offset = 0

    def readUint8(self):
        uint8 = self.view[self.offset]
        self.offset += 1
        return uint8
    
    def readUint16(self, littleEndian=True):
        endian = "little"
        if not littleEndian:
            endian = "big"
        uint16 = int.from_bytes(self.view[self.offset: self.offset + 2], endian)
        self.offset += 2;
        return uint16
    
    def readUint32(self, littleEndian=True):
        endian = "little"
        if not littleEndian:
            endian = "big"
        uint32 = int.from_bytes(self.view[self.offset: self.offset + 4], endian)
        self.offset += 4
        return uint32
    
    def readFloat32(self, littleEndian=True):
        endian = "<"
        if not littleEndian:
            endian = ">"
        float32 = struct.unpack(endian +  "f", self.view[self.offset: self.offset + 4])
        self.offset += 4
        return float32[0]
    
    def readInt32(self, littleEndian=True):
        endian = "little"
        if not littleEndian:
            endian = "big"
        int32 = int.from_bytes(self.view[self.offset: self.offset + 4], endian, signed=True)
        self.offset += 4
        return int32
    
    def readString(self):
        length = self.readUint8()
        string = self.view[self.offset:self.offset + length].decode("UTF-8")
        self.offset += length
        return string
    
    def readVec3Uint8(self):
        return Vector3Uint8(self.readUint8(), self.readUint8(), self.readUint8())

    def readVec3Uint16(self):
        return Vector3Uint16(self.readUint16(), self.readUint16(), self.readUint16())

    def readVec3Float32(self):
        return Vector3Float(self.readFloat32(), self.readFloat32(), self.readFloat32())
    
    def readBuffer(self, size=1):
        buffer = self.view[self.offset:self.offset + size]
        self.offset += size
        return buffer

class Buffer:
    def __init__(self, fileNameAndPath: str, mode):
        self.fileName = fileNameAndPath
        self.mode = mode
        self.byteStream = bytes()
    
    def write(self, byteStream: bytes):
        self.byteStream += byteStream
    
    def flush(self):
        file = open(self.fileName, self.mode)
        file.write(zlib.compress(self.byteStream))
        file.close()
    
class BufferWriter:
    def __init__(self, bufferNameAndPath: str):
        self.offset = 0
        self.buffer = Buffer(bufferNameAndPath, "bw")
        self.endian = "little"

    def writeUint8(self, value: int):
        self.buffer.write(int(value).to_bytes(1))
        self.offset += 1

    def writeUint16(self, value: int, littleEndian = True):
        self.buffer.write(int(value).to_bytes(2, self.endian))
        self.offset += 2

    def writeUint32(self, value: int, littleEndian = True):
        self.buffer.write(int(value).to_bytes(4, self.endian))
        self.offset += 4

    def writeFloat32(self, value: float, littleEndian = True):
        self.buffer.write(struct.pack("<f", value))
        self.offset += 4

    def writeInt32(self, value: int, littleEndian = True):
        self.buffer.write(int(value).to_bytes(4, self.endian, signed=True))
        self.offset += 4

    def writeString(self, value: str, littleEndian = True):
        stringLenght = len(value)
        self.writeUint8(stringLenght)
        self.buffer.write(value.encode("UTF-8"))
        self.offset += stringLenght + 1

    def writeVec3Uint8(self, value: Vector3Uint8):
        x, y, z = value
        self.writeUint8(x)
        self.writeUint8(y)
        self.writeUint8(z)

    def writeVec3Uint16(self, value: Vector3Uint16, littleEndian=True):
        x, y, z = value
        self.writeUint16(x)
        self.writeUint16(y)
        self.writeUint16(z)

    def writeVec3Float32(self, value: Vector3Float, littleEndian=True):
        x, y, z = value
        self.writeFloat32(x)
        self.writeFloat32(y)
        self.writeFloat32(z)
