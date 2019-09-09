#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Week 2 assignment - Python Standard Library"""

import datetime
import logging
import csv
import sys
import urllib2


def downloadData(url):
    """get CSV file"""
    filedata = urllib2.urlopen(url)
    datatowrite = filedata.read()
    return datatowrite


def processData(contents):
    """process data in CSV file and outbout to assignment2 and logging.ERROR"""
    logger = logging.getLogger('assignment2')
    logger.setLevel(logging.ERROR)

    lines = contents.split('\n')[1:]
    data = {}
    for idx in range(0, len(lines)):
        line = lines[idx]
        if line.strip() == '':
            continue

        Date, name, id = '', '', ''
        isValidDate = True

        try:

            lineData = line.split(',')
            if len(lineData) < 3:
                raise ValueError
            id, name, birthday = lineData[0], lineData[1], lineData[2]

            birthdayData = birthday.split('/')
            if len(birthdayData) < 3:
                raise ValueError

            day, month, year = birthdayData[0], birthdayData[1], birthdayData[2]
            Date = datetime.date(int(year.strip()), int(month.strip()), int(day.strip()))

        except ValueError:
            isValidDate = False

        if isValidDate:
            data[id] = (name, Date)
        else:
            logger.error("Error processing line #" + str(idx + 2) + " for ID #" + str(id))
    return data


def displayPerson(id, personData):
    """Display persons data"""

    id = str(id)
    if id not in personData:
        print("No user found with that id")
    else:
        name, birthday = personData[id]

        print("Person #" + str(id) + " is " + name + " with birthday of " + str(birthday))


def main():
    """Calls on all three functions and stores data"""
    # test URL:
    # http://www.sharecsv.com/dl/666e78f47117702a49dd606d472a56cc/birthdays100.csv
    if len(sys.argv) == 2:

        try:
            csvData = downloadData(str(sys.argv[1]))
            logging.basicConfig(filename='errors.log', level=logging.ERROR)
            personData = processData(csvData)

            while True:
                id = input("Enter a ID: ")
                if id > 0:
                    displayPerson(id, personData)
                else:
                    break

        except Exception as e:
            print("Invalid Exception")


main()
