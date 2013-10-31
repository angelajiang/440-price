from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time
import socket

cities = ['CHI',
        'NYC']

d_expedia = dict([('url', 'http://www.expedia.com'),
            ('origin_id','uw_flight_origin_input'),
            ('dest_id', 'uw_flight_destination_input'),
            ('dep_id', 'uw_flight_dep_date_input'),
            ('ret_id', 'uw_flight_return_date_input'),
            ('submit_id', 'uw_flight_submit_lnk')
            ])

d_travelocity = dict([('url', 'http://www.travelocity.com/flights'),
            ('origin_id','fo-from'),
            ('dest_id', 'fo-from'),
            ('dep_id', 'fo-fromdate'),
            ('ret_id', 'fo-todate')
            ])

sites_dict = dict([('expedia', d_expedia),
                ('travelocity', d_travelocity)])

class WebCrawler():

    def __init__(self):
        self.driver = webdriver.Firefox()

    def quit(self):
        self.driver.close()

    def run(self, site):
        driver = self.driver
        d_site = sites_dict[site]
        driver.get(d_site['url'])

        #Test for beta version of Expedia site
        try:
            driver.find_element_by_id(d_site['origin_id'])
        except:
            return

        #Set origin and destination fields
        origin_obj = driver.find_element_by_id(d_site['origin_id'])
        origin_obj.clear()
        origin_obj.send_keys(cities[0])
        dest_obj = driver.find_element_by_id(d_site['dest_id'])
        dest_obj.clear()
        dest_obj.send_keys(cities[1])

        #Set depature and return dates
        self.set_date(d_site['dep_id'], 10)
        self.set_date(d_site['ret_id'], 15)

        #Submit to search flights
        submit = driver.find_element_by_id(d_site['submit_id'])
        submit.click();

        try:
            WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"timeline-row")))
        finally:
            flight_info_list = driver.find_elements_by_class_name('timeline-row')
            #print data to file
            filename = 'data/' + site + time.strftime("-%m-%d-%Y")
            f  = open(filename, 'a+')
            myIp = socket.gethostbyname(socket.gethostname())
            for flight_info in flight_info_list:
                #flight info = dept_time, dept_airport, dept_city, arr_time,
                #arr_airport, air_city, flight_time, cost, cost_unit 
                #info = flight_info.text.split('\n')
                info = flight_info.text.replace('\n', ' | ')
                f.write(time.strftime("%m-%d-%Y %H:%M:%S | ") + info + ' | ' + myIp  + '\n')
            f.close()


    def set_date(self, date_input_id, days_delta):
        #date_input_id: selector id for date input e.g. 'uw_flight_dep_date_input'
        #days_delta: number of days from today
        driver = self.driver
        today = datetime.date.today()
        input_date = today + datetime.timedelta(days=days_delta)
        date_str = input_date.strftime('%m/%d/%Y')
        input_obj = driver.find_element_by_id(date_input_id)
        input_obj.clear()
        input_obj.send_keys(date_str)
        

if __name__ == "__main__":
    crawler = WebCrawler()
    crawler.run('expedia')
    crawler.quit()
