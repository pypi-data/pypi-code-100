import cv2
from tracker import *
from datetime import datetime
import numpy as np


def read_video():
    cap = cv2.VideoCapture('/Users/worksitevision/Documents/worker/stream/test.mp4')
    object_detector = cv2.createBackgroundSubtractorMOG2(history=225, varThreshold=100)
    durum = 0
    centers = []
    while cap.isOpened():
        ret, frame = cap.read()
        if np.shape(frame) == ():
            # If there is no frame, it draws points to the coordinates it takes in the centers list.
            create_image(centers)
            break
        else:
            height, width, _ = frame.shape
            set_region(frame)
            detections = car_detection(frame, object_detector)
            merkez, durum, id_list = car_tracking(detections, frame, durum)
            centers.append(merkez)
            entrance_exit_gate(frame)
            capture_photo(frame, durum)
            result(frame, durum)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                # If the video is closed with 'q' before it ends, it draws a point to the coordinates it has listed
                # so far.
                create_image(centers)
                break
    cap.release()
    cv2.destroyAllWindows()


def set_region(frame):
    # Set fixed region
    x = 650
    y = 750
    w = 150
    h = 200
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 3)
    coordinate = [x, y, x + w, y + h]
    return coordinate


def find_center_of_the_region(coordinate):
    # Find the center of the fixed region
    x1, y1, x2, y2 = coordinate
    cX = int(x1 + ((x2 - x1) / 2))
    cY = int(y1 + ((y2 - y1) / 2))
    region_center = cX, cY
    return region_center


def car_detection(frame, object_detector):
    # Detect vehicles
    mask = object_detector.apply(frame)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 250:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            detections.append([x, y, w, h])
    return detections


def create_image(centers):
    image = cv2.imread("image.png")
    print(len(centers))
    for i in range(len(centers)):
        print(centers[i])
        cv2.circle(image, centers[i], 2, (0, 255, 0), 15)
    cv2.imwrite("newimage.png", image)
    return image


def entrance_exit_gate(frame):
    # Draw Entry-Exit Doors
    x1, y1, w1, h1 = (880, 838, 0, 50)
    x2, y2, w2, h2 = (1890, 800, 0, 80)
    x3, y3, w3, h3 = (1590, 660, 0, 80)

    cv2.line(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 255), thickness=5)  # T1 Gate
    cv2.line(frame, (x2, y2), (x2 + w2, y2 + h2), (0, 0, 255), thickness=5)  # T2 Gate
    cv2.line(frame, (x3, y3), (x3 + w3, y3 + h3), (0, 0, 255), thickness=5)  # T3 Gate

    g1_xy = x1, y1, x1 + w1, y1 + h1
    g2_xy = x2, y2, x2 + w2, y2 + h2
    g3_xy = x3, y3, x3 + w3, y3 + h3

    return g1_xy, g2_xy, g3_xy


def car_tracking(detections, frame, durum):
    # Track vehicle
    id_list = []
    tracker = EuclideanDistTracker()
    boxes_ids, deneme = tracker.update(detections)
    x_y = None
    for box_id in boxes_ids:
        x, y, w, h, car_id = box_id
        if car_id not in id_list:
            id_list.append(car_id)
        cv2.putText(frame, str(car_id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 177, 0), 3)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        x_y = deneme[car_id]

        statusDegisken = x, y, x_y, car_id, frame
        durum = status(statusDegisken, durum)
    return x_y, id_list, durum


def status(statusDegisken, durum):
    # Entry-exit status of vehicles
    # T1 Gate
    cX = int(850 + ((850 - 850) / 2))  # (x1+((x1-x1)/2))
    cY = int(838 + ((888 - 838) / 2))  # (y1 + ((y1+h1)-y1)/2)

    # T2 Gate
    cX1 = int(1890 + ((1890 - 1890) / 2))
    cY1 = int(800 + ((800 - 80) / 2))

    # T3 Gate
    cX2 = int(1590 + ((1590 - 1590) / 2))
    cY2 = int(660 + ((660 - 80) / 2))

    x, y, x_y, car_id, frame = statusDegisken
    now = datetime.now()
    minute = now.minute
    if minute <= 9:
        minute = "0" + str(minute)

    # T1 Kapısı
    if (x_y[0]) > cX and (x_y[0]) < cX + 20 and x_y[1] > cY and x_y[1] < cY + 20:
        cv2.putText(frame, "X", (x + 37, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 4)
        durum = 1
        print("Status: T1 Kapısından Girdi " + str(durum) + " - " + "Car Id: " + str(car_id) + " - " + "Giris Saati: " + str(
            now.hour) + ":")


    elif (x_y[0]) < cX and (x_y[0]) > cX - 20 and x_y[1] < cY and x_y[1] > cY - 20:
        cv2.putText(frame, "A", (x + 37, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 4)
        durum = -1
        print("Status: T1 Kapısından Çıktı " + str(durum) + " - " + "Car Id: " + str(car_id) + " - " + "Cikis Saati: " + str(
            now.hour) + ":" + str(minute))

    # T2 Kapısı
    elif (x_y[0]) > cX1 and (x_y[0]) < cX1 + 20 and x_y[1] > cY1 and x_y[1] < cY1 + 20:
        cv2.putText(frame, "X", (x + 37, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 4)
        durum = 1
        print("Status: T2 Kapısından Girdi " + str(durum) + " - " + "Car Id: " + str(car_id) + " - " + "Giris Saati: " + str(
            now.hour) + ":" + str(minute))
        #counter += 1
        #print("T2 Bölgesine Giren Araç Sayısı: " + str(counter))

    elif (x_y[0]) < cX1 and (x_y[0]) > cX1 - 20 and x_y[1] < cY1 and x_y[1] > cY1 - 20:
        cv2.putText(frame, "A", (x + 37, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 4)
        durum = -1
        print("Status: T2 Kapısından Çıktı " + str(durum) + " - " + "Car Id: " + str(car_id) + " - " + "Cikis Saati: " + str(
            now.hour) + ":" + str(minute))

    # T3 Kapısı
    elif (x_y[0]) > cX2 and (x_y[0]) < cX2 + 20 and x_y[1] > cY2 and x_y[1] < cY2 + 20:
        cv2.putText(frame, "X", (x + 37, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 4)
        durum = 1
        print("Status: T3 Kapısından Girdi " + str(durum) + " - " + "Car Id: " + str(car_id) + " - " + "Giris Saati: " + str(
            now.hour) + ":" + str(minute))


    elif (x_y[0]) < cX2 and (x_y[0]) > cX2 - 20 and x_y[1] < cY2 and x_y[1] > cY2 - 20:
        cv2.putText(frame, "A", (x + 37, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 4)
        durum = -1
        print("Status: T3 Kapısından Çıktı " + str(durum) + " - " + "Car Id: " + str(car_id) + " - " + "Cikis Saati: " + str(
            now.hour) + ":" + str(minute))

    return durum


def capture_photo(frame, durum):
    now = datetime.now()
    if durum == 1:
        cv2.imwrite('img' + str(now.hour) + '.jpg', frame)
        print(frame)
        return frame


def result(frame, durum):
    raporList = (durum,frame)
    with open("rapor.txt", "a") as file:
        file.write(str(raporList))

    return file


def run():
    pass


if __name__ == "__main__":
    read_video()

