import subprocess
import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.ndimage

bitrate = [100, 110,120,140]
qp = [10, 20, 30, 40]

bit720 = [512, 1024, 2048, 3072]
bit360 = [96, 128, 256,384, 612, 1024, 2048]
bit180 = [64, 96, 128, 256, 512, 1024]

#https://write.corbpie.com/upscaling-and-downscaling-video-with-ffmpeg/#:~:text=All%20you%20need%20to%20do,to%20make%20it%20at%201080p.

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


#for _rate in bitrate:

#subprocess.run(f'''ffmpeg -i dancing_org.mp4 -b:v {100}k -vcodec: libx264 -psnr out_{100}.mp4''', shell=True)


Y,U,V = readYUV420('D:\\Personal\\College\\5thYear\\Motion Picture Engineering\\Assignment 2\\SourceVideo', (1280,720),True)
Y2x = scipy.ndImage.zoom(Y, (1,2,3))

#subprocess.run(f'''ffmpeg -i input.mp4 -vf scale=1920x1080:flags=lanczos -c:v libx264 -preset slow -crf 21 output_compress_1080p.mp4''')

print(f'original dim: {Y.shape}, new dim: {Y2x.shape}')

plt.imshow(Y[0])
plt.imshow