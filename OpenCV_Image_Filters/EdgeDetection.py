import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame_in = cap.read()
    # frame_hsv = cv2.cvtColor(frame_in,cv2.COLOR_BGR2HSV)
    # frame_hsv[...,1] = frame_hsv[...,1]*1.4
    # # frame_hsv[...,2] = frame_hsv[...,2]*0.6
    # frame = cv2.cvtColor(frame_hsv,cv2.COLOR_HSV2BGR)
    frame = frame_in

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);

    # filter = cv2.Canny(frame,50,155)
    bgr_denoised = cv2.GaussianBlur(frame,(3,3),0)
    filter = cv2.Canny(bgr_denoised,25,100)

    # denoised = cv2.GaussianBlur(frame_gray,(3,3),0)
    # # filter = cv2.Laplacian(denoised,cv2.CV_64F)
    # filter = cv2.Laplacian(denoised,cv2.CV_64F)
    # bgr_filter = cv2.Laplacian(bgr_denoised,cv2.CV_64F,scale=2)
    # bgr_filter = cv2.convertScaleAbs(bgr_filter)
    # filter = bgr_filter
    # filter = cv2.convertScaleAbs(filter)
    bgr_filter = cv2.cvtColor(filter, cv2.COLOR_GRAY2BGR);
    mixed = cv2.addWeighted(frame, 1, bgr_filter, 0.5, 0.0);
    # Display the resulting frame
    cv2.imshow('frame',frame)
    # cv2.imshow('frame_gray',frame_gray)
    cv2.imshow('filter',filter)
    cv2.imshow('mixed',mixed)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


#
# import cv2
# import numpy as np
# from matplotlib import pyplot as plt
#
# cap = cv2.VideoCapture(0)
#
# img = cv2.imread('messi5.jpg',0)
# edges = cv2.Canny(img,100,200)
#
# plt.subplot(121),plt.imshow(img,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(edges,cmap = 'gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
#
# plt.show()
