class MITClass:
    def __init__(self, number:str, prereqs:list[str], postreqs:list[str]):
        self.number = number
        self.prereqs = prereqs.copy()
        self.postreqs = postreqs.copy()

    def display(self):
        print(f"Class: {self.number}\nprereqs: {self.prereqs}\npostreqs:{self.postreqs}\n")

    def get_number(self)->str:
        return self.number
    
    def get_prereqs(self)->list[str]:
        return self.prereqs.copy()

    def get_postreqs(self)->list[str]:
        return self.postreqs.copy()
    def add_prereq(self, prereq:str)->None:
        self.prereqs.append(prereq)
    def add_postreq(self, postreq:str)->None:
        self.postreqs.append(postreq)