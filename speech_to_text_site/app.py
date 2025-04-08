from flask import Flask, request, render_template
import whisper
import os

app = Flask(__name__)
model = whisper.load_model("medium")  # Можно заменить на "small", "medium", "large"

@app.route('/', methods=['GET', 'POST'])
def index():
    transcript = ""
    if request.method == 'POST':
        audio = request.files['audio']
        if audio:
            filepath = os.path.join("uploads", audio.filename)
            audio.save(filepath)
            result = model.transcribe(filepath)
            transcript = result['text']
            os.remove(filepath)
    return render_template('index.html', transcript=transcript)

if __name__ == '__main__':
    if not os.path.exists("uploads"):
        os.mkdir("uploads")
    app.run(debug=True)
