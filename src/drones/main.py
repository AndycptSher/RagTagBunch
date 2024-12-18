import pygame
from djitellopy import tello
import cv2
import time
import numpy
pygame.init()
global display, prev_error

w, h = 360, 240
prev_error = 0

# testing zone


# hand tracking section

# mediapipe depreciated

# tello
drone = tello.Tello()
try:
    try:
        drone.connect()
    except "Command '{}' was unsuccessful for {} tries. Latest response:\t'{}'":
        pass


    if drone.get_battery() < 10:
        print("battery too low")
        quit()
    # sensor

    # win = pygame.display.set_mode((0, 0))


    def get_key(key_name: str) -> bool:
        for _ in pygame.event.get():
            pass
        keyinput = pygame.key.get_pressed()
        mykey = getattr(pygame,"K_{}".format(key_name))

        if keyinput[mykey]:
            # pygame.display.update()
            return True


    def keyboard_input() -> list:
        forwardv, strafev, elevationv, rotationv = 0, 0, 0, 0
        # key/input detection section
        if get_key("a"):
            strafev = -50

        if get_key("d"):
            strafev = 50

        if get_key("w"):
            forwardv = 50

        if get_key("s"):
            forwardv = -50

        if get_key("LEFT"):
            rotationv = -50

        if get_key("RIGHT"):
            rotationv = 50

        if get_key("SPACE"):
            elevationv = 50

        if get_key("RSHIFT") or get_key("LSHIFT"):
            elevationv = -50

        if get_key("ESCAPE"):
            drone.land()
            drone.streamoff()

        if get_key("q"):
            drone.land()

        if get_key("e"):
            drone.takeoff()

        if get_key("z"):
            cv2.imwrite(f"/Users/andychung/PycharmProjects/pygame stuff/drone_pictures/{time.time()}.jpg", display)

        return [rotationv*2, elevationv, forwardv, strafev]

    def find_face(image):
        face_cascade = cv2.CascadeClassifier("drone_pictures/face_reconition_machine_learning_algorithim.xml")
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow("gray", grayscale)
        cv2.waitKey(1)
        faces = face_cascade.detectMultiScale(grayscale, 1.2, 8)

        facedictionary = {}

        for (x, y, d, f) in faces:
            x_center = x + d // 2
            y_center = y + f // 2
            face_area = d * f
            facedictionary[(x_center, y_center)] = face_area
            cv2.rectangle(image, (x,  y), (x + d, y + f), (0, 0, 255), 2)
        if facedictionary:

            return image, [max(facedictionary, key=facedictionary.get), max(facedictionary.values())]
        else:
            return image, [(0, 0), 0]


    pid = [0.4, 0.4, 0]

    def position_adjustment(drone, info, w, pid, prev_Error):
        x, y = info[0]
        area = info[1]
        person_range = [10000, 15000]

        distance_from_center = x - w // 2

        speed = pid[0] * distance_from_center + pid[1] * (distance_from_center - prev_Error)
        speed = int(numpy.clip(speed, -100, 100))

        forwardv, elevationv = 0, 0
        if person_range[0] < area < person_range[1]:
            forwardv = 0
        elif area > person_range[1]:
            forwardv = -20
        elif area < person_range[0] and area:
            forwardv = 20

        if 80 < y < 160:
            elevationv = 0
        elif y > 160:
            elevationv = 10
        elif y < 80 and y:
            elevationv = -10


        if not x:
            speed = 0
            distance_from_center = 0

        print(info)
        drone.send_rc_control(0, forwardv, elevationv, speed)

        return distance_from_center


    def thresholding(image):
        hsvVals = [0, 0, 117, 179, 22, 219]
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower = numpy.array([hsvVals[0], hsvVals[1], hsvVals[2]])
        upper = numpy.array([hsvVals[3], hsvVals[4], hsvVals[5]])
        return cv2.inRange(hsv, lower, upper)

    def getContours(image_thr, image):
        cx = 0
        contours, heiracrhy = cv2.findContours(image_thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if not len(contours):
            biggest = max(contours, key = cv2.contourArea)
            x, y, d, f = cv2.boundingRect(biggest)
            cx = x + d // 2
            cy = y + f // 2
            cv2.drawContours(image, contours, -1, (255, 0, 255), 7)
            # cv2.circle(image, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        return cx

    def getSensorOutput(image_thr, image):
        sensors = 3
        totalPixels = (image.shape[1]//sensors)*image.shape[0]
        imgs = numpy.hsplit(image_thr, sensors)
        senOut = []
        for x, im in enumerate(imgs):
            pixelCount = cv2.countNonZero(im)
            if pixelCount > totalPixels* 0.2:
                senOut.append(1)
            else:
                senOut.append(0)
            # cv2.imshow(str(x), im)
        return senOut

    def send_to_drone(drone, senOut, cx):
        sensitivity = 3  # high val == les sensitive
        ## TRANSLATION
        width, height = 360, 240
        lr = (cx - width // 2)//sensitivity
        lr = int(numpy.clip(lr, -10, 10))

        if -2 < lr < 2:
            lr = 0

        weights = [-25, -15, 0, 15, 25]
        ## ROTATION
        curve = 0
        if senOut == [1, 0, 0]:
            curve = weights[0]
        elif senOut == [1, 1, 0]:
            curve = weights[1]
        elif senOut == [0, 1, 0]:
            curve = weights[2]
        elif senOut == [0, 1, 1]:
            curve = weights[3]
        elif senOut == [0, 0, 1]:
            curve = weights[4]

        elif senOut == [0, 0, 0]:
            curve = weights[2]
        elif senOut == [1, 1, 1]:
            curve = weights[2]
        elif senOut == [1, 0, 1]:
            curve = weights[2]


        drone.send_re_control(lr, 10, 0, curve)



    # star-ting the stream
    drone.streamon()
    track, path = False, False

    while True:
        if get_key("ESCAPE"):
            break


        # image replay/display section

        display = drone.get_frame_read().frame
        # resize image
        display = cv2.resize(display, (360, 240))
        # tab title, image
        cv2.imshow("Image", display)
        # show for 1 millisecond
        cv2.waitKey(1)

        # track tracking
        if not path:
            path = get_key("p")
        if path and not track:
            if get_key("r"):
                path = False
            else:
                # follow track
                img_thr = thresholding(display)
                cx = getContours((img_thr, display))
                senOut = getSensorOutput(img_thr, display)
                send_to_drone(drone, senOut, cx)




        # face tracking section

        if not track:
            track = get_key("t")

        if track and not path:
            if get_key("r"):
                track = False
                cv2.destroyAllWindows()
            else:
                print("hey")
                # face recognition

                display, info = find_face(display)
                prev_error = position_adjustment(drone, info, w, pid, prev_error)

        # keyboard controls
        val = keyboard_input()

        drone.send_rc_control(val[3], val[2], val[1], val[0])
        time.sleep(0.05)

    drone.streamoff()
except TypeError:
    print("did not find drone")
    drone.streamoff()
    quit()