import subprocess
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
from ffmpeg_quality_metrics import FfmpegQualityMetrics

bit1280 = [512, 1024, 2048, 3072]
bit640 = [96, 128, 256,384, 612, 1024, 2048]
bit320 = [64, 96, 128, 256, 512, 1024]

bitrates = [bit320, bit640, bit1280]
resolutionNames = ["320x138","640x274","1280x548"]

def convertToMP4Lossy(resolution: str, rate: int):
        subprocess.run(f'''ffmpeg -s {resolution} -i SourceVideo\\dancing{resolution}.yuv -b:v {rate}k 
            -c:v libx264 -preset slow OutputVideo\\compressed_{resolution}_{rate}.mp4''',shell = True)

def convertMP4ToYUVLossless(resolution: str, rate: int):
    subprocess.run(f'''ffmpeg -i OutputVideo\\compressed_{resolution}_{rate}.mp4 -c:v libx264 OutputVideo\\compressed_{resolution}_{rate}.yuv''',shell=True)

def upscale(resolution: str, UpDimensions: str, rate: int):
    subprocess.run(f'''ffmpeg -i OutputVideo\\compressed_{resolution}_{rate}.yuv -vf scale={UpDimensions}:flags=lanczos 
        -c:v libx264 -preset slow -crf 21 OutputVideo\\upscaled_{resolution}_{rate}_{UpDimensions}.yuv''',shell=True)

def convertToMP4Lossless(resolution: str):
        subprocess.run(f'''ffmpeg -s {resolution} -i SourceVideo\\dancing{resolution}.yuv SourceVideo\\compressed_lossless.mp4''',shell = True)

def runProcess(resolution, rates):
    for _rate in rates:
        print(_rate)
        convertToMP4Lossy(resolution,_rate)
        convertMP4ToYUVLossless(resolution,_rate)
        upscale(resolution, "1280x548",_rate)
        ffqm = FfmpegQualityMetrics(f"OutputVideo\\upscaled_{resolution}_{_rate}_1280x548.yuv ", "SourceVideo\\compressed_lossless.mp4")
        metrics = ffqm.calculate(["psnr"])
        #print(ffqm.get_global_stats()["ssim"]["ssim_y"]["average"])
        print(ffqm.get_global_stats()["psnr"]["psnr_avg"]["average"])
        psnrs.append(ffqm.get_global_stats()["psnr"]["psnr_avg"]["average"])

convertToMP4Lossless("1280x548")

for index in range(len(bitrates)):
    psnrs = []
    runProcess(resolutionNames[index], bitrates[index])
    plt.plot(bitrates[index], psnrs, label = resolutionNames[index], marker = 'o')

plt.title('Bitrate against PSNR')
plt.xlabel('Bitrate')
plt.ylabel('PSNR')
plt.legend()
plt.show()