from flask import Flask, request, jsonify, render_template, send_from_directory
import whisper
import os

app = Flask(__name__)
model = whisper.load_model("small")  # можно поменять на tiny / small / medium / large

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "file" not in request.files:
        return jsonify({"error": "Нет файла"}), 400

    file = request.files["file"]
    if not file.filename.endswith(".wav"):
        return jsonify({"error": "Формат должен быть .wav"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        result = model.transcribe(filepath)
        return jsonify({"text": result["text"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(filepath)

if __name__ == "__main__":
    app.run(debug=True)
