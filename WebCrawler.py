from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime

cities = ['Chicago',
        'New York']

d_expedia = dict([('url', 'http://www.expedia.com'),
            ('origin_id','uw_flight_origin_input'),
            ('dest_id', 'uw_flight_destination_input'),
            ('dep_id', 'uw_flight_dep_date_input'),
            ('ret_id', 'uw_flight_return_date_input'),
            ('submit_id', 'uw_flight_submit_lnk')
            ])

sites_dict = dict([('expedia', d_expedia)])

class WebCrawler():

    def __init__(self):
        self.driver = webdriver.Firefox()

    def quit(self):
        self.driver.close()

    def run(self, site):
        driver = self.driver
        d_site = sites_dict[site]
        driver.get(d_site['url'])

        #Set origin and destination fields
        origin_obj = driver.find_element_by_id(d_site['origin_id'])
        dest_obj = driver.find_element_by_id(d_site['dest_id'])
        origin_obj.send_keys('Chicago')
        dest_obj.send_keys('New York')

        #Set depature and return dates
        self.set_date(d_site['dep_id'], 10)
        self.set_date(d_site['ret_id'], 15)

        #Submit to search flights
        submit = driver.find_element_by_id(d_site['submit_id'])
        submit.click();

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
    #crawler.quit()
