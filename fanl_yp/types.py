import numpy as np

class Game:
    def __init__(self, title="New Game", author="Unknown Author", description="A fancade game.", indexOffset = 597):
        super()
        self.title       = title
        self.author      = author
        self.description = description
        self.indexOffset = indexOffset
        self.fileVersion = 31
        self.objectContainers: list[objectContainer] = []

class Connection:
    def __init__(self):
        self.position = {"from":None, "to":None}
        self.offset   = {"from":None, "to":None}
        self.size = 24

class Header:
    def __init__(self, bits):
        self.bits = bits
        self.BitOffset = {
          "hasConnections": 0,
          "hasSettings": 1,
          "hasBlocks": 2,
          "hasVoxels": 3,
          "inGroup": 4,
          "hasCollider": 5,
          "uneditable1": 6,
          "uneditable2": 7,
          "hasBackground": 8,
          "hasData2": 9,
          "hasData1": 10,
          "hasName": 11,
          "hasType": 12,
          }
    
    def hasConnections(self): return (self.bits >> self.BitOffset["hasConnections"]) & 1
    def hasSettings(self): return (self.bits >> self.BitOffset["hasSettings"]) & 1
    def hasBlocks(self): return (self.bits >> self.BitOffset["hasBlocks"]) & 1
    def hasVoxels(self): return (self.bits >> self.BitOffset["hasVoxels"]) & 1
    def inGroup(self): return (self.bits >> self.BitOffset["inGroup"]) & 1
    def hasCollider(self): return (self.bits >> self.BitOffset["hasCollider"]) & 1
    def uneditable1(self): return (self.bits >> self.BitOffset["uneditable1"]) & 1
    def uneditable2(self): return (self.bits >> self.BitOffset["uneditable2"]) & 1
    def hasBackground(self): return (self.bits >> self.BitOffset["hasBackground"]) & 1
    def hasData2(self): return (self.bits >> self.BitOffset["hasData2"]) & 1
    def hasData1(self): return (self.bits >> self.BitOffset["hasData1"]) & 1
    def hasName(self): return (self.bits >> self.BitOffset["hasName"]) & 1
    def hasType(self): return (self.bits >> self.BitOffset["hasType"]) & 1

    def setConnections(self, value): self.setBit(value, self.BitOffset["hasConnections"])
    def setSettings(self, value): self.setBit(value, self.BitOffset["hasSettings"])
    def setBlocks(self, value): self.setBit(value, self.BitOffset["hasBlocks"])
    def setVoxels(self, value): self.setBit(value, self.BitOffset["hasVoxels"])
    def setGroup(self, value): self.setBit(value, self.BitOffset["inGroup"])
    def setCollider(self, value): self.setBit(value, self.BitOffset["hasCollider"])
    def setUneditable1(self, value): self.setBit(value, self.BitOffset["uneditable1"])
    def setUneditable2(self, value): self.setBit(value, self.BitOffset["uneditable2"])
    def setBackground(self, value): self.setBit(value, self.BitOffset["hasBackground"])
    def setData2(self, value): self.setBit(value, self.BitOffset["hasData2"])
    def setData1(self, value): self.setBit(value, self.BitOffset["hasData1"])
    def setName(self, value): self.setBit(value, self.BitOffset["hasName"])
    def setType(self, value): self.setBit(value, self.BitOffset["hasType"])

    def setBit(self, value, offset):
        if value:
            self.bits |= 1 << offset
        else:
            self.bits &= 0b1111_1111_1111_1111 ^ (1 << offset)

        return self

class Setting:
    def __init__(self):
        self.index = None #np.uint8
        self.position = None #Vector3Uint16
        self.type = None  ### enum Setting.Types
        self.value = None    ### u8 | u16 | i32 | f32 | vec3f32 | string
        self.Types = {
            "Byte": 0x01,
            "Short": 0x02,
            "Int": 0x03,
            "Float": 0x04,
            "Vec": 0x05,
            "Str": 0x06,
            "ExePin": 0x07,
            "NumPin": 0x08,
            "self": 0x09,
            "VecPin": 0x0a,
            "RotPin": 0x0c,
            "TruPin": 0x0e,
            "ObjPin": 0x10,
            "ConPin": 0x12,
            }

class objectContainer:
    def __init__(self):
        self.header: np.uint16
        self.headerReader: Header
        self.type = 0
        self.name: str = None
        self._data1: np.uint8 = None
        self._data2: np.uint32 = None
        self.backgroundColor = None
        self.collider: np.uint8 = 0
        self.group: Group = None
        self.faces: Faces = None
        self.tiles: Tiles = Tiles()
        self.settings: list[Setting] = []
        self.connections: list[Connection] = []
        self.Header: Header = Header

        self.Types = {
            "Normal"  : 0,
            "Physics" : 1,
            "Script"  : 2,
            "Level"   : 3,
            }

        self.Color = {
            "None"         : 0x00,
            "DarkGray"     : 0x01,
            "Gray"         : 0x02,
            "LightGray"    : 0x03,
            "DarkSilver"   : 0x04,
            "Silver"       : 0x05,
            "LightSilver"  : 0x06,
            "DarkBrown"    : 0x07,
            "Brown"        : 0x08,
            "LightBrown"   : 0x09,
            "DarkBeige"    : 0x0A,
            "Beige"        : 0x0B,
            "LightBeige"   : 0x0C,
            "DarkRed"      : 0x0D,
            "Red"          : 0x0E,
            "LightRed"     : 0x0F,
            "DarkOrange"   : 0x10,
            "Orange"       : 0x11,
            "LightOrange"  : 0x12,
            "DarkYellow"   : 0x13,
            "Yellow"       : 0x14,
            "LightYellow"  : 0x15,
            "DarkGreen"    : 0x16,
            "Green"        : 0x17,
            "LightGreen"   : 0x18,
            "DarkBlue"     : 0x19,
            "Blue"         : 0x1A,
            "LightBlue"    : 0x1B,
            "DarkPurple"   : 0x1C,
            "Purple"       : 0x1D,
            "LightPurple"  : 0x1E,
            "DarkMagenta"  : 0x1F,
            "Magenta"      : 0x20,
            "LightMagenta" : 0x21,
            }
        
        self.Collider = {
            "None":    0,
            "Box":     1,
            "Sphere":  2,
            "Surface": 3,
            "Exact":   4,
            }

        self.Group = Group
        self.Faces = Faces
        self.Tiles = Tiles
        self.Default = defaultObjectContainer
    
    def __repr__(self):
        return f"ObjectContainer:\n  - Type: {self.type}\n  - Name: {self.name}\n  - data1: {self._data1}"

class defaultObjectContainer(objectContainer):
    def __init__(self, type_, name):
        super()
        self.type = type_
        self.name = name
    
    def level(self, name, color=None):
        objectContainer = self(self.Types['Level'], name)
        if type(color) == int:
            objectContainer.backgroundColor = color
        return objectContainer
    
    def script(self, name):
        return self(self.Types["Script"], name)
    
    def normal(self, name):
        return self(self.Types['Normal'], name)
    
    def physics(self, name):
        return self(self.Types["Physics"], name)
    
class Group:
    def __init__(self):
        self.index = 0    
        self.position = Vector3Uint8()
        self.size = 5

class Faces:
    def __init__(self):
        self.positiveX = []
        self.negativeX = []
        self.positiveY = []
        self.negativeY = []
        self.positiveZ = []
        self.negativeZ = []
        self.unglueBitOffset = 7
        for n in range(512):
            self.positiveX.append(0)
            self.negativeX.append(0)
            self.positiveY.append(0)
            self.negativeY.append(0)
            self.positiveZ.append(0)
            self.negativeZ.append(0)
        self.size = 3072
        self.voxelArrayLength = 512

class Tiles:
    def __init__(self):
        self.size = Vector3Uint16()
        self.blocks = []

class Vector3Uint8:
  def __init__(self, x=0, y=0, z=0):
    self.x = np.uint8(x)
    self.y = np.uint8(y)
    self.z = np.uint8(z)

  def __iter__(self):
    yield self.x
    yield self.y
    yield self.z

class Vector3Uint16:
    def __init__(self, x=0, y=0, z=0):
        self.x = np.uint16(x)
        self.y = np.uint16(y)
        self.z = np.uint16(z)

    def __iter__(self):
        yield int(self.x)
        yield int(self.y)
        yield int(self.z)

    def __repr__(self):
        return f"Vector3Uit16({self.x}, {self.y}, {self.z})"

class Vector3Float:
    def __init__(self, x=0, y=0, z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z
    
    def __repr__(self):
        return f"Vector3Float({self.x}, {self.y}, {self.z})"
    

def array_from_bytes(bytes_, lengt=1, endian="little"):
    out = []
    readerPos = 0
    maxReaderPos = len(bytes_)
    while readerPos < maxReaderPos:
        out.append(int.from_bytes(bytes_[readerPos: readerPos + lengt], byteorder=endian))
        readerPos += lengt
    return out

def turn_dict(dict_: dict):
    new_dict = {}
    for key in dict_.keys():
        new_dict[dict_[key]] = key
    return new_dict

bg_colors = {1: (23,24,31),
             6: (255, 255, 255),
             23: (86, 197, 107),
             28: (79, 56, 115),
             }

faceColors = {
              0x01: (22, 21, 36),
              0x02: (57, 55, 80),
              0x03: (99, 99, 127),
              0x04: (172, 1774, 193),
              0x05: (228, 229, 240),
              0x06: (255, 255, 255),
              0x07: (141, 79, 88),
              0x08: (179, 102, 122),
            "LightBrown"   : 0x09,
            "DarkBeige"    : 0x0A,
            "Beige"        : 0x0B,
            "LightBeige"   : 0x0C,
              0x0D: (175, 52, 70),
              0x0E: (238, 80, 101),
            "LightRed"     : 0x0F,
            "DarkOrange"   : 0x10,
              0x11: (239, 109, 63),
              0x12: (243, 164, 116),
              0x13: (221, 164, 0),
              0x14: (246, 214, 0),
              0x15: (251, 255, 89),
              0x16: (48, 132, 63),
              0x17: (79, 147, 45),
            "LightGreen"   : 0x18,
            "DarkBlue"     : 0x19,
            "Blue"         : 0x1A,
            "LightBlue"    : 0x1B,
            "DarkPurple"   : 0x1C,
            "Purple"       : 0x1D,
            "LightPurple"  : 0x1E,
            "DarkMagenta"  : 0x1F,
              0x20: (2443, 1433, 202),
              0x21: (247, 14, 240),
              }