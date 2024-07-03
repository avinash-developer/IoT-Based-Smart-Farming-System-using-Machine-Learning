import RPi.GPIO as GPIO
import time
import requests
import cv2
import numpy as np

# Set up GPIO pins
pir1_pin = 17
pir2_pin = 18
led_check_in_pin = 23
led_check_out_pin = 24
flame_sensor_pin = 25
buzzer_pin = 22

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir1_pin, GPIO.IN)
GPIO.setup(pir2_pin, GPIO.IN)
GPIO.setup(led_check_in_pin, GPIO.OUT)
GPIO.setup(led_check_out_pin, GPIO.OUT)
GPIO.setup(flame_sensor_pin, GPIO.IN)
GPIO.setup(buzzer_pin, GPIO.OUT)

# Initialize variables
car_detected = False
last_car_detection_time = time.time()

# Functions for controlling LEDs and buzzer
def turn_on_led(pin):
    GPIO.output(pin, GPIO.HIGH)

def turn_off_led(pin):
    GPIO.output(pin, GPIO.LOW)

def activate_buzzer():
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(buzzer_pin, GPIO.LOW)

# Function to send data to ThingSpeak
def send_to_thingspeak(data):
    api_key = 'YOUR_THINGSPEAK_API_KEY'
    url = f'https://api.thingspeak.com/update?api_key={api_key}&field1={data}'
    response = requests.get(url)
    if response.status_code == 200:
        print("Data sent to ThingSpeak successfully.")
    else:
        print("Failed to send data to ThingSpeak.")

# Function to monitor flame sensor
def monitor_flame_sensor():
    if GPIO.input(flame_sensor_pin):
        print("Fire detected!")
        activate_buzzer()
        send_to_thingspeak(1)
    else:
        print("No fire detected.")

# Function to monitor PIR sensors
def monitor_pir_sensors():
    global car_detected, last_car_detection_time
    if GPIO.input(pir1_pin):
        turn_on_led(led_check_in_pin)
        if not car_detected:
            car_detected = True
            last_car_detection_time = time.time()
    else:
        turn_off_led(led_check_in_pin)

    if GPIO.input(pir2_pin):
        turn_on_led(led_check_out_pin)
        if car_detected:
            car_detected = False
            last_car_detection_time = time.time()
    else:
        turn_off_led(led_check_out_pin)

# Function to monitor car presence
def monitor_car_presence():
    global car_detected, last_car_detection_time
    if not car_detected and time.time() - last_car_detection_time > 20:
        # Dim the intensity of the LEDs
        print("No vehicle detected for more than 20 seconds. Dimming lights...")
        # Add code to dim the intensity of the LEDs here
        last_car_detection_time = time.time()

# Function to monitor accidents using IP webcam
def monitor_accidents():
    stream_url = 'http://192.168.145.216:8080/video'
    cap = cv2.VideoCapture(stream_url)

    detected_objects = {}

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
                if confidence > 0.5:
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

        # Draw bounding boxes on detected objects and update counts
        if len(indexes) > 0:
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])

                if label in ['person', 'car', 'truck', 'motorbike']:
                    print(f"{label} detected!")
                    # Add code to handle accident detection alert
                else:
                    print(f"{label} detected but not relevant to accident detection.")

                # Draw rectangle and text
                color = (0, 255, 0)
                cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
                cv2.putText(img, label, (x, y+20), cv2.FONT_HERSHEY_PLAIN, 1, color, 2)

        # Display output
        cv2.imshow('Image', img)
        key = cv2.waitKey(1)
        if key == 27:  # press 'Esc' to exit
            break

    cap.release()
    cv2.destroyAllWindows()

try:
    while True:
        monitor_pir_sensors()
        monitor_flame_sensor()
        monitor_car_presence()
        monitor_accidents()
        time.sleep(1)  # Check sensors every 1 second

except KeyboardInterrupt:
    GPIO.cleanup()
