from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

# This block is only used for local development
if __name__ == '__main__':
    app.run(debug=True)