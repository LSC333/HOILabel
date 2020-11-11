
def readTxT(filePath):
    with open(filePath, 'r') as file:
        lines = file.readlines()
        fileContent = [line.strip() for line in lines]
    return fileContent
