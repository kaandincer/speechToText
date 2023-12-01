import streamlit as st
import requests
from configure import auth_key
import assemblyai as aai

aai.settings.api_key = auth_key

config = aai.TranscriptionConfig(
    speaker_labels=True,
)

if 'status' not in st.session_state:
    st.session_state['status'] = 'submitted'

# new_audio_url = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"

st.title('Easily transcribe audio files')

uploaded_wav_file = st.file_uploader('Upload your WAV file', type=['wav'])
uploaded_mp3_file = st.file_uploader('Upload your MP3 file', type=['mp3'])
st.text("The transcription is " + st.session_state['status'])

upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'
headers_auth_only = {'authorization': auth_key}
headers = {'authorization': auth_key, 'content-type': 'application/json'}
CHUNK_SIZE = 5242880

@st.cache_data
def transcribe_from_wav_or_mp3(audio_file, categories: bool):
    # Upload audio file to AssemblyAI
    upload_response = requests.post(upload_endpoint, headers=headers_auth_only, data=audio_file.getvalue())

    audio_url = upload_response.json()['upload_url']

    # Start the transcription of the audio file
    transcript_request = {
        'audio_url': audio_url,
        'iab_categories': 'True' if categories else 'False',
    }

    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)

    # This is the id of the file that is being transcribed in the AssemblyAI servers
    # We will use this id to access the completed transcription
    transcript_id = transcript_response.json()['id']
    polling_endpoint = transcript_endpoint + "/" + transcript_id

    # Polling loop until transcription is completed
    while True:
        polling_response = requests.get(polling_endpoint, headers=headers)
        st.session_state['status'] = polling_response.json()['status']
        if st.session_state['status'] == 'completed':
            transcript_text = polling_response.json()['text']
            st.write("Transcription Completed:")
            # st.write(transcript_text)
            transcript = aai.Transcriber().transcribe(audio_url, config)
            for utterance in transcript.utterances:
                print(f"Speaker {utterance.speaker}: {utterance.text}")
                st.write(f"Speaker {utterance.speaker}: {utterance.text}")
            break

    return polling_endpoint

def refresh_state():
    st.session_state['status'] = 'submitted'

if uploaded_wav_file is not None:
    st.audio(uploaded_wav_file, format='audio/wav')

if uploaded_mp3_file is not None:
    st.audio(uploaded_mp3_file, format='audio/mp3')

st.button('Check Status', on_click=refresh_state)
transcribe_button_wav = st.button('Transcribe WAV', on_click=transcribe_from_wav_or_mp3, args=(uploaded_wav_file, False))
transcribe_button_mp3 = st.button('Transcribe MP3', on_click=transcribe_from_wav_or_mp3, args=(uploaded_mp3_file, False))
