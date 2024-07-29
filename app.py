from __future__ import division
import numpy as np
import pandas as pd
import time
import os
from collections import Counter
import altair as alt

# Flask imports
import requests
from flask import Flask, render_template, session, request, redirect, flash, Response

# Audio imports
from library.speech_emotion_recognition import speechEmotionRecognition

# Flask config
app = Flask(__name__)
app.secret_key = b'(\xee\x00\xd4\xce"\xcf\xe8@\r\xde\xfc\xbdJ\x08W'
app.config['UPLOAD_FOLDER'] = '/Upload'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/Audio_Interview')
def landing():
    return render_template('Audio_Interview.html')

@app.route('/interview/v')
def video_interview():
    return render_template('interview.html')

# Read the overall dataframe before the user starts to add his own data
df = pd.read_csv('static/js/db/histo.txt', sep=",")

################################################################################
############################### AUDIO INTERVIEW ################################
################################################################################

@app.route('/audio_index', methods=['POST'])
def audio_index():
    flash("After pressing the button above, you will have 15sec to answer the question.")
    return render_template('audio.html', display_button=False)

@app.route('/audio_recording', methods=["POST", "GET"])
def audio_recording():
    # Instantiate new SpeechEmotionRecognition object
    SER = speechEmotionRecognition()

    # Voice Recording
    rec_duration = 16  # in sec
    tmp_dir = 'tmp'
    rec_sub_dir = os.path.join(tmp_dir, 'voice_recording.wav')

    # Ensure the directory exists
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    SER.voice_recording(rec_sub_dir, duration=rec_duration)

    # Send Flash message
    flash("The recording is over! You now have the opportunity to do an analysis of your emotions. If you wish, you can also choose to record yourself again.")
    return render_template('audio.html', display_button=True)

@app.route('/audio_dash', methods=["POST", "GET"])
def audio_dash():
    # Sub dir to speech emotion recognition model
    model_sub_dir = os.path.join('Models', 'audio.hdf5')

    # Instantiate new SpeechEmotionRecognition object
    SER = speechEmotionRecognition(model_sub_dir)

    # Voice Record sub dir
    rec_sub_dir = os.path.join('tmp', 'voice_recording.wav')

    # Predict emotion in voice at each time step
    step = 1  # in sec
    sample_rate = 16000  # in Hz
    emotions, timestamp = SER.predict_emotion_from_file(rec_sub_dir, chunk_step=step * sample_rate)

    # Export predicted emotions to .txt format
    SER.prediction_to_csv(emotions, os.path.join("static/js/db", "audio_emotions.txt"), mode='w')
    SER.prediction_to_csv(emotions, os.path.join("static/js/db", "audio_emotions_other.txt"), mode='a')

    # Get most common emotion during the interview
    major_emotion = max(set(emotions), key=emotions.count)

    # Calculate emotion distribution
    emotion_dist = [int(100 * emotions.count(emotion) / len(emotions)) for emotion in SER._emotion.values()]

    # Export emotion distribution to .csv format for D3JS
    df = pd.DataFrame(emotion_dist, index=SER._emotion.values(), columns=['VALUE']).rename_axis('EMOTION')
    df.to_csv(os.path.join('static/js/db', 'audio_emotions_dist.txt'), sep=',')

    # Get most common emotion of other candidates
    df_other = pd.read_csv(os.path.join("static/js/db", "audio_emotions_other.txt"), sep=",")

    # Get most common emotion during the interview for other candidates
    major_emotion_other = df_other['EMOTION'].mode()[0]

    # Calculate emotion distribution for other candidates
    emotion_dist_other = [int(100 * len(df_other[df_other['EMOTION'] == emotion]) / len(df_other)) for emotion in SER._emotion.values()]

    # Export emotion distribution to .csv format for D3JS
    df_other = pd.DataFrame(emotion_dist_other, index=SER._emotion.values(), columns=['VALUE']).rename_axis('EMOTION')
    df_other.to_csv(os.path.join('static/js/db', 'audio_emotions_dist_other.txt'), sep=',')

    # Sleep
    time.sleep(0.5)

    return render_template('audio_dash.html', emo=major_emotion, emo_other=major_emotion_other, prob=emotion_dist, prob_other=emotion_dist_other)

# This block is only used for local development
if __name__ == '__main__':
    app.run(debug=True)
