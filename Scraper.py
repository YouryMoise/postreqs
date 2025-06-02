from DataHandler import DataHandler
from MITClass import MITClass
import requests
import os
# should directly use datahandler to save/load everything
class Scraper:
    def __init__(self, dataHandler:DataHandler):
        self.base_url = "https://student.mit.edu/catalog/m"
        self.url_extensions:list[str] = self._create_extensions()
        self.dataHandler = dataHandler
        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.txt_folder_name = "responses"

    def _create_extensions(self)->list[str]:
        extensions:list[str] = [str(i) for i in range(1, 13)] +\
             [str(i) for i in range(14, 19)] + ["20"]+ \
            ["21A", "21W", "21G", "21H", "21L", "21M", "21T"]
        # add in the other courses later
        return extensions

    # should only do this for urls that do not already
    # have txt file named after them
    # for the ones that don't, do the logic and add their classes
    # to the array from the pkl file
    # so if all are already included it just returns the original array
    def get_all_classes(self)->list[MITClass]:
        # fetch all pages
        # parse all pages to save into datahandler
        # save them into pkl file
        # return the class dict (let it be mutable for now)

        # self._fetch_all_pages()
        
        # maybe use iterator here, not for now though
        course_files = os.listdir(self.txt_folder_name)
        for course in course_files:
            current_html_page = self.dataHandler.load_txt_file(self.txt_folder_name + "/"+course)
            self.parse_page(current_html_page)
            # self.dataHandler.display_classes()
            # print(f"Done with {course}")
        course_dict = self.dataHandler.get_course_dict()
        self.dataHandler.save_pkl_file("course_dict.pkl", course_dict)
        # self.dataHandler.display_classes()
        # print(files)


    def _fetch_all_pages(self)->None:
        """
        Store all HTML content in txt files in /responses folder
        """
        for extension in self.url_extensions:
            for letter in self.alphabet:
                full_extension = extension + letter
                filename = self.txt_folder_name + "/" + full_extension + ".txt"
                if self.dataHandler.txt_file_exists(filename):
                    continue
                current_url = self.base_url + full_extension + ".html"
                response = requests.get(current_url)
                if response.status_code != 200:
                    break #assuming we have exceeded letters
                self.dataHandler.save_txt_file(filename, response.text)
    
    def split_page(self, html_page:str):
        """
        Takes raw html text and returns a list of html blocks
            with class info
        """
        # should go from where it says name=...
        # to the last <--end comment
        # YOURY - need to handle the 21Gc special case
        if "<a name=" not in html_page:
            return []
        start_index = html_page.index("<a name=")
        end_index = html_page.rfind("<!--end-->") + len("<!--end-->")
        relevant_text = html_page[start_index:end_index] #shouldn't need +1
        return relevant_text.split("<!--end-->")


    def parse_single_class(self, html_block:str)->None:
        # just need number and prereqs
        if "name=\"" not in html_block:
            return
        number_start_index = html_block.index("name=\"") + len("name=\"")
        number_end_index = number_start_index
        while html_block[number_end_index] != "\"":
            number_end_index += 1
        number = html_block[number_start_index:number_end_index]
        # print(f"handling {number}")
        # if number == "18.02":
        print(f"processing {number}")
        # for prereqs, most are like
        #>number</a>
        # should only look after the "prereq" index
        # should only add if it is numeric
        #   not just numeric cause also have things like 16.C20
        # maybe just look for dot
        # if you find one that is not numeric, look at "title"
        prereq_index = html_block.index("Prereq: ") if "Prereq: " in html_block else len(html_block)-1 
        # also captures coreqs
        prereq_info = html_block[prereq_index:]
        prereqs = []
        while "</a>" in prereq_info and "Prereq: None" not in prereq_info and "Prereq: Permission" not in prereq_info:
            anchor_close_index = prereq_info.index("</a>")
            previous_close_index = anchor_close_index
            while prereq_info[previous_close_index] != ">":
                previous_close_index-=1
            current_prereq = prereq_info[previous_close_index+1:anchor_close_index]
            if '.' not in current_prereq:
                if "title=\"" in prereq_info:
                    title_index = prereq_info.index("title=\"")+len("title=\"")
                    end_title_index = title_index
                    while prereq_info[end_title_index] != "\"":
                        end_title_index+=1
                    class_options = prereq_info[title_index:end_title_index]
                    for course in class_options.split(', '):
                        if "." not in course:
                            continue
                        prereqs.append(course)

            else:
                prereqs.append(current_prereq)
            prereq_info = prereq_info[anchor_close_index+1:]
        # if number == "18.02":
        #     print(f"18.02: {prereqs=}")
            
        # this class may have already been added when it was found
        # to be a prereq for another class
        # so have to get it from dataHandler
        # current_class:MITClass = None
        # if number == "18.02":
        #     if self.dataHandler.course_exists("18.02"):
        #         print(f"{self.dataHandler.get_course("18.02").display()} before")
        if self.dataHandler.course_exists(number):
            current_class = self.dataHandler.get_course(number)
            for prereq in prereqs:
                current_class.add_prereq(prereq)
        else:
            current_class:MITClass = MITClass(number, prereqs, [])
        self.dataHandler.add_course(current_class)
        # if number == "18.02":
        #     if self.dataHandler.course_exists("18.02"):
        #         print(f"{self.dataHandler.get_course("18.02").display()} after")
            

        # for every prereq, also need to create a class for it and add this
        # as a postreq
        # if "18.02" in prereqs:
        #     if self.dataHandler.course_exists("18.02"):
        #         print(f"{self.dataHandler.get_course("18.02").display()} before")
            
        for prereq in prereqs:
            # prereq_object:MITClass = None
            if not self.dataHandler.course_exists(prereq):
                prereq_object = MITClass(prereq, [], [number])
            else:
                prereq_object = self.dataHandler.get_course(prereq)
                prereq_object.add_postreq(number)
            self.dataHandler.add_course(prereq_object)
        # if "18.02" in prereqs:
        #     if self.dataHandler.course_exists("18.02"):
        #         print(f"{self.dataHandler.get_course("18.02").display()} after")
        
        # print(self.dataHandler.course_dict)
        # self.dataHandler.display_classes()
        # return prereqs

        #for GIRs like calc, look for "title=" and split that by ','


    def parse_page(self, html_page:str):
        """
        Takes raw html content and adds all classes to dataHandler
        """
        blocks = self.split_page(html_page)
        for block in blocks:
            self.parse_single_class(block)
        
        # self.dataHandler.display_classes()
        
                # maybe sleep a bit to prevent overloading

# print(response.status_code) # Print the HTTP status code
# print(len(response.text))

    