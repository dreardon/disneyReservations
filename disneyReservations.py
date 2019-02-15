from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from argparse import RawTextHelpFormatter
import os
import sys
import time 
import boto3
import datetime
import logging
import json
import argparse, textwrap
import datetime
from selenium.common.exceptions import NoSuchElementException
import chromedriver_binary

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
    parser = argparse.ArgumentParser(description='Arguments to query reservation details.', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-t', '--time', default='6:00pm', help="Currently supports a comma separated list of times including 'breakfast' 'lunch' 'dinner' '7:00am' '6:00pm'") 
    parser.add_argument('-d', '--date', default=now.strftime("%m/%d/%Y"), help='A comma separated list of dates in the format mm/dd/yyyy')
    parser.add_argument('-s', '--size', default='2', help='A comma separated list of integers between 1 and 49')  
    parser.add_argument('-l', '--location', default='''Cinderella's Royal Table''', help=textwrap.dedent('''Currently supports a comma separated list of quoted string locations including
'900 Park Fare'
'Akershus Royal Banquet Hall'
'Cape May Resort'
'Chef Mickey''s'
'Cinderella''s Royal Table'
'Crystal Palace'
'Broadway Concert Series Dining Package'
'Perfectly Princess Tea Party'
'Fantasmic! Dining Package'
'Garden Grill Restaurant'
'Garden Rocks Dinner Package'
'Breakfast with Goofy Ravello'
'Hollywood and Vine'
'Ohana'
'Rivers of Light Dining Package'
'Artists Point'
'Trattoria al Forna'
'Tusker Hour Restaurant'
'Wonderland Tea Party at 1900 Park Fare'
'''))
    parser.add_argument('-n', '--notification', default=None, help='SNS ARN for Notification Topic')  
    parser.add_argument('-r', '--region', default=None, help='AWS Region for SNS Notification') 
    parser.add_argument('--debug', help="set debug level logging", action="store_true")
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    
    if args.notification and not args.region:
        parser.error('The --notification argument requires the --region to be specified')
        sys.exit(1)

    locationLst = args.location.split(',')
    partyTimeLst = args.time.split(',')
    partySizeLst = args.size.split(',')
    reservationDateLst = args.date.split(',')
    notificationARN = args.notification
    region = args.region

    logging.debug('Location(s): ' + str(locationLst))
    logging.debug('Party Size: ' + str(partySizeLst))
    logging.debug('Party Time(s): ' + str(partyTimeLst))
    logging.debug('Date(s): ' + str(reservationDateLst))
    logging.debug('Notification ARN: ' + str(notificationARN))
    logging.debug('Region: ' + str(region))

    disneyReservation(locationLst, partyTimeLst,partySizeLst,reservationDateLst,notificationARN,region)
    end = time.time()
    logging.debug('Elapsed Time: '+ str(start-end))

def disneyReservation(locationLst, partyTimeLst,partySizeLst,reservationDateLst,notificationARN,region):
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
        if location=='''1900 Park Fare''': 
            url = 'https://disneyworld.disney.go.com/dining/grand-floridian-resort-and-spa/1900-park-fare/'
        if location=='''Akershus Royal Banquet Hall''': 
            url = 'https://disneyworld.disney.go.com/dining/epcot/akershus-royal-banquet-hall/'
        if location=='''Cape May Resort''': 
            url = 'https://disneyworld.disney.go.com/dining/beach-club-resort/cape-may-cafe/'
        if location=='''Chef Mickey's''':  
            url = 'https://disneyworld.disney.go.com/dining/contemporary-resort/chef-mickeys/'
        if location=='''Cinderella's Royal Table''': 
            url = 'https://disneyworld.disney.go.com/dining/magic-kingdom/cinderella-royal-table/'
        if location=='''Crystal Palace''': 
            url = 'https://disneyworld.disney.go.com/dining/magic-kingdom/crystal-palace/'
        if location=='''Broadway Concert Series Dining Package''': 
            url = 'https://disneyworld.disney.go.com/dining/epcot/broadway-concert-series-dining-package/'
        if location=='''Perfectly Princess Tea Party''': 
            url = 'https://disneyworld.disney.go.com/dining/grand-floridian-resort-and-spa/perfectly-princess-tea-party/'
        if location=='''Fantasmic! Dining Package''': 
            url = 'https://disneyworld.disney.go.com/dining/hollywood-studios/fantasmic-dining-package/'
        if location=='''Garden Grill Restaurant''': 
            url = 'https://disneyworld.disney.go.com/dining/epcot/garden-grill-restaurant/'
        if location=='''Garden Rocks Dinner Package''': 
            url = 'https://disneyworld.disney.go.com/dining/epcot/garden-rocks-dinner-package/'
        if location=='''Breakfast with Goofy Ravello''': 
            url = 'https://disneyworld.disney.go.com/dining/four-seasons/breakfast-with-goofy-ravello/'
        if location=='''Hollywood and Vine''': 
            url = 'https://disneyworld.disney.go.com/dining/hollywood-studios/hollywood-and-vine/'
        if location==''''Ohana''': 
            url = 'https://disneyworld.disney.go.com/dining/polynesian-resort/ohana/'
        if location=='''Rivers of Light Dining Package''': 
            url = 'https://disneyworld.disney.go.com/dining/animal-kingdom/rivers-of-light-dining-package/'
        if location=='''Artists Point''': 
            url = 'https://disneyworld.disney.go.com/dining/wilderness-lodge-resort/artist-point/'
        if location=='''Trattoria al Forna''': 
            url = 'https://disneyworld.disney.go.com/dining/boardwalk/trattoria-al-forno/'
        if location=='''Tusker Hour Restaurant''': 
            url = 'https://disneyworld.disney.go.com/dining/animal-kingdom/tusker-house-restaurant/'
        if location=='''Wonderland Tea Party at 1900 Park Fare''': 
            url = 'https://disneyworld.disney.go.com/dining/grand-floridian-resort-and-spa/wonderland-tea-party-at-1900-park-fare/'
        driver.get(url)
        logging.debug("Got Page")
        for partyTime in partyTimeLst:
            #Select Time
            driver.find_element_by_id("searchTime-wrapper").click()
            time.sleep(1)
            try:
                xpath_timeLoc = '''//li[@data-display=\"''' +partyTime+ '''\"]'''
                driver.find_element_by_xpath(xpath_timeLoc).click()
                logging.debug("Finished Time")
            except NoSuchElementException:
                result = partyTime + ' is not available on this day'
                logging.info(result)
                sys.exit(1)
            
            for partySize in partySizeLst:
                #Select Party Size
                driver.find_element_by_id("partySize-wrapper").click()
                time.sleep(1)
                xpath_sizeLoc = '''//li[@data-value=\"''' +partySize+ '''\"]'''
                driver.find_element_by_xpath(xpath_sizeLoc).click()
                logging.debug("Finished Party Size")
                
                for reservationDate in reservationDateLst:
                    #Select Date
                    date = driver.find_element_by_id("diningAvailabilityForm-searchDate")
                    date.send_keys(Keys.CONTROL + "a")
                    date.send_keys(Keys.DELETE)
                    date.send_keys(reservationDate)
                    time.sleep(5)
                    driver.find_element_by_id("checkAvailability").click()
                    logging.debug("Finished Date")
                    
                    #Determine Availability
                    driver.find_element_by_id("dineAvailSearchButton").click()
                    try:
                        time.sleep(5)
                        results = driver.find_element_by_class_name("ctaNoAvailableTimesContainer")
                    except:
                        results = driver.find_element_by_class_name("ctaAvailableTimesContainer")
                        if notificationARN:
                            logging.debug('In Notification')
                            client = boto3.client('sns', region_name=region)
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