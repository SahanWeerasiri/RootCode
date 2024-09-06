import os
import cv2
import pytesseract
import base64
from flask_cors import CORS
from flask import Flask, jsonify, request

# Set up relative path or environment variable for Tesseract executable
pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_CMD', '/usr/bin/tesseract')

app = Flask(__name__)
CORS(app)

@app.route('/detect-passport', methods=['POST'])
def detect_passport():
    # Expect the image as base64 string and decode it
    data = request.get_json()
    image_base64 = data.get('image')

    if not image_base64:
        return jsonify({"error": "No image data provided."}), 400

    # Decode the base64 image
    import io
    import numpy as np
    image_bytes = base64.b64decode(image_base64)
    image_np = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    if image is None:
        return jsonify({"error": "Could not decode the image data."}), 400

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # OCR to extract all text
    text = pytesseract.image_to_string(gray)

    # Extract the MRZ (bottom 2 lines)
    custom_config = '--psm 6'  # Treat the image as a single uniform block of text
    mrz = pytesseract.image_to_string(gray, config=custom_config)

    # Use regular expressions to find MRZ lines (MRZ lines are usually the last two lines of text)
    mrz_lines = mrz.strip().split('\n')[-2:]  # Get the last two lines
    mrz_text = ' '.join(mrz_lines)

    # Parse MRZ data
    def parse_mrz(mrz_lines):
        if len(mrz_lines) != 2:
            return None

        # Remove spaces for easier parsing
        line1 = mrz_lines[0].replace(' ', '')
        line2 = mrz_lines[1].replace(' ', '')

        # Extract data from MRZ
        passport_data = {
            "document_type": line1[0],
            "country_code": line1[2:5],
            "surname": line1[5:].split('<<')[0].replace('<', ' ').strip(),
            "given_names": ' '.join(line1[5:].split('<<')[1].split('<')).strip(),
            "passport_number": line2[0:9].replace('<', ''),
            "nationality": line2[10:13],
            "date_of_birth": line2[13:19],
            "sex": line2[20],
            "expiration_date": line2[21:27],
            "personal_number": line2[28:42].replace('<', '')
        }
        return passport_data

    passport_info = parse_mrz(mrz_lines)

    if passport_info is None:
        return jsonify({"error": "Failed to parse MRZ data."}), 400

    # Face Detection and Extraction with Padding
    def extract_face_with_padding(image, padding=40):
        # Load the pre-trained Haar Cascade for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            return None

        # Assuming the passport has one face, extract the first detected face
        for (x, y, w, h) in faces:
            # Add padding while ensuring it doesn't go out of image boundaries
            x1 = max(x - padding, 0)
            y1 = max(y - padding, 0)
            x2 = min(x + w + padding, image.shape[1])
            y2 = min(y + h + padding, image.shape[0])

            face = image[y1:y2, x1:x2]
            _, buffer = cv2.imencode('.jpg', face)
            face_base64 = base64.b64encode(buffer).decode('utf-8')
            return face_base64

    # Extract face from the passport with padding
    face_base64 = extract_face_with_padding(image, padding=40)

    response_data = {"passport_info": passport_info}
    if face_base64:
        response_data["face_image"] = face_base64

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
