import picamera
import picamera.array
import time
from automl import evaluate
import boto3
import vlc
from time import sleep

client = boto3.client('polly', region_name='us-east-1')

threshold = 50    # required pixel change
sensitivity = 100  # amount of pixels changes

def speek(text):
    response = client.synthesize_speech(
        OutputFormat='mp3',
        Text=text,
        TextType='text',
        VoiceId='Brian'
    )
    audio_stream = response['AudioStream'].read()
    response['AudioStream'].close()

    with open('temp.mp3', 'w') as f:
        f.write(audio_stream)
    
    vlc.MediaPlayer('temp.mp3').play()

# print(response)
def takeFrame(width, height):
    with picamera.PiCamera() as camera:
        time.sleep(1)
        camera.resolution = (width, height)
        with picamera.array.PiRGBArray(camera) as stream:
            camera.exposure_mode = 'auto'
            camera.awb_mode = 'auto'
            camera.capture(stream, format='rgb')
            return stream.array

# take a frame of what the camera  sees.


def scanFrameChange(width, height):
    frameChng = False
    data1 = takeFrame(width, height)  # comparison of two
    while not frameChng:
        data2 = takeFrame(width, height)
        diffCount = 0
        for w in range(0, width):
            for h in range(0, height):
                diff = abs(int(data1[h][w][1]) - int(data2[h][w][1]))
                if diff > threshold:
                    diffCount += 1
            if diffCount > sensitivity:
                break
        if diffCount > sensitivity:
            frameChng = True
        else:
            data2 = data1
    return frameChng


def changeDetect():
    print("Detecting motion...")
    speek("Detecting motion...")
    while True:
        if scanFrameChange(224, 160):
            print("Motion detected")
            speek("Motion detected")
            with picamera.PiCamera() as camera:
                camera.resolution = (1024, 768)
                camera.start_preview()
                # Camera warm-up time
                time.sleep(1)
                camera.capture('temp.jpg')
                camera.close()
                evaluate()


if __name__ == '__main__':
    try:
        changeDetect()
    finally:
        print("Exiting Program")
