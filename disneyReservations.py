from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import os
import time 
import boto3
import datetime
import logging
import json

def disneyReservation(location, partyTimeLst,partySizeLst,reservationDateLst):
    logging.basicConfig(filename='/opt/disneyReservations/disneyReservations.log', format='%(asctime)s %(message)s', level=logging.INFO)

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
    chrome_options.binary_location = "/opt/disneyReservations/bin/headless-chromium"

    #Setup
    driver = webdriver.Chrome(executable_path='/opt/disneyReservations/bin/chromedriver', chrome_options=chrome_options)  
    if location=='''Chef Mickey's''':
        url = 'https://disneyworld.disney.go.com/dining/contemporary-resort/chef-mickeys/'
    if location=='''Cinderella's Royal Table''':
        url = 'https://disneyworld.disney.go.com/dining/magic-kingdom/cinderella-royal-table/'
    driver.get(url)
    logging.debug("Got Page")
    for partyTime in partyTimeLst:
        for partySize in partySizeLst:
            for reservationDate in reservationDateLst:
                #Select Party Size
                driver.find_element_by_id("partySize-wrapper").click();
                time.sleep(5)
                xpath_sizeLoc = '''//li[@data-value=\"''' +partySize+ '''\"]'''
                driver.find_element_by_xpath(xpath_sizeLoc).click();
                logging.debug("Finished Party Size")

                #Select Time
                driver.find_element_by_id("searchTime-wrapper").click();
                time.sleep(5)
                xpath_timeLoc = '''//li[@data-display=\"''' +partyTime+ '''\"]'''
                driver.find_element_by_xpath(xpath_timeLoc).click();
                logging.debug("Finished Time")

                #Select Date
                date = driver.find_element_by_id("diningAvailabilityForm-searchDate");
                time.sleep(10);
                date.send_keys(Keys.CONTROL + "a");
                date.send_keys(Keys.DELETE);
                date.send_keys(reservationDate);
                driver.find_element_by_id("checkAvailability").click();
                logging.debug("Finished Date")
                
                #Determine Availability
                driver.find_element_by_id("dineAvailSearchButton").click()
                time.sleep(10);
                try:
                    results = driver.find_element_by_class_name("ctaNoAvailableTimesContainer")
                except:
                    results = driver.find_element_by_class_name("ctaAvailableTimesContainer")
                    client = boto3.client('sns')
                    response = client.publish(
                        TargetArn='arn:aws:sns:us-east-1:679695450108:DisneyRes',
                        Message=json.dumps({'default': 'Default Message',
                                            'sms': 'Available Time at ' + location + ' for: ' + partySize + ' people on ' + reservationDate + ' at ' + results.text,
                                            'email': 'Available Time at ' + location + ' for: ' + partySize + ' people on ' + reservationDate + ' at ' + results.text}),
                        Subject='A New Reservation is Available',
                        MessageStructure='json'
                    )
                result = location + ' for: ' + partySize + ' people on ' + reservationDate + ' for ' + partyTime, 'Results: '+ results.text.splitlines()[0]
                print(result)
                logging.info(result)
    logging.debug("Done")
    driver.close()

disneyReservation('''Cinderella's Royal Table''', ['breakfast'],['6','4'],['02/05/2019','02/06/2019','02/07/2019'])
disneyReservation('''Chef Mickey's''', ['breakfast'],['6','4'],['02/05/2019','02/06/2019','02/07/2019'])