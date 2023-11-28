# speechToText
This directory includes Python code that allows users to transcribe their speech to text in real-time.

There are 4 folders in this repo. The descriptions of what is in each is as follows:
<br>
<ol>
  <li>
    SpeechToText with UI: The full-function transciber with an UI for users to interact with. All files in the folder convert speech to text in real-time using Assembly AI's API. The files are as below: 
    <ul>
      <li> speechToText_App.py: The final version of the UI. It transcribes speech to text in real-time, and when recording is stopped converts the text output to a downloadable txt file. <br></li>
      <li> speech_recognition.py: Has a basic Ui of starting recording by clicking abutton, outputting speech as text on the page, and stopping recording (and the program). <br> </li>
    </ul>
  </li>
  <li>AssembleAI: The real-time speech to text transcriber that has all the necessary functionality but no UI, so the transcription is done in the terminal. </li>
  <li> Jupyter Notebook: The real-time speech to text transcriber created in Jupyter Notebook, solely using pyaudio. No Assembly AI was used. </li>
  <li> Non-Assembly AI Python: The real-time speech to text transcriber created in Python, solely using pyaudio. No Assembly AI was used. The transcribed text is output onto the terminal.</li>
</ol>
