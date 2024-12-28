# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import face_recognition
import cv2
import requests
import os

# Define the function here
def extract_face_encodings(face_image_path):
    # Load the image
    image = face_recognition.load_image_file(file_name)

    # Get the face encodings
    encodings = face_recognition.face_encodings(image)
    if encodings:
        return encodings[0]  # Return the first encoding
    else:
        raise ValueError("No faces found in the image.")


def reverse_image_search(image_url, api_key):
    # this is the url link of serp api
    serp_api_url = "https://serpapi.com/search.json"

    # parameters for this request
    params = {
        "engine": "google_reverse_image",
        "image_url": image_url,  # url adress of the photo
        "api_key": api_key
    }
    # שליחת בקשת GET ל-SerpApi
    response = requests.get(serp_api_url, params=params)

    if response.status_code == 200:
        print("Full Response:", response.json())  # Debugging: Print the full response
        return response.json().get("images_results", [])
    else:
        raise ValueError(f"Error {response.status_code}: {response.text}")


# דוגמה לשימוש
api_key = "037aa4ce80f1e408c081476a8669b0b2aaac654acdedadc36657392675199700"

# כתובת URL ציבורית של תמונה (יש להעלות תמונה לשירות אחסון ולהשתמש בכתובת שלה)
image_url = "https://upload.wikimedia.org/wikipedia/commons/d/da/Britney_Spears_2013_%28Straighten_Crop%29.jpg"
if __name__ == '__main__':
    # Loading the haar cascade algorithm file
    alg = os.path.abspath('./haarcascade_frontalface_default.xml')

    # Passing the algorithm to OpenCV
    haar_cascade = cv2.CascadeClassifier(alg)

    # Loading the image path into file_name variable
    file_name = os.path.abspath("./friends-square.jpg")

    # Reading the image
    img = cv2.imread(file_name, 0)

    # Check if the image is loaded correctly
    if img is None:
        print("Image not loaded. Please check the file path and format.")
    else:
        # Converting the image to black and white (grayscale)
        gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Detecting the faces
        faces = haar_cascade.detectMultiScale(
            gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100)
        )

        i = 0
        # For each face detected
        for x, y, w, h in faces:
            # Crop the image to select only the face
            cropped_image = img[y: y + h, x: x + w]

            # Creating the target file name for storing the cropped face image
            target_file_name = r'stored-faces' + str(i) + '.jpg'

            # Saving the cropped face image
            cv2.imwrite(
                target_file_name,
                cropped_image,
            )

            i = i + 1

        print(f"Number of faces detected: {len(faces)}")
        cropped_faces = ["stored-faces1.jpg", "stored-faces3.jpg"]  # Example cropped face images
        for face in cropped_faces:
            try:
                encoding = extract_face_encodings(face)
                print(f"Face encoding for {face}: {encoding}")
            except ValueError as e:
                print(f"Error processing {face}: {e}")
    # Example usage
    api_key = "037aa4ce80f1e408c081476a8669b0b2aaac654acdedadc36657392675199700"
    #for face in cropped_faces:
    #results = reverse_image_search(file_name, api_key)
    #print(f"Results for {face}:", results)


    try:
        results = reverse_image_search(image_url, api_key)
        print("Results:", results)
    except ValueError as e:
        print("Error:", e)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
