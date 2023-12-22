# speechToText
This repository includes Python code that allows users to transcribe their speech to text in real-time. 

This repo contains code from my company, <a href="https://www.vitalwise-technology.com/">VitalWise's</a>, private AutoDocumentation repository, where the client-ready software is built. 

There are 4 folders in this repo. The descriptions of what is in each is as follows:
<br>
<ol>
  <li>
    <strong> SpeechToText with UI:</strong> The full-function transciber with an UI for users to interact with. All files in the folder convert speech to text in real-time using Assembly AI's API. The files are as below: 
    <ul>
      <li> <strong> speechToText_App.py: </strong> The final version of the UI. It transcribes speech to text in real-time, and when recording is stopped converts the text output to a downloadable txt file. <br></li>
      <li> <strong> speech_recognition.py:</strong> Has a basic UI of starting recording by clicking abutton, outputting speech as text on the page, and stopping recording (and the program). <br> </li>
      <li> <strong> audio_file_transcript.py:</strong> The UI enables a user to input an audio file, and outputs the speech as text on the page with Speaker labels on each separate speaker. <br> </li>
      <li><strong>20230607_me_canadian_wildfires.mp3: </strong> The audio file we use to test our program. </li>
    </ul>
  </li><br>
  <li> <strong> AWS:</strong> The real-time speech to text transcriber using AWS Transcribe, that has all the necessary functionality but no UI, so the transcription is done in the terminal. </li><br>
  <li> <strong> AssemblyAI:</strong> The real-time speech to text transcriber that has all the necessary functionality but no UI, so the transcription is done in the terminal. </li><br>
  <li> <strong> Jupyter Notebook: </strong> The real-time speech to text transcriber created in Jupyter Notebook, solely using pyaudio. No Assembly AI was used. </li><br>
  <li> <strong> Non-API Speech-To-Text </strong> The real-time speech to text transcriber created in Python, solely using pyaudio. No Assembly AI was used. The transcribed text is output onto the terminal.</li><br>
</ol>
