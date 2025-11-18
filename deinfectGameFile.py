import fanl_yp
import zlib

gameFilePath = input("Please insert the path to the game file: ")

gameFile = open(gameFilePath, "br")
data = zlib.decompress(gameFile.read())
gameFile.close()
game = fanl_yp.decode.decode(data)

removeFile = open("./remove", "br")
data = zlib.decompress(removeFile.read())
removeFile.close()
remove = fanl_yp.decode.decode(data)

indexOffset = game.indexOffset
offset = 0

mode = input("1 Remove by ID\n2 Hold by ID\nSelect a mode [1-2]: ")

print()
print(f"IndexOffset: {indexOffset}\n")
print("Removable lock IDs:")
for objectContainer in game.objectContainers:
    if objectContainer.headerReader.hasVoxels():
        print(f"  {offset} {objectContainer.name}")
    offset += 1

print()

if mode == "1":
    getIDs = input("Enter the IDs you want to remove: ")
    IDList = getIDs.split(",")
    for ID in IDList:
        game.objectContainers[int(ID)] = remove.objectContainers[1]

elif mode == "2":
    getIDs = input("Enter the IDs you want to Hold: ")
    IDList = getIDs.split(",")
    IDSet = set()
    for ID in IDList:
        IDSet.add(int(ID))
    for objectContainerID in range(len(game.objectContainers)):
        if game.objectContainers[objectContainerID].headerReader.hasVoxels():
            if IDSet.__contains__(objectContainerID):
                continue
            game.objectContainers[objectContainerID] = remove.objectContainers[1]

output = fanl_yp.encode.encode(game, gameFilePath + "_fixed")
output.flush()