import cv2
import os
import sys
import time

def main(house_number):
    video = cv2.VideoCapture(0)

    if not video.isOpened():
        print("Error: Could not open video device.")
        return

    imageDetect = cv2.CascadeClassifier('C:\\Users\\himan\\Documents\\Community_Project\\smart_community\\community\\haarcascade_frontalface_default.xml')
    if imageDetect.empty():
        print("Error: Haar Cascade classifier not loaded. Check the file path.")
        return

    count = 0
    path = os.path.join('smart_community', 'community', 'static', 'images', house_number)

    if not os.path.exists(path):
        os.mkdir(path)
    else:
        print("Directory already exists. Please use a different house number.")
        return

    time.sleep(3)  # Wait for 3 seconds before capturing the image

    while True:
        ret, frame = video.read()
        if not ret:
            print("Failed to capture frame")
            break

        faces = imageDetect.detectMultiScale(frame, 1.3, 5)
        if len(faces) == 0:
            print("No faces found in the frame.")
            continue  # Skip the rest of the loop if no faces are found

        for x, y, w, h in faces:
            count += 1
            filename = os.path.join(path, f'{count}.jpg')
            print("Creating images: " + filename)
            cv2.imwrite(filename, frame[y:y+h, x:x+w])
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

        cv2.imshow("Window Frame", frame)
        if count == 1:
            break

    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        house_number = sys.argv[1]
        main(house_number)
    else:
        print("House number is required")
