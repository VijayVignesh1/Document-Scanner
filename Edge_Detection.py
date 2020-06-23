import cv2

def detect_edges(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    output = cv2.Canny(img_blur, 70, 200)
    return output

if __name__ == '__main__':

    test = cv2.imread('test_processed.jpg')
    test = detect_edges(test)
    cv2.imshow("Edged", test)
    cv2.waitKey(0)
    cv2.destroyAllWindows()