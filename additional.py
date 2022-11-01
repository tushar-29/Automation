from selenium import webdriver


chrome_path = 'D:\python_file\LearningProjects\chromedriver.exe'

driver = webdriver.Chrome(executable_path=chrome_path)
driver.maximize_window()

url = 'https://www.myntra.com/'


driver.get(url)


