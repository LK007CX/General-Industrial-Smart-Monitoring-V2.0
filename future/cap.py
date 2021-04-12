import cv2

def main():
    dev = "0"
    width = "1280"
    height = "720"
    gst_str = ('v4l2src device=/dev/video{} ! '
                   'video/x-raw, width=(int){}, height=(int){} ! '
                   'videoconvert ! appsink').format(dev, width, height)

    output_path = './output.avi'
    vc = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)
    ret, frame = vc.read()
    w = int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = vc.get(cv2.CAP_PROP_FPS)
    
    fourcc = cv2.VideoWriter_fourcc('H', '2', '6', '4')
    # fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
    # fourcc = cv2.VideoWriter_fourcc('H', 'E', 'V', 'C')
    vw = cv2.VideoWriter(output_path, fourcc, fps, (w, h), True)
    while ret:
        vw.write(frame)
        ret, frame = vc.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            return -1

if __name__ == '__main__':
    main()