import subprocess
import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.ndimage as ndi
import ffmpeg
from ffmpeg_quality_metrics import FfmpegQualityMetrics

bitrate = [100, 110,120,140]
qp = [10, 20, 30, 40]

bit1280 = [512, 1024, 2048, 3072]
bit640 = [96, 128, 256,384, 612, 1024, 2048]
bit320 = [64, 96, 128, 256, 512, 1024]

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

psnrs = []
for _rate in bit1280:
    print(_rate)
    #subprocess.run(f'''ffmpeg -i dancing.1280x548.mp4 ''')
    subprocess.run(f'''ffmpeg -i dancing.1280x548.yuv -b:v {_rate}k -vcodec: libx264 -flags +psnr out_{_rate}.mp4''',capture_output=True, text=True)
    subprocess.run(f'''ffmpeg -i out_{_rate}.mp4 -vf scale=1280x548:flags=lanczos -c:v libx264 -preset slow -crf 21 out_{_rate}_upscaled_720p.mp4''')
    ffqm = FfmpegQualityMetrics(f"out_{_rate}_upscaled_720p.mp4", "dancing_org.mp4")
    metrics = ffqm.calculate(["ssim", "psnr"])
    print(ffqm.get_global_stats()["ssim"]["ssim_y"]["average"])
    print(ffqm.get_global_stats()["psnr"]["psnr_avg"]["average"])
    psnrs.append(ffqm.get_global_stats()["psnr"]["psnr_avg"]["average"])

plt.plot(bit1280, psnrs)
plt.title('Rate against PSNR')
plt.xlabel('Bitrate')
plt.ylabel('PSNR')
plt.show()
#Y,U,V = readYUV420('D:\\Personal\\College\\5thYear\\Motion Picture Engineering\\Assignment 2\\SourceVideo\\dancing_org.1280x548.yuv', (1280,548),True)
#Y2x = ndi.zoom(Y, 2.0)



#print(f'original dim: {Y.shape}, new dim: {Y2x.shape}')

#plt.imshow(Y[0])
#plt.show()