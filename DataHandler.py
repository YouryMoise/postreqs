import os
from MITClass import MITClass
import pickle


class DataHandler:
    def __init__(self):
        self.course_dict:dict[str, MITClass] = {}
        #maps course numbers to MITClass objects

    def display_classes(self):
        for course in self.course_dict.values():
            course.display()
    
    def get_course_dict(self):
        # don't want to do deep copy here
        # need to be able to edit the actual classes?
        return self.course_dict

    def add_course(self, course:MITClass)->None:
        number = course.get_number()
        self.course_dict[number] = course

    def course_exists(self, name:str)->bool:
        return name in self.course_dict.keys()

    def get_course(self, name:str)->MITClass:
        return self.course_dict[name]

    def save_pkl_file(self, filename:str, data)->None:
        with open(filename, 'wb') as file:
            pickle.dump(data, file)

    def save_txt_file(self, filename:str, data:str)->None:
        file = open(filename, "w")
        file.write(data)

    def load_pkl_file(self, filename:str):
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        return data
    def load_txt_file(self, filename:str)->str:
        file = open(filename, "r")
        return file.read()

    def txt_file_exists(self, filename:str)->bool:
        return os.path.exists(filename)
