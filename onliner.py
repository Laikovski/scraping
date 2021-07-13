from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
import time

options = Options()
options.add_argument('-profile')
options.add_argument('/home/laikov/Desktop/projects/store_scraping/profile')

driver = webdriver.Firefox(executable_path=r'gecko/geckodriver', options=options, service_args=['--marionette-port', '2828'])


page = driver.get('https://ab.onliner.by/?order=created_at%3Adesc')
links = driver.find_elements_by_class_name('vehicle-form__offers-unit')

car_link = []
for i in range(2):
    car_link.append(f'{links[i].get_attribute("href")}')

for item in car_link:
    driver.get(item)
    id = driver.find_element_by_css_selector('div.vehicle-form__intro-item:nth-child(3)').text
    click_tel = driver.find_element_by_class_name('vehicle-form__button_phone').click()
    time.sleep(5)
    driver.get(item)


    model = driver.find_element_by_tag_name('h1').text
    year = driver.find_element_by_class_name('jest-year').text
    price_car = driver.find_element_by_class_name('vehicle-form__description').text
    get_num = driver.find_element_by_class_name('vehicle-form__button-value').text


    print(get_num)