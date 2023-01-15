import validators

from selenium import webdriver

import sys
import os
import googlesearch
import googlesearch.googlesearch as gg
from googlesearch.googlesearch import GoogleSearch
from googlesearch import search
# from googlesearch import Search

import requests
from bs4 import BeautifulSoup

import pyperclip as pc

import google

def mysearch(request : str):
    print("Search for \'{}\'".format(request))
    GS = GoogleSearch()
    response = GS.search(request)
    # print("Response object:", response)
    # print(dir(response))

    print("Response results:", response.results)
    print("Total number of results:", response.total)
    for result in response.results:
        
        print("Title:", result.title)
        print("URL:", result.url)
        print("Content:", result.getText())


def devTest():

    if len(sys.argv) == 1:  # Only the file name.
        query = "python"
    else:
        query = " ".join(sys.argv[1:])

    search = GoogleSearch()

    num_results = 10
    print ("Fetching first " + str(num_results) + " results for \"" + query + "\"...")

    response = search.search(query, num_results, prefetch_pages=True)
    print ("TOTAL: " + str(response.total) + " RESULTS")
    print("__ results:", response.results)

    for count, result in enumerate(response.results):
        print("RESULT #" + str (count+1) + ":")
        print(
            (
                result._SearchResult__text.strip()
                    if result._SearchResult__text is not None 
                    else "[None]"
            ) + "\n\n"
        )

def search_error(statement):
    print("Googling.......")
    google_search = requests.get("https://www.google.com/search?q=" + statement)
    
    soup = BeautifulSoup(google_search.content, 'html.parser')
    
    print(dir(soup))## returning google cookie ask
    print(type(soup))
    pc.copy(str(soup))

    search_result = soup.find_all("a", {"data-uch" : 1}) # soup.select(".r a")

    print("res:", search_result)
    
    print("")
    print(type(search_result))
    print(dir(search_result))


    for link in search_result:
        print(link)

if __name__ == "__main__":
    # mysearch("Auto")
    # help(search)

    # for i in search(query= "car", tld="co.in", lang="de", num=2, stop=10, pause=2):
    #     print(i)


    # print(dir(GoogleSearch()))

    # help(gg)

    # results = Search("Car")
    # print(results.results)

    # mysearch("car")

    statement = "car" #input("Enter the Statement of Error to find it on Stack Overflow: ")
    search_error(statement)
