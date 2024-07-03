import cv2
import numpy as np

# Load pre-trained model for object detection
net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
classes = []
with open('coco.names', 'r') as f:
    classes = f.read().splitlines()

# Define the classes of interest
classes_of_interest = ['car', 'person', 'truck', 'motorbike']

# Set up camera with stream URL
stream_url = 'http://192.168.145.216:8080/video'
cap = cv2.VideoCapture(stream_url)

# Create a separate window for real-time results
cv2.namedWindow('Real-Time Results', cv2.WINDOW_NORMAL)

while True:
    success, img = cap.read()
    if not success:
        print("Failed to retrieve frame from stream.")
        break

    height, width, _ = img.shape

    # Prepare input image for object detection
    blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layer_outputs = net.forward(output_layers_names)

    # Extract bounding boxes, confidences, and class IDs
    boxes = []
    confidences = []
    class_ids = []

    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and classes[class_id] in classes_of_interest:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w/2)
                y = int(center_y - h/2)
                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    # Apply non-max suppression
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Draw bounding boxes on detected objects
    result_img = img.copy()  # Create a copy of the original image for displaying results
    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i],2))
            color = (0, 255, 0)
            cv2.rectangle(result_img, (x, y), (x+w, y+h), color, 2)
            cv2.putText(result_img, label + " " + confidence, (x, y+20), cv2.FONT_HERSHEY_PLAIN, 1, color, 2)

    # Display real-time results
    cv2.imshow('Real-Time Results', result_img)

    # Display output
    cv2.imshow('Original Stream', img)
    key = cv2.waitKey(1)
    if key == 27:  # press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
