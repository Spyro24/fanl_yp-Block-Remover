import fanl_yp
from fanl_yp.buffer_reader_writer import BufferWriter
from fanl_yp.types import Setting

def encode(game: fanl_yp.types.Game, fileNameAndPath: str):
    writer = BufferWriter(fileNameAndPath)

    writer.writeUint16(game.fileVersion)
    writer.writeString(game.title)
    writer.writeString(game.author)
    writer.writeString(game.description)
    writer.writeUint16(game.indexOffset)
    writer.writeUint16(len(game.objectContainers))

    for objectContainer in game.objectContainers:
        header = objectContainer.Header(objectContainer.header)
        writer.writeUint16(header.bits)

        if header.hasType():
            writer.writeUint8(objectContainer.type)
    
        if header.hasName():
            writer.writeString(objectContainer.name)
        
        if header.hasData1():
            if objectContainer._data1 != None:
                writer.writeUint8(objectContainer._data1)
            else:
                writer.writeUint8(0)
        
        if header.hasData2():
            writer.writeUint32(objectContainer._data2)
        
        if header.hasBackground():
            writer.writeUint8(objectContainer.backgroundColor)
        
        if header.hasCollider():
            writer.writeUint8(objectContainer.collider)
        
        if header.inGroup():
            writer.writeUint16(objectContainer.group.index)
            writer.writeVec3Uint8(objectContainer.group.position)
        
        if header.hasVoxels():
            def writeFaces(faces):
                for face in faces:
                    writer.writeUint8(face)
            writeFaces(objectContainer.faces.positiveX)
            writeFaces(objectContainer.faces.negativeX)
            writeFaces(objectContainer.faces.positiveY)
            writeFaces(objectContainer.faces.negativeY)
            writeFaces(objectContainer.faces.positiveZ)
            writeFaces(objectContainer.faces.negativeZ)

        if header.hasBlocks():
            writer.writeVec3Uint16(objectContainer.tiles.size)
            for block in objectContainer.tiles.blocks:
                writer.writeUint16(block)
        
        if header.hasSettings():
            writer.writeUint16(len(objectContainer.settings))
            for setting in objectContainer.settings:
                writer.writeUint8(setting.index)
                writer.writeUint8(setting.type)
                writer.writeVec3Uint16(setting.position)

                value = setting.value
                valType = setting.type
                if valType == setting.Types["Byte"]:
                    writer.writeUint8(value)
                elif valType == setting.Types["Short"]:
                    writer.writeUint16(value)
                elif valType == setting.Types['Int']:
                    writer.writeInt32(value)
                elif valType == setting.Types["Float"]:
                    writer.writeFloat32(value)
                elif valType == setting.Types["Vec"]:
                    writer.writeVec3Float32(value)
                else:
                    writer.writeString(value)
    
        if header.hasConnections():
            writer.writeUint16(len(objectContainer.connections))
            for connection in objectContainer.connections: 
                writer.writeVec3Uint16(connection.position["from"])
                writer.writeVec3Uint16(connection.position["to"])
                writer.writeVec3Uint16(connection.offset["from"])
                writer.writeVec3Uint16(connection.offset["to"])

    return writer.buffer
