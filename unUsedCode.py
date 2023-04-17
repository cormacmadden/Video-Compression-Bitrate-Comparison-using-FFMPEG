
def readYUV420(name: str, resolution: tuple, upsampleUV: bool = False):
    height = resolution[0]
    width = resolution[1]
    bytesY = int(height * width)
    bytesUV = int(bytesY/4)
    Y = []
    U = []
    V = []
    with open(name,"rb") as yuvFile:
        while (chunkBytes := yuvFile.read(bytesY + 2*bytesUV)):
            Y.append(np.reshape(np.frombuffer(chunkBytes, dtype=np.uint8, count=bytesY, offset = 0), (width, height)))
            U.append(np.reshape(np.frombuffer(chunkBytes, dtype=np.uint8, count=bytesUV, offset = bytesY),  (width//2, height//2)))
            V.append(np.reshape(np.frombuffer(chunkBytes, dtype=np.uint8, count=bytesUV, offset = bytesY + bytesUV), (width//2, height//2)))
    Y = np.stack(Y)
    U = np.stack(U)
    V = np.stack(V)
    if upsampleUV:
        U = U.repeat(2, axis=1).repeat(2, axis=2)
        V = V.repeat(2, axis=1).repeat(2, axis=2)
    return Y, U, V

def writeYUV420(name: str, Y, U, V, downsample=True):
    Y = Y.astype(np.uint8)
    U = U.astype(np.uint8)
    V = V.astype(np.uint8)
    towrite = bytearray()
    if downsample:
        U = U[:, ::2, ::2]
        V = V[:, ::2, ::2]
    for i in range(Y.shape[0]):
        towrite.extend(Y[i].tobytes())
        towrite.extend(U[i].tobytes())
        towrite.extend(V[i].tobytes())
    with open(name, "wb") as destination:
        destination.write(towrite)