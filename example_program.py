from time import sleep
import cv2 as cv
import random

def do_something(path):
    print("Doing something here:", path)
    sleep(10)
    return "Done " + path


def read_images_and_flip(image_path_list, ):

    flip_img_list = []
    flip_img_dict = {}
    image_counts = {}

    for img_path_num in range(len(image_path_list)):
        # img
        img = cv.imread(image_path_list[img_path_num])
        img_flip = cv.flip(img, 1)


        # count
        rand_num = random.randint(500, 1000)

        flip_img_list.append(img_flip)
        flip_img_dict[img_path_num] = img_flip
        image_counts[img_path_num] = rand_num

    return flip_img_dict, image_counts
