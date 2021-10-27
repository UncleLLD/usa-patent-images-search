import cv2
import sys
import numpy

PADDING_VALUE = 10
TOP_Y = 20
TOP_X = 100

def crop_image(image, ocr_data):
    img = cv2.imread(image) if isinstance(image, str) else image
    h, w, _ = img.shape
    print(h, w)

    image_position = get_area_order(ocr_data)

    for k, v in ocr_data.items():
        image_name = k + '.jpg'
        box_coord = v
        left_upper_coord = box_coord[0]
        right_upper_coord = box_coord[1]
        right_down_coord = box_coord[2]
        left_down_coord = box_coord[3]
        b_h = left_down_coord[1] - left_upper_coord[1]
        b_w = right_down_coord[0] - left_down_coord[0]
        coord_list = []
        if b_w > b_h:   # 横着的
            x1, y1 = left_upper_coord
            x2, y2 = right_upper_coord

            y_start = TOP_Y
            for position in image_position:
                x_1, y_1 = position
                if x_1 <= x2 and x_1 >= x1 and y1 > y_1:
                    if y_1 > y_start:
                        y_start = y_1

            # left-right must have element
            for x in range(x1, x2):
                for j in range(y_start, y1):
                    pixel = img[j, x]
                    if pixel.tolist() != [255, 255, 255]:
                        coord_list.append((x, j))

            left_flag = True
            while left_flag and x1 > 0:  # left move x1
                len_coord = len(coord_list)
                for j in range(y_start, y1):
                    pixel = img[j, x1]
                    if pixel.tolist() != [255, 255, 255]:
                        coord_list.append((x1, j))
                if len(coord_list) - len_coord > 1:
                    left_flag = True
                    x1 = x1 - 1 if x1 > 1 else 0
                else:
                    left_flag = False

            right_flag = True
            while right_flag and x2 < w:  # right move x2
                len_coord = len(coord_list)
                for j in range(y_start, y1):
                    pixel = img[j, x2]
                    if pixel.tolist() != [255, 255, 255]:
                        coord_list.append((x2, j))
                if len(coord_list) - len_coord > 1:
                    right_flag = True
                    x2 = x2 + 1 if x2 < w-1 else w - 1
                else:
                    right_flag = False
        else:  # 竖着的
            x1, y1 = left_upper_coord
            x2, y2 = left_down_coord

            # left-right must have element
            print(y1, y2)
            print(TOP_X, x1)

            x_start = TOP_X
            for position in image_position:
                x_1, y_1 = position
                if y_1 <= y2 and y_1 >= y1 and x1 > x_1:
                    if x_1 > y_start:
                        x_start = x_1

            for y in range(y1, y2):
                for i in range(x_start, x1):
                    pixel = img[y, i]
                    # print(pixel)
                    if pixel.tolist() != [255, 255, 255]:
                        coord_list.append((i, y))

            down_flag = True
            while down_flag and y1 > 0:  # upper move y1
                len_coord = len(coord_list)
                for i in range(x_start, x1):
                    pixel = img[y1, i]
                    if pixel.tolist() != [255, 255, 255]:
                        coord_list.append((i, y1))
                if len(coord_list) - len_coord > 1:
                    down_flag = True
                    y1 = y1 - 1 if y1 > 0 else 0
                else:
                    down_flag = False

            upper_flag = True
            while upper_flag and y2 < h:  # down move y2
                len_coord = len(coord_list)
                for i in range(x_start, x1):
                    pixel = img[y2, i]
                    if pixel.tolist() != [255, 255, 255]:
                        coord_list.append((i, y2))
                if len(coord_list) - len_coord > 1:
                    upper_flag = True
                    y2 = y2 + 1 if y2 < h-1 else h-1
                else:
                    upper_flag = False


        min_x, min_y, max_x, max_y = get_box_sub_img(coord_list)
        print(min_x, min_y, max_x, max_y)
        object_img = img[min_y-PADDING_VALUE: max_y+PADDING_VALUE, min_x-PADDING_VALUE: max_x+PADDING_VALUE]
        cv2.imwrite(image_name, object_img)


def get_box_sub_img(coord_list):
    xs = []
    ys = []
    for coord in coord_list:
        xs.append(coord[0])
        ys.append(coord[1])
    min_x = min(xs) if len(xs) > 0 else 0
    max_x = max(xs) if len(xs) > 0 else 0
    min_y = min(ys) if len(ys) > 0 else 0
    max_y = max(ys) if len(ys) > 0 else 0
    return min_x, min_y, max_x, max_y


def get_area_order(ocr_data):
    image_position = []
    for k, v in ocr_data.items():
        box_coord = v
        left_upper_coord = box_coord[0]
        right_upper_coord = box_coord[1]
        right_down_coord = box_coord[2]
        left_down_coord = box_coord[3]

        x1, y1 = left_upper_coord
        x2, y2 = right_down_coord
        x_center = int((x1+x2)/2)
        y_center = int((y1+y2)/2)
        image_position.append((x_center, y_center))
    return image_position


# ocr_data = {'fig1': [[370,924],[530,934],[530,965],[370,965]]}

ocr_data = {
    'fig2': [[159,331],[272,331],[272,361],[159,361]],
    'fig3': [[158,819],[269,819],[269,848],[158,848]],
    'fig4':[[481,820],[593,820],[593,849],[481,849]]}
# ocr_data = {'fig1': [[571,504],[600,506],[598,586],[569,585]]}
image_path = sys.argv[1]
crop_image(image_path, ocr_data)