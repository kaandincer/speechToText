from threading import Thread
from queue import Queue
import time
import pyaudio
import subprocess
import json
from vosk import Model, KaldiRecognizer

# threads: python concept. Function that run in the background. Don't interrupt main function.
# Can record audio simultaneously

messages = Queue()  # tell the thread when to start and stop
recordings = Queue()  # store audio and pass to transcriptor

# VARIABLES: OPTIMIZING FOR SPEECH RECOGNITION
CHANNELS = 1
FRAME_RATE = 16000
RECORD_SECONDS = 20
AUDIO_FORMAT = pyaudio.paInt16
SAMPLE_SIZE = 2

p = pyaudio.PyAudio()  # initialize pyaudio connection to system devices
for i in range(p.get_device_count()):
    print(p.get_device_info_by_index(i))

p.terminate()

def record_microphone(chunk=1024):
    p = pyaudio.PyAudio()

    stream = p.open(format=AUDIO_FORMAT,
                    channels=CHANNELS,
                    rate=FRAME_RATE,
                    input=True,
                    input_device_index=1,
                    frames_per_buffer=chunk)
    frames = []

    while not messages.empty():
        # as long as there is a message in the queue keep recording
        data = stream.read(chunk)
        frames.append(data)

        if len(frames) >= (FRAME_RATE * RECORD_SECONDS) / chunk:
            recordings.put(frames.copy())
            frames = []

    stream.stop_stream()
    stream.close()
    p.terminate()


model = Model(model_name="vosk-model-en-us-0.22")
rec = KaldiRecognizer(model, FRAME_RATE)
rec.SetWords(True)


def speech_recognition():
    while not messages.empty():
        frames = recordings.get()
        rec.AcceptWaveform(b''.join(frames))
        result = rec.Result()
        text = json.loads(result)["text"]
        print(text)

def start_recording():
    messages.put(True)  # tell thread to keep running and recording (put a message in the msgs queue)

    print("Recording...")
    record = Thread(target=record_microphone)  # creating thread that will record microphone
    record.start()

    transcribe = Thread(target=speech_recognition)
    transcribe.start()


def stop_recording():
    messages.put(False)  # Stop the recording thread
    print("Stopped.")


if __name__ == "__main__":
    print("Start recording? y/n")
    print("Press 's' to stop.")
    choice = input("Enter your choice: ")

    if choice == "y":
        start_recording()
    elif choice == "n":
        print("Sounds good!")
    elif choice == "s":
        stop_recording()
    else:
        print("Invalid choice. Please try again.")
