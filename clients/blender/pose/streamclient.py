import cv2
import numpy as np
import zmq
import base64


ctx = zmq.Context()
stream_socket = ctx.socket(zmq.SUB)
stream_socket.bind("tcp://*:6666")
stream_socket.setsockopt_string(zmq.SUBSCRIBE, "")
frame_count = 0
print("listening to TCP:6666")

# start listening to stream from zeromq server
while True:
    try:
        frame_count += 1
        stream_resp = stream_socket.recv_string()
        img = base64.b64decode(stream_resp)
        npimg = np.fromstring(img, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)
        cv2.imshow("image", source)
        cv2.waitKey(1)

    except KeyboardInterrupt:
        print("keyboard interrruption....")
        cv2.destroyAllWindows()
        break
