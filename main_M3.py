from ultralytics import YOLO
import cv2
import socket
from time import sleep

# Load yolov8 model
model = YOLO('yolov8n.pt')
move = False
# Start capturing video from the default camera
cap = cv2.VideoCapture(2)


def create_socket():
    try:
        global host
        global port
        global s
        host = "0.0.0.0"
        port = 9988
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        # Attempt to bind the socket
        s.bind(("", port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error: " + str(msg) + "\n" + "Retrying...")
        bind_socket()


def socket_accept():
    global conn
    conn, address = s.accept()
    print("Connection has been established! |" + " IP " + address[0] + " | Port" + str(address[1]))
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()
        # Check if the frame was read successfully
        if ret:
            # Detect and track objects in the frame
            results = model.track(frame, persist=True)
            # Iterate over the results
            for result in results:
                # print(result.names)
                # Extract bounding box coordinates of detected persons
                boxes = result.boxes.xyxy

                # print(result.boxes.cls)
                # print(f"shape {result.boxes.shape}")
                detection_count = result.boxes.shape[0]

                for i in range(detection_count):
                    cls = int(result.boxes.cls[i].item())
                    name = result.names[cls]
                    confidence = float(result.boxes.conf[i].item())
                    bounding_box = result.boxes.xyxy[i].cpu().numpy()
                    # print(f"cls {cls}  name {name}   confidence {confidence}   box  {bounding_box}")

                # "tensor([ 0., 67.])" == str(result.boxes.cls)
                # Iterate over the bounding boxes
                # print(len("tensor([4.])"))
                # if len(str(result.boxes.id)) < 14:
                if "tensor([ 0., 67.])" == str(result.boxes.cls):
                    # print(str(result.boxes.id))
                    # boxes = result.boxes.xyxy
                    pattern = []
                    counter = 0
                    for box in boxes:
                        # if "tensor([0.])" == bo:

                        x1, y1, x2, y2 = map(int, box)  # Convert to integer
                        x = (x1 + x2) // 2  # Calculate x-coordinate of the center
                        y = (y1 + y2) // 2  # Calculate y-coordinate of the center
                        subtract = x1 - x2
                        pattern.append(x)
                        pattern.append(y)
                        pattern.append(y1)
                        pattern.append(subtract)
                        counter += 1
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                        # print(f"Person detected at ({x}, {y})")  # Print the coordinates
                        # print(f"x1 = {x1}, y1 = {y1}")
                    if pattern[3] > pattern[7]:
                        x = pattern[4]
                        y = pattern[5]
                        y1 = pattern[6]
                    else:
                        x = pattern[0]
                        y = pattern[1]
                        y1 = pattern[2]

                    if x >= 400:
                        direction = "right"
                        if y1 > 50:
                            move = True
                        else:
                            move = False
                    elif x <= 200:
                        direction = "left"
                        if y1 > 50:
                            move = True
                        else:
                            move = False
                    else:
                        direction = "center"
                        if y1 > 50:
                            move = True
                        else:
                            move = False

                    # print(f"y1 = {y1} and y2 = {y2}")
                    # Draw bounding box on the frame
                    print(f"direction {direction}      +        move {move}")
                    list_dir_move = [direction, move]
                    list_dir_move = str(list_dir_move)
                    conn.send(list_dir_move.encode())

            # Display the resulting frame
            cv2.imshow('Real-time Object Detection', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


create_socket()
bind_socket()
socket_accept()
cap.release()
cv2.destroyAllWindows()
