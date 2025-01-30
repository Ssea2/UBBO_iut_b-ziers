from keras.models import load_model # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import cv2
import time

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

model = new_model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()


def predic_move(image):
    # Load the model
    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    #image = Image.open(image).convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = cv2.resize(image, size, interpolation= cv2.INTER_LINEAR)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", confidence_score)

url = "http://127.0.0.1:4747/video"

cap = cv2.VideoCapture(url)

c=0
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    if c==12:
        predic_move(frame)
        c=0
    # Convert from YUVJ420P if needed
    #frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_I420)

    cv2.imshow("DroidCam USB Stream", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

    c+=1
    
