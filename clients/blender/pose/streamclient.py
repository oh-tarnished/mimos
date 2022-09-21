import cv2
import zmq
import base64
import numpy as np

# create zmq context
context = zmq.Context()

# create zmq PUB socket for keypoints & stream
stream_socket = context.socket(zmq.SUB)
stream_socket.bind("tcp://*:6666")
stream_socket.setsockopt_string(zmq.SUBSCRIBE, "")

print("Listening to tcp://localhost:6666 ...")

# start listening to stream from zeromq server
while True:
    try:
        stream_resp = stream_socket.recv_string()
        img = base64.b64decode(stream_resp)
        npimg = np.fromstring(img, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)
        cv2.imshow("image", source)
        cv2.waitKey(1)

    except KeyboardInterrupt:
        print("keyboard interrruption....")
        stream_socket.close()
        context.release()
        cv2.destroyAllWindows()
        break
