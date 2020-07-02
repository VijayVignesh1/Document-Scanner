import numpy as np
import cv2

def image_splitter(img):
    w, h, _ = img.shape
    img_split = []

    if w >= h:
        factor = round(h/256)
    else:
        factor = round(w/256)

    resized_img = cv2.resize(img, (256*factor, 256*factor), interpolation=cv2.INTER_CUBIC)
    print(resized_img.shape)

    temp = [[None for i in range(factor)] for j in range(factor)]
    for i in range(1, factor+1):
        for j in range(1, factor+1):

            temp[i-1][j-1] = resized_img[256*(i-1):256*i, 256*(j-1):256*j, :]

    return np.asarray(temp)

def img_merger(img_list):
    l = img_list.shape[0]

    print(img_list.shape)
    print(l)

    temp = []
    for i in range(l):
        temp.append(cv2.hconcat(img_list[i]))
    final_img = cv2.vconcat(temp)

    return final_img


if __name__ == '__main__':
    test_img = cv2.imread("Test Images/book.jpg")
    print("Actual image size", test_img.shape)
    cv2.imshow("Original Image", test_img)

    result = image_splitter(test_img)

    print(result.shape)

    for i in range(len(result)):
        for j in range(len(result[0])):
            cv2.imshow("Split", result[i][j])
            cv2.waitKey(0)

    test_output = img_merger(result)
    # print(test_output.shape)
    # print(test_output)
    cv2.imshow("Merged", test_output)
    cv2.waitKey(0)


    cv2.destroyAllWindows()