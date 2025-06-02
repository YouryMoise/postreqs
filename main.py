# quick test to get http calls working
import requests

# url = "https://student.mit.edu/catalog/m6a.html"
# response = requests.get(url)

# print(response.status_code) # Print the HTTP status code
# print(len(response.text)) 

from Scraper import Scraper
from Searcher import Searcher
from MITClass import MITClass
from DataHandler import DataHandler
import os
import pickle

# desired_class:str = input("Enter official course number")
dataHandler = DataHandler()
scraper = Scraper(dataHandler)
scraper.get_all_classes()
data = dataHandler.load_pkl_file("course_dict.pkl")
searcher = Searcher("18.06", data, dataHandler)
result = searcher.get_postreqs()
print(result)

# with open("course_dict.pkl", "rb") as file:
#     data = pickle.load(file)

# data["6.1910"].display()