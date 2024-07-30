from flask import Flask, render_template

# Flask config
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/Audio_Interview')
def landing():
    return render_template('Audio_Interview.html')

@app.route('/interview/v')
def video_interview():
    return render_template('interview.html')

@app.route('/audio_index', methods=['POST'])
def audio_index():
    flash("After pressing the button above, you will have 15sec to answer the question.")
    return render_template('audio.html', display_button=False)



# This block is only used for local development
if __name__ == '__main__':
    app.run(debug=True)
