import cv2
import numpy as np


def main():
    cap = cv2.VideoCapture('/Users/worksitevision/Documents/worker/stream/croptest.mp4')
    frameNo = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if np.shape(frame) == ():
            break
        else:
            cv2.imshow("frame", frame)
            camera_movement(frame,frameNo)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


def average(liste):
    return int(sum(liste) / len(liste))


def camera_movement(frame, frameNo):
    b = list()
    g = list()
    r = list()
    for y in range(1175, 1225):
        for x in range(175, 225):
            b.append(frame[x, y, 0])  # B Channel Value
            g.append(frame[x, y, 1])  # G Channel Value
            r.append(frame[x, y, 2])  # R Channel Value

    averageB = average(b)  # average of list b
    averageG = average(g)  # average of list g
    averageR = average(r)  # average of list r
    print('Frame: {0}, B:{1}, G:{2}, R:{3}.'.format(frameNo, averageB, averageG, averageR))
    frameNo += 1

    # bgr value of fixed point at sea (209,124,38)
    if 195 < averageB < 215 and 115 < averageG < 135 and 25 < averageR < 50:
        print("Kamera sabit.")
    else:
        print("Kamera hareket etti")


if __name__ == "__main__":
    main()
