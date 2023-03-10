import cv2
import numpy as np
from selenium import webdriver
import pytesseract
import re
from time import sleep


chrome_path = 'D:\python_file\LearningProjects\chromedriver.exe'
pytesseract.pytesseract.tesseract_cmd = 'D:\other\module\\tesseract.exe'


def open_website(url):
    driver = webdriver.Chrome(executable_path=chrome_path)
    driver.maximize_window()
    driver.get(url)
    sleep(1)
    driver.get_screenshot_as_file(f"static/img/scrap_img/{url[12:17]}.png")
    driver.close()
    image = cv2.imread(f"static/img/scrap_img/{url[12:17]}.png", cv2.IMREAD_COLOR)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    return image


def image_processing(image):
    # Convert the image to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Kernel size increases or decreases the area of the rectangle to be detected.
    # A smaller value like (10, 10) will detect each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))

    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    return contours


def get_web_elements(detected_data, image, WEBSITE_URL):
    element_set = set()
    element_data = []
    for element in detected_data:
        # x coordinate, y cordinate, height and width of element
        x, y, w, h = cv2.boundingRect(element)

        # Cropping the text block for giving input to OCR
        cropped_box = image[y:y + h, x:x + w]

        # Apply OCR on the cropped image
        box_data = pytesseract.image_to_string(cropped_box)

        #basic text filteration
        box_data = re.sub('\s+', '', box_data)

        if box_data != "" and box_data not in element_set:
            img = cv2.cvtColor(np.array(cropped_box), cv2.COLOR_RGB2BGR)
            cv2.imwrite(f"static/img/scrap_img/{box_data}.png", img)

            # Drawing a rectangle on copied image
            rect = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            element_set.add(box_data)
            element_data.append({
                'img_url': f'img/scrap_img/{box_data}.png',
                'name': box_data,
                'x_cod': x,
                'y_cod': y,
                'height': h,
                'width': w,
                'website': WEBSITE_URL[12:17],
                'main_name': box_data
            })

    rect = cv2.cvtColor(np.array(rect), cv2.COLOR_RGB2BGR)
    cv2.imwrite(f"static/img/scrap_img/{WEBSITE_URL[12:17]}_box.png", rect)
    return element_data


def get_website_data(url):
    if not url or url == "":
        return

    image = open_website(url)
    detected_regions = image_processing(image)
    element = get_web_elements(detected_regions, image, url)
    return element


def custom_detection(element_data, url):
    x_cod, y_cod, height, width = element_data.x_cod, element_data.y_cod, element_data.height, element_data.width
    image = cv2.imread(f"static/img/scrap_img/{url}.png", cv2.IMREAD_COLOR)

    cropped_box = image[y_cod:(y_cod + height), x_cod:(x_cod + width)]
    new_crop_img = cv2.cvtColor(np.array(cropped_box), cv2.COLOR_RGB2BGR)
    box_data = pytesseract.image_to_string(new_crop_img)

    box_data = re.sub('\s+', '', box_data)

    element_data.main_name = box_data

    cv2.imwrite(f"static/img/scrap_img/{element_data.name}.png", new_crop_img)
    element_data.img_url = f"img/scrap_img/{element_data.name}.png"

    box_img = cv2.imread(f"static/img/scrap_img/{url}_box.png", cv2.IMREAD_COLOR)
    rect = cv2.rectangle(box_img, (x_cod, y_cod), (x_cod + width, y_cod + height), (0, 255, 0), 2)
    rect = cv2.cvtColor(np.array(rect), cv2.COLOR_RGB2BGR)
    cv2.imwrite(f"static/img/scrap_img/{url}_box.png", rect)

    return element_data


if __name__ == "__main__":
    element_data = get_website_data('https://www.myntra.com/')
    for data in element_data:
        print(data['img_url'])
        print(data['name'])
        print(data['x_cod'])
        print()