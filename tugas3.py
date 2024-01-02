from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import pygame

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_Model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

pygame.init()

width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bahasa Isyarat")

fps = 30
clock = pygame.time.Clock()
# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)
camera.set(3, 1280)
camera.set(4, 720)


start = True
while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()
    # Grab the webcamera's image.
    ret, image = camera.read()
    img = cv2.flip(image, 1)

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB = np.rot90(imgRGB)
    frame = pygame.surfarray.make_surface(imgRGB).convert()
    frame = pygame.transform.flip(frame, True, False)
    window.blit(frame, (0, 0))
    
    font = pygame.font.Font('freesansbold.ttf', 50)
    textTitle = font.render(f'Class: {class_name[2:]}', True, (50, 50, 255))
    window.blit(textTitle, (490, 35))
    
    pygame.display.update()
    clock.tick(30)

camera.release()
cv2.destroyAllWindows()

