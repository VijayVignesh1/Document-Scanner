import cv2
import imutils

def detect_edges(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    output = cv2.Canny(img_blur, 70, 200)
    _, contours, _ = cv2.findContours(output.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:6]

    for c in cnts:

        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            edge_pts = approx
            break

    top_left, bottom_left, bottom_right, top_right = edge_pts[0][0], edge_pts[1][0], edge_pts[2][0], edge_pts[3][0]

    ################## Debug
    # print(top_left, bottom_left, bottom_right, top_right)
    # print(len(edge_pts))
    #
    # for pt in edge_pts:
    #
    #     img = cv2.circle(img, (pt[0][0], pt[0][1]), radius=2, color=(0, 0, 255), thickness=-1)
    # cv2.imshow("Corners", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return output, (top_left, bottom_left, bottom_right, top_right)

if __name__ == '__main__':

    test = cv2.imread('test_processed.jpg')
    test, pts = detect_edges(test)
    cv2.imshow("Edged", test)
    cv2.waitKey(0)
    cv2.destroyAllWindows()