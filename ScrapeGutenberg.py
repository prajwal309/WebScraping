#Author: Prajwal Niraula
#Program to scrape off data
#Python version 3.8
#External library beautifulsoup4 -- version 4.9.3

import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import json
import os


def DownloadTxtGutenberg(BookNumber):
  URL = "https://www.gutenberg.org/cache/epub/%d/pg%d.txt" %(BookNumber, BookNumber)
  r = requests.get(URL)
  if not(r.status_code==404):
     html_doc = r.text
     SaveName = "data/"+str(BookNumber).zfill(10)+".txt"
     with open(SaveName, 'w') as currentFile:
         currentFile.write(html_doc)

  pass


def ExploreByBookShelf(Shelf=range(1,200)):
  '''
  This function scrapes gutenberg project by
  the book shelf category
  '''

  AllTitle = []
  AllWriter = []
  AllDownloadCount = []
  SavedLocation = []
  AllGutenbergBookNumber = []


  #Make a local directory
  if not(os.path.exists("database")):
      os.system("mkdir database")


  #Now save to json file
  if not(os.path.exists("database/GutenbergDatabase.json")):
      CurrentFile =  open('database/GutenbergDatabase.json', 'w')
      CurrentFile.write("[\n")
      CurrentFile.close()
  else:
      #remove the last ]
      with open('database/GutenbergDatabase.json', 'rb+') as filehandle:
          filehandle.seek(-1, os.SEEK_END)
          filehandle.truncate()
          #filehandle.write("\n")

      with open('database/GutenbergDatabase.json', 'a') as filehandle:
          filehandle.write(",\n")

  for i in Shelf:
    URL =  "https://www.gutenberg.org/ebooks/bookshelf/"+str(i)
    r = requests.get(URL)

    print("The URL is given by:", URL)
    #Only if the page exists
    if not(r.status_code==404):
        html_doc = r.text
        soup = BeautifulSoup(html_doc, 'html.parser')



        for link in soup.find_all('a'):
            SubLink = str(link.get('href'))
            try:
                BookNumber = int(SubLink.split("/")[2])
                AllGutenbergBookNumber.append(BookNumber)
            except:
                pass


        for link in soup.find_all('span'):

            StrLink = str(link)
            LinkContent = link.contents

            if "\n" in StrLink or "Sort Alphabetically" in StrLink or "Sort by Release Date" in StrLink:
                continue

            if "subtitle" in StrLink:
                AllWriter.append(link.contents[0])
            elif "title" in StrLink:
                AllTitle.append(link.contents[0])
            elif "extra" in StrLink:
                #Just save the number -- specific to python3
                AllDownloadCount.append(int(''.join(filter(str.isdigit, link.contents[0]))))
            else:
                pass






        for writer, title, download, number in zip(AllWriter, AllTitle,AllDownloadCount, AllGutenbergBookNumber):
            Entry = {

                    'Writer':writer,
                    'title':title,
                    'Download':download,
                    'Gutenberg Number':number
            }

            #Save the data to the gutenberg project
            with open('database/GutenbergDatabase.json', 'a') as json_file:
                FileEntry = json.dumps(Entry, indent=4)
                json_file.write(FileEntry+",\n")


        #remove the last comma from file
        with open('database/GutenbergDatabase.json', 'rb+') as filehandle:
            filehandle.seek(-2, os.SEEK_END)
            filehandle.truncate()

        CurrentFile =  open('database/GutenbergDatabase.json', 'a')
        CurrentFile.write("]")
        CurrentFile.close()
        #Now we will do this



def SerialScraper():
    '''
    Function to serially download all the books from Gutenberg
    '''

    #Save in the local directory -- data
    if not(os.path.exists("data")):
        os.system("mkdir data")
    #go serially from 1 to 100000
    for i in range(100000):
        #Construct URL
        URL = "https://www.gutenberg.org/cache/epub/"+str(i)+"/pg"+str(i)+".txt"
        r = requests.get(URL)

        #Only if the page exists
        if not(r.status_code==404):
            CurrentText = r.text
            #Now saving to the
            SaveName = "data/"+str(i).zfill(10)+".txt"
            with open(SaveName, 'w') as json_file:
                json.dumps(CurrentText, json_file)


def DownloadFromDatabase():
    '''
    Now plot the data from the database
    '''

    f = open('database/GutenbergDatabase.json', 'r')
    Content = json.load(f)
    for Entry in Content:
        print("Now Downloading ", Entry['title'])
        DownloadTxtGutenberg(Entry['Gutenberg Number'])



os.system("rm database/*")

#Scrape a selected number of books
ExploreByBookShelf([30])
ExploreByBookShelf([68])

#input("Now we download the book from the database")
#Download the books from database/GutenbergDatabase.json
DownloadFromDatabase()
