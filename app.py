from flask import Flask, render_template

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

# Video interview template
@app.route('/video', methods=['POST'])
def video() :
    # Display a warning message
    flash('You will have 45 seconds to discuss the topic mentioned above. Due to restrictions, we are not able to redirect you once the video is over. Please move your URL to /video_dash instead of /video_1 once over. You will be able to see your results then.')
    return render_template('video.html')

# This block is only used for local development
if __name__ == '__main__':
    app.run(debug=True)
