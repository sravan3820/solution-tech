from flask import Flask, render_template, request, send_file
from gtts import gTTS
import os
import uuid

# Initialize Flask app
app = Flask(__name__)

# Folder to save audio output
OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Home route
@app.route('/')
def index():
    return render_template('index.html')  # Ensure this file exists in the templates folder

# Route for text-to-speech conversion
@app.route('/convert', methods=['POST'])
def convert_text_to_audio():
    text = request.form.get('text', '')
    if not text.strip():
        return "Error: No text provided.", 400

    try:
        # Convert to speech using gTTS
        tts = gTTS(text)
        
        # Create unique filename
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join(OUTPUT_FOLDER, filename)

        # Save the audio file
        tts.save(filepath)

        # Send the file back to the user
        return send_file(
            filepath,
            as_attachment=True,
            download_name="echoverse_audiobook.mp3",
            mimetype="audio/mpeg"
        )

    except Exception as e:
        return f"Something went wrong: {str(e)}", 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
