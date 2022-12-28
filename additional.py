from selenium import webdriver
from time import sleep

element_data = [{"name": "GetExtra", "x_cod": 1174, "y_cod": 829, "height": 45, "width": 207, "img_url": "img/scrap_img/GetExtra.png", "website": "myntr"}, {"name": "Buy", "x_cod": 1039, "y_cod": 829, "height": 51, "width": 90, "img_url": "img/scrap_img/Buy.png", "website": "myntr"}, {"name": "Calvin", "x_cod": 1451, "y_cod": 578, "height": 50, "width": 151, "img_url": "img/scrap_img/Calvin.png", "website": "myntr"}, {"name": "NOW", "x_cod": 1159, "y_cod": 447, "height": 35, "width": 86, "img_url": "img/scrap_img/NOW.png", "website": "myntr"}, {"name": "Starting", "x_cod": 1373, "y_cod": 324, "height": 67, "width": 224, "img_url": "img/scrap_img/Starting.png", "website": "myntr"}, {"name": "Styles", "x_cod": 1188, "y_cod": 323, "height": 68, "width": 174, "img_url": "img/scrap_img/Styles.png", "website": "myntr"}, {"name": "ALLNEWCOLLECTION25K+Styles|StartingAt*299+SHOPNOW]ONLY(CalinikleinFLAT=200OFFaz", "x_cod": 0, "y_cod": 145, "height": 591, "width": 1904, "img_url": "img/scrap_img/ALLNEWCOLLECTION25K+Styles|StartingAt*299+SHOPNOW]ONLY(CalinikleinFLAT=200OFFaz.png", "website": "myntr"}, {"name": "BEAUTY", "x_cod": 672, "y_cod": 35, "height": 22, "width": 74, "img_url": "img/scrap_img/BEAUTY.png", "website": "myntr"}, {"name": "HOME&LIVING", "x_cod": 501, "y_cod": 35, "height": 22, "width": 135, "img_url": "img/scrap_img/HOME&LIVING.png", "website": "myntr"}, {"name": "KIDS", "x_cod": 419, "y_cod": 35, "height": 22, "width": 46, "img_url": "img/scrap_img/KIDS.png", "website": "myntr"}, {"name": "WOMEN", "x_cod": 307, "y_cod": 35, "height": 22, "width": 76, "img_url": "img/scrap_img/WOMEN.png", "website": "myntr"}, {"name": "MEN", "x_cod": 227, "y_cod": 35, "height": 22, "width": 45, "img_url": "img/scrap_img/MEN.png", "website": "myntr"}, {"name": "Searchforproducts,brandsandmore", "x_cod": 984, "y_cod": 33, "height": 25, "width": 278, "img_url": "img/scrap_img/Searchforproducts,brandsandmore.png", "website": "myntr"}, {"name": "STUDIO\u201cEW", "x_cod": 781, "y_cod": 31, "height": 26, "width": 106, "img_url": "img/scrap_img/STUDIO\u201cEW.png", "website": "myntr"}, {"name": "QWishlist", "x_cod": 1709, "y_cod": 25, "height": 47, "width": 61, "img_url": "img/scrap_img/QWishlist.png", "website": "myntr"}, {"name": "Bag", "x_cod": 1798, "y_cod": 24, "height": 51, "width": 31, "img_url": "img/scrap_img/Bag.png", "website": "myntr"}, {"name": "Profile", "x_cod": 1636, "y_cod": 23, "height": 49, "width": 49, "img_url": "img/scrap_img/Profile.png", "website": "myntr"}]

chrome_path = r'D:\python_file\LearningProjects\chromedriver.exe'

URL = 'https://www.myntra.com/'

driver = webdriver.Chrome(executable_path=chrome_path)
driver.maximize_window()
driver.get(URL)
action = webdriver.ActionChains(driver)


for data in element_data:
    x_loc = data['x_cod'] + (data['width'] / 2)
    y_loc = data['y_cod'] + (data['height'] / 2)
    action.move_by_offset(data["x_cod"], data["y_cod"]).click()
    sleep(5)
