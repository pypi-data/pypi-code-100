import cv2
from Camera import Camera


def watch_stream(source):
    cap = Camera(source)
    while True:
        frame = cap.getFrame()
        if frame is not None:
            cv2.imshow('frame', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            continue
    cv2.destroyAllWindows()


def watch_stream_grey(source):
    cap = Camera(source)
    while True:
        frame = cap.getFrame()
        if frame is not None:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame', gray_frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            continue
    cv2.destroyAllWindows()


def run(source):
    watch_stream(source)


if __name__ == "__main__":
    run(
        source='',
    )
