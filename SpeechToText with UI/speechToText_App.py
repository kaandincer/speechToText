# import sys
# sys.path.append("/Users/kaandincer/Library/Python/3.9/lib/python/site-packages")
import streamlit as st # house all the code for web app. Provides with input/output widgets.
# from docx import Document
import websockets # interact with Assembly AI
import asyncio # perform audio input and output in concurrent manner
import base64 # encode and decode audio signals before sent to api
import json # read in audio output (transcribe text)
import pyaudio # accept audio input processing
import os # for navigating through the various files in the project and file processing
from pathlib import Path

# Describing session state (memory of the web app)
if 'text' not in st.session_state:
	st.session_state['text'] = 'Listening...' # if running for the first time, session state text equals listening
	st.session_state['run'] = False
	st.session_state['recording_name'] = ''
	st.session_state['recorded_files'] = []  # New key for recorded files

# Audio parameters. We create a sidebar to set audio parameters 
st.sidebar.header('Audio Parameters')

# Web user interface
st.title('Auto-Document')
st.header('🎙️ Record Your Meeting Notes')

with st.expander('About this App'):
	st.markdown('''
	This web app uses the AssemblyAI API to perform real-time speech to text transcription.
	
	Things to note:
	- If you want to change the look of the web app or other settings, click the 3 bars on the upper right corner of your screen, and click settings. 
	- If you want to change audio parameters of your recording, click the arrow on the upper left corner, and set the numbers. 
	- We reccomend keeping the parameters at their pre-set levels. 
	- Click the "Download Meeting Notes" to download the transcription (of your meeting) to your local device.
	''')

recording_name = st.text_input('Enter a name for the recording:')
st.session_state['recording_name'] = recording_name

# # Display the chosen recording name
# if st.session_state['recording_name']:
#     st.write(f"Recording Name: {st.session_state['recording_name']}")

FRAMES_PER_BUFFER = int(st.sidebar.text_input('Frames per buffer', 3200))
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = int(st.sidebar.text_input('Rate', 16000))
p = pyaudio.PyAudio()

# Open an audio stream with above parameter settings
stream = p.open(
   format=FORMAT,
   channels=CHANNELS,
   rate=RATE,
   input=True,
   frames_per_buffer=FRAMES_PER_BUFFER
)

# Start/stop audio transmission
def start_listening():
	st.session_state['run'] = True

def download_transcription():
	file_name = f"{st.session_state['recording_name'] or 'meeting_recording'}.txt"
	read_txt = open('transcription.txt', 'r')
	st.download_button(
		label="Download Meeting Notes",
		data=read_txt,
		# file_name='meeting_recording.txt',
		file_name = file_name,
		mime='text/plain')

# .docx download
# def download_transcription():
#     document = Document()
#     document.add_paragraph(st.session_state['text'])

#     document.save('transcription_output.docx')

#     st.download_button(
#         label="Download Meeting Notes",
#         data='transcription_output.docx',
#         file_name='transcription_output.docx',
#         mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
#     )

def stop_listening():
	st.session_state['run'] = False

start, stop = st.columns(2)

start.button('Start', on_click=start_listening)
stop.button('Stop', on_click=stop_listening)

# Send audio (Input) / Receive transcription (Output)
async def send_receive():
	URL = f"wss://api.assemblyai.com/v2/realtime/ws?sample_rate={RATE}"

	print(f'Connecting websocket to url ${URL}')

	async with websockets.connect(
		URL,
		extra_headers=(("Authorization", st.secrets['api_key']),),
		ping_interval=5,
		ping_timeout=20
	) as _ws:

		r = await asyncio.sleep(0.1)
		print("Receiving messages ...")

		session_begins = await _ws.recv()
		print(session_begins)
		print("Sending messages ...")


		async def send():
			while st.session_state['run']:
				try:
					data = stream.read(FRAMES_PER_BUFFER)
					data = base64.b64encode(data).decode("utf-8")
					json_data = json.dumps({"audio_data":str(data)})
					r = await _ws.send(json_data)

				except websockets.exceptions.ConnectionClosedError as e:
					print(e)
					assert e.code == 4008
					break

				except Exception as e:
					print(e)
					assert False, "Not a websocket 4008 error"

				r = await asyncio.sleep(0.01)


		async def receive():
			while st.session_state['run']:
				try:
					result_str = await _ws.recv()
					result = json.loads(result_str)['text']

					if json.loads(result_str)['message_type']=='FinalTranscript':
						print(result)
						st.session_state['text'] = result
						st.write(st.session_state['text'])

						transcription_txt = open('transcription.txt', 'a')
						transcription_txt.write(st.session_state['text'])
						transcription_txt.write(' ')
						transcription_txt.close()


				except websockets.exceptions.ConnectionClosedError as e:
					print(e)
					assert e.code == 4008
					break

				except Exception as e:
					print(e)
					assert False, "Not a websocket 4008 error"
			
		send_result, receive_result = await asyncio.gather(send(), receive())


asyncio.run(send_receive())

# After clicking on stop, download button shows, from this code. 
if Path('transcription.txt').is_file():
	st.markdown('### Download')
	st.sidebar.markdown('### Recorded Files')
	download_transcription()
	os.remove('transcription.txt')

# References (Code modified and adapted from the following)
# 1. https://github.com/misraturp/Real-time-transcription-from-microphone
# 2. https://medium.com/towards-data-science/real-time-speech-recognition-python-assemblyai-13d35eeed226
# 3. https://www.youtube.com/watch?v=8rb9GefC_CU