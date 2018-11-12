from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import os
import sys
import time 
import boto3
import datetime
import logging
import json
import argparse
import datetime

def main():
    start = time.time()

    #Setup Logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    #Parse Arguments and Set Defaults
    now = datetime.datetime.now()
    parser = argparse.ArgumentParser(description='Arguments to query reservation details.')
    parser.add_argument('-t', '--time', default='dinner', help="Currently supports a comma separated list of times including 'breakfast' 'lunch' 'dinner'") 
    parser.add_argument('-d', '--date', default=now.strftime("%m/%d/%Y"), help='A comma separated list of dates in the format mm/dd/yyyy')
    parser.add_argument('-s', '--size', default='2', help='A comma separated list of integers between 1 and 49')  
    parser.add_argument('-l', '--location', default='''Cinderella's Royal Table''', help="Currently supports a comma separated list of quoted string locations including 'Cinderella's Royal Table' and 'Chef Mickey's'")  
    parser.add_argument('-n', '--notification', default=None, help='SNS ARN for Notification Topic')  
    parser.add_argument('--debug', help="set debug level logging", action="store_true")
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    locationLst = args.location.split(',')
    partyTimeLst = args.time.split(',')
    partySizeLst = args.size.split(',')
    reservationDateLst = args.date.split(',')
    notificationARN = args.notification

    logging.debug('Location(s): ' + str(locationLst))
    logging.debug('Party Size: ' + str(partySizeLst))
    logging.debug('Party Time(s): ' + str(partyTimeLst))
    logging.debug('Date(s): ' + str(reservationDateLst))
    logging.debug('Notification ARN: ' + str(notificationARN))

    disneyReservation(locationLst, partyTimeLst,partySizeLst,reservationDateLst,notificationARN)
    end = time.time()
    logging.debug('Elapsed Time: '+ str(start-end))

def disneyReservation(locationLst, partyTimeLst,partySizeLst,reservationDateLst,notificationARN):
    chrome_options = Options()  
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument("--test-type")
    chrome_options.add_argument("--js-flags=--expose-gc")
    chrome_options.add_argument("--enable-precise-memory-info")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--window-size=1024,1000")
    driver = webdriver.Chrome(chrome_options=chrome_options)  


    for location in locationLst:
        if location=='''Chef Mickey's''':
            url = 'https://disneyworld.disney.go.com/dining/contemporary-resort/chef-mickeys/'
        if location=='''Cinderella's Royal Table''':
            url = 'https://disneyworld.disney.go.com/dining/magic-kingdom/cinderella-royal-table/'
        driver.get(url)
        logging.debug("Got Page")
        for partyTime in partyTimeLst:
            #Select Time
            driver.find_element_by_id("searchTime-wrapper").click()
            time.sleep(0)
            xpath_timeLoc = '''//li[@data-display=\"''' +partyTime+ '''\"]'''
            driver.find_element_by_xpath(xpath_timeLoc).click()
            logging.debug("Finished Time")
            
            for partySize in partySizeLst:
                #Select Party Size
                driver.find_element_by_id("partySize-wrapper").click()
                time.sleep(0)
                xpath_sizeLoc = '''//li[@data-value=\"''' +partySize+ '''\"]'''
                driver.find_element_by_xpath(xpath_sizeLoc).click()
                logging.debug("Finished Party Size")
                
                for reservationDate in reservationDateLst:
                    #Select Date
                    date = driver.find_element_by_id("diningAvailabilityForm-searchDate")
                    time.sleep(0)
                    date.send_keys(Keys.CONTROL + "a")
                    date.send_keys(Keys.DELETE)
                    date.send_keys(reservationDate)
                    driver.find_element_by_id("checkAvailability").click()
                    logging.debug("Finished Date")
                    
                    #Determine Availability
                    driver.find_element_by_id("dineAvailSearchButton").click()
                    time.sleep(4)
                    try:
                        results = driver.find_element_by_class_name("ctaNoAvailableTimesContainer")
                    except:
                        results = driver.find_element_by_class_name("ctaAvailableTimesContainer")
                        if notificationARN:
                            logging.debug('In Notification')
                            client = boto3.client('sns', region_name='us-east-1')
                            client.publish(
                                TargetArn=notificationARN,
                                Message=json.dumps({'default': 'Default Message',
                                                    'sms': 'Available Time at ' + location + ' for ' + partySize + ' people on ' + reservationDate + ' at ' + results.text,
                                                    'email': 'Available Time at ' + location + ' for ' + partySize + ' people on ' + reservationDate + ' at ' + results.text}),
                                Subject='A New Reservation is Available',
                                MessageStructure='json'
                            )
                    result = location + ' for ' + partySize + ' people on ' + reservationDate + ' for ' + partyTime, 'Results: '+ results.text.splitlines()[0]
                    logging.info(result)
    driver.close()

if __name__ == "__main__": main()