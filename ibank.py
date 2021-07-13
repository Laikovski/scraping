import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json


options = Options()
options.add_argument('-profile')
options.add_argument('/home/laikov/Desktop/projects/scraping/profile')

driver = webdriver.Firefox(executable_path=r'gecko/geckodriver', options=options, service_args=['--marionette-port', '2828'])

page = driver.get('https://www.ibanknet.com/scripts/callreports/fiList.aspx?type=031')
links = driver.find_elements_by_class_name('pagebody')

# get links from main page
list_link = []
for i in links:
    if i.get_attribute('href'):
        list_link.append(i.get_attribute('href'))

new_dict = []


def scraping_info():
    """get information from page and add to dictionary"""

    # common information
    name = driver.find_element_by_class_name('blockuhilite').text
    certificate = driver.find_element_by_css_selector('td.instinfo:nth-child(1)').text

    # adress and site
    adress_line_1 = driver.find_element_by_xpath("//table[@width='95%']/tbody/tr[2]/td[1]").text
    adress_line_2 = driver.find_element_by_xpath("//table[@width='95%']/tbody/tr[3]/td[1]").text
    full_adress = f'{adress_line_1} {adress_line_2}'
    web_site = driver.find_element_by_xpath("//table[@width='95%']/tbody/tr[4]/td[1]").text

    # common information
    year_opened = driver.find_element_by_xpath("//table[@class='hrbgcolor3']/tbody/tr[2]/td[2]").text
    entity_type = driver.find_element_by_xpath("//table[@class='hrbgcolor3']/tbody/tr[3]/td[2]").text
    number_of_offices = driver.find_element_by_xpath("//table[@class='hrbgcolor3']/tbody/tr[11]/td[2]").text
    try:
        employees = driver.find_element_by_xpath("//table[@class='hrbgcolor3']/tbody/tr[11]/td[4]").text
    except:
        employees = None

    # financial information
    total_assets = driver.find_element_by_xpath("//html/body/table/tbody/tr/td/table[2]/tbody/tr/td["
                                                "3]/table/tbody/tr[1]/td[5]/table/tbody/tr/td/font/center["
                                                "4]/table/tbody/tr[3]/td[2]").text

    liabilities = driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table[2]/tbody/tr/td[3]/table/tbody/tr["
                                               "1]/td[5]/table/tbody/tr/td/font/center[4]/table/tbody/tr[4]/td[2]").text

    total_capital = driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table[2]/tbody/tr/td["
                                                 "3]/table/tbody/tr[1]/td[5]/table/tbody/tr/td/font/center[4]/table/tbody/tr[12]/td[2]").text

    total_deposits = driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table[2]/tbody/tr/td["
                                                  "3]/table/tbody/tr[1]/td[5]/table/tbody/tr/td/font/center[4]/table/tbody/tr[7]/td[2]").text

    # create dictionary
    new_dict.append({
        'name': name,
        'adress':full_adress,
        'web': web_site,
        'certificates': certificate,
        'year': year_opened,
        'type': entity_type,
        'oficess': number_of_offices,
        'employees': employees,
        'deposits': total_deposits,
        'assets': total_assets,
        'capital': total_capital,
        'liabilities': liabilities
        })


for n, link in enumerate(list_link):
    page = driver.get(link)
    if n == 0 or n == 30 or n == 60 or n == 90:
        input("Press ENTER after filling CAPTCHA")
        scraping_info()
    else:
        time.sleep(1)
        scraping_info()

# write to file
with open('data.json', 'w') as outfile:
    json.dump(new_dict, outfile, indent=4)

driver.quit()