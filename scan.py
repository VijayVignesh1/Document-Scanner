import cv2
from skimage.filters import threshold_local
def scan(img,c_val):
    img=cv2.adaptiveThreshold(img,maxValue=255,blockSize=25,adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,thresholdType=cv2.THRESH_BINARY,C=c_val)
    img=cv2.fastNlMeansDenoising(img,None,2,7,21)
    return img

def scan_adaptive(img,val):
        T = threshold_local(img, val, offset = 10, method = "gaussian")
        warped = (img > T).astype("uint8") * 255
        # cv2.imshow('',warped)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return warped
