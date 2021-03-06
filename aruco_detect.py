import numpy as np
import cv2
import params
import cv2.aruco as aruco
import time
import math

# local modules
import params
from camera_helper import USBVideoStream, PicVideoStream, FPS

if __name__ == "__main__":
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_1000)
    stream = PicVideoStream("/home/hongji-li/cam_plane", "default_typhoon_h480_cgo3_camera_link_camera(1)-", sync=True).start()

    while True:
        # Capture frame-by-frame
        ret, frame = stream.read()

        corners, ids, rejecttedImgPoints = aruco.detectMarkers(frame, aruco_dict)
        frame = aruco.drawDetectedMarkers(frame, corners, ids)

        if ids is not None:    
            rvecs, tvecs = aruco.estimatePoseSingleMarkers(corners, 0.15, params.mtx, params.dist)
            print(rvecs, tvecs)
            prompt_strings = []
            vecs = list(zip(rvecs, tvecs))
            for rvec, tvec in vecs:
                frame = aruco.drawAxis(frame, params.mtx, params.dist, rvec, tvec, 0.15)
                prompt_strings.append("x:{:.2f} y:{:.2f} z:{:.2f}".format(*(tvec[0])))
                prompt_strings.append("x:{:.2f} y:{:.2f} z:{:.2f}".format(*(rvec[0])))
            cv2.putText(frame, '\n'.join(prompt_strings), (25,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1)
        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # When everything done, stop the stream
    stream.stop()
    print("average fps", stream.get_fps())
    cv2.destroyAllWindows()
