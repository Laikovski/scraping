#parser for store without oop
from selenium import webdriver
import csv

driver = webdriver.Firefox(executable_path=r'gecko/geckodriver')
driver.get('https://www.21vek.by/notebooks/')

def main():
    def get_count_page():
        """get count page for category"""
        count_page = driver.find_element_by_class_name('cr-paging_nav').text
        pages = count_page.split('/')
        res = int(pages[-1].rstrip(' >'))
        return res
    get_count_page()
    #get information from links
    for item in range(1, get_count_page()):
        driver.get(f'https://www.21vek.by/notebooks/page:{item}')
        block = driver.find_elements_by_class_name('result__item')
        for item in block:
            arr = []
            name = item.find_element_by_class_name('result__name').text
            price = item.find_elements_by_class_name('j-item-data')
            res_price = ''
            for i in price:
                if i.text == False:
                    res_price = 'none'
                else:
                    res_price = i.text

            table = item.find_elements_by_tag_name('tr')
            for table_item in table:
                td = table_item.find_element_by_xpath('td[2]')
                arr.append(td.text)
            if len(arr) < 6:
                diagonal, extension, ram, hdd = 'None', 'None', 'None', 'None'
            else:
                diagonal, extension, ram, hdd = arr[0], arr[1], arr[4], arr[5]
            print(name, res_price, diagonal, extension, ram, hdd)

            #write information to file
            csv_file = 'export.csv'
            with open(csv_file, 'a') as csvfile:
                fieldnames = ['Название', 'Цена','Экран', 'Разрешение', 'RAM', 'SSD']
                writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
                # writer.writeheader()
                writer.writerow({'Название': name, 'Цена': res_price, 'Экран': diagonal, 'Разрешение': extension, 'RAM': ram,  'SSD': hdd})

if __name__ == '__main__':
    main()
