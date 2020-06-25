import cv2
import imutils

def detect_edges(img):

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    output = cv2.Canny(img_blur, 70, 200)
    contours, _ = cv2.findContours(output.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(contours, key=cv2.contourArea, reverse=True)

    final_x, final_y, final_w, final_h = cv2.boundingRect(cnts[0])
    initial_area = final_w*final_h
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if w*h > initial_area:
            final_x, final_y, final_w, final_h = x, y, w, h
            initial_area = w*h

    if final_x<0:
        final_x=0
    elif final_x>img.shape[0]:
        final_x=img.shape[0]-1
    if final_y<0:
        final_y=0
    elif final_y>img.shape[1]:
        final_y=img.shape[1]-1        
    top_left, top_right = (final_x, final_y), (final_x + final_w, final_y)
    bottom_left, bottom_right = (final_x, final_y + final_h), (final_x + final_w, final_y + final_h)

    ################## Debug
    # print(top_left, bottom_left, bottom_right, top_right)
    #
    # corners = cv2.circle(img, top_left, radius=4, color=(0, 0, 255), thickness=-1)
    # corners = cv2.circle(img, top_right, radius=4, color=(0, 0, 255), thickness=-1)
    # corners = cv2.circle(img,  bottom_left, radius=4, color=(0, 0, 255), thickness=-1)
    # corners = cv2.circle(img, bottom_right, radius=4, color=(0, 0, 255), thickness=-1)
    # cv2.imshow("Corners", corners)
    # img = cv2.rectangle(img, (final_x, final_y), (final_x + final_w, final_y + final_h), (0, 255, 0), 2)
    # cv2.imshow("Final", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return output, (top_left, bottom_left, bottom_right, top_right)

if __name__ == '__main__':

    test = cv2.imread('Test Images/book_page_1.jpg')
    test, pts = detect_edges(test)
    cv2.imshow("Edged", test)
    cv2.waitKey(0)
    cv2.destroyAllWindows()