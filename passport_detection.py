import os
import cv2
import pytesseract
import base64
import json
import numpy as np
import requests


# Set Tesseract command
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Get image URL from environment variable
image_url = os.environ.get('IMAGE_URL')


# Parse MRZ data
def parse_mrz(mrz_lines):
    if len(mrz_lines) != 2:
        return None
    line1 = mrz_lines[0].replace(' ', '')
    line2 = mrz_lines[1].replace(' ', '')
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



# Face Detection and Extraction
def extract_face_with_padding(image, padding=40):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) == 0:
        return None
    for (x, y, w, h) in faces:
        x1 = max(x - padding, 0)
        y1 = max(y - padding, 0)
        x2 = min(x + w + padding, image.shape[1])
        y2 = min(y + h + padding, image.shape[0])
        face = image[y1:y2, x1:x2]
        _, buffer = cv2.imencode('.jpg', face)
        face_base64 = base64.b64encode(buffer).decode('utf-8')
        return face_base64



if image_url:
    # Download the image
    response = requests.get(image_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Save the image locally
        local_image_path = "downloaded_image.jpg"
        with open(local_image_path, "wb") as f:
            f.write(response.content)
        
        # Load the image from the local path
        image = cv2.imread(local_image_path)
        
        # Check if the image was loaded properly
        if image is not None:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Continue with your processing...
            # OCR to extract all text
            text = pytesseract.image_to_string(gray)
            
            # Extract the MRZ (bottom 2 lines)
            custom_config = '--psm 6'
            mrz = pytesseract.image_to_string(gray, config=custom_config)
            mrz_lines = mrz.strip().split('\n')[-2:]
            mrz_text = ' '.join(mrz_lines)

            passport_info = parse_mrz(mrz_lines)
        
            face_base64 = extract_face_with_padding(image, padding=40)
            
            response_data = {"passport_info": passport_info}
            if face_base64:
                response_data["face_image"] = face_base64
            
            # Save the result to a file
            with open('passport_detection_result.json', 'w') as f:
                json.dump(response_data, f)
            
            print(json.dumps(response_data, indent=2))

            
        else:
            print("Error: Image could not be loaded from the local file.")
    else:
        print(f"Error: Failed to download the image. Status code: {response.status_code}")
else:
    print("Error: IMAGE_URL environment variable not set.")
