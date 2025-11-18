from fanl_yp.types import *
import fanl_yp.types
from fanl_yp.buffer_reader_writer import BufferReader

voxelArrayLength = objectContainer().Faces().voxelArrayLength
littleEndian = True

def decode(buffer) -> fanl_yp.types.Game:
    reader = BufferReader(buffer)
    game = Game()

    game.fileVersion = reader.readUint16()
    game.title       = reader.readString()
    game.author      = reader.readString()
    game.description = reader.readString()
    game.indexOffset = reader.readUint16()
    
    objectContainerCount = reader.readUint16()
    
    for objectContainerNumber in range(objectContainerCount):
        objectContainer = fanl_yp.types.objectContainer()
        objectContainer.header = reader.readUint16()
        header = objectContainer.Header(objectContainer.header)
        objectContainer.headerReader = header
        if header.hasType():
            objectContainer.type = reader.readUint8()
        if header.hasName():
            objectContainer.name = reader.readString()
        
        if header.hasData1():
            objectContainer.data1 = reader.readUint8()
        if header.hasData2():
          objectContainer.data2 = reader.readUint32()
        if header.hasBackground():
            objectContainer.backgroundColor = reader.readUint8()
        if header.hasCollider():
          objectContainer.collider = reader.readUint8()
        if header.inGroup():
          objectContainer.group = objectContainer.Group()
          objectContainer.group.index    = reader.readUint16()
          objectContainer.group.position = reader.readVec3Uint8()
        if header.hasVoxels():
            objectContainer.faces = objectContainer.Faces()

            objectContainer.faces.positiveX = array_from_bytes(reader.readBuffer(voxelArrayLength))
            objectContainer.faces.negativeX = array_from_bytes(reader.readBuffer(voxelArrayLength))
            objectContainer.faces.positiveY = array_from_bytes(reader.readBuffer(voxelArrayLength))
            objectContainer.faces.negativeY = array_from_bytes(reader.readBuffer(voxelArrayLength))
            objectContainer.faces.positiveZ = array_from_bytes(reader.readBuffer(voxelArrayLength))
            objectContainer.faces.negativeZ = array_from_bytes(reader.readBuffer(voxelArrayLength))
        
        if header.hasBlocks():
            objectContainer.tiles = objectContainer.Tiles()
            objectContainer.tiles.size = reader.readVec3Uint16()
            x, y, z = objectContainer.tiles.size
            bufferSize = x * y * z * 2
            slice_ = reader.readBuffer(bufferSize)
            if littleEndian:
                objectContainer.tiles.blocks = array_from_bytes(slice_, lengt=2)
        
        if header.hasSettings():
            settingLength = reader.readUint16()
            objectContainer.settings = []

            for settingCount in range(settingLength):
                setting = Setting()

                setting.index = reader.readUint8();
                setting.type = reader.readUint8();
                setting.position = reader.readVec3Uint16();

                test = setting.type
                if test == setting.Types["Byte"]:
                    setting.value = reader.readUint8()
                elif test == setting.Types["Short"]:
                    setting.value = reader.readUint16()
                elif test == setting.Types["Int"]:
                    setting.value = reader.readInt32()
                elif test == setting.Types["Float"]:
                    setting.value = reader.readFloat32()
                elif test == setting.Types["Vec"]:
                    setting.value = reader.readVec3Float32()
                else:
                    setting.value = reader.readString()

                objectContainer.settings.append(setting)
        if header.hasConnections():
            connectionLength = reader.readUint16()
            objectContainer.connections = []

            for conectionCount in range(connectionLength):
                connection = Connection()

                connection.position['from'] = reader.readVec3Uint16();
                connection.position['to']   = reader.readVec3Uint16();
                connection.offset['from']   = reader.readVec3Uint16();
                connection.offset['to']     = reader.readVec3Uint16();

                objectContainer.connections.append(connection)
        game.objectContainers.append(objectContainer)
    return game
