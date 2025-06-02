from MITClass import MITClass
from DataHandler import DataHandler

class Searcher:
    def __init__(self, desired_class:str, all_classes:list[MITClass], dataHandler:DataHandler):
        self.dataHandler = dataHandler
        self.all_classes = all_classes
        self.desired_class:MITClass = self.dataHandler.get_course(desired_class)

    def get_postreqs(self)->list[str]:
        queue:list[MITClass] = [self.desired_class]
        all_postreqs:list[str] = []
        visited = set()
        while queue:
            # print(queue)
            current_class = queue.pop(0)
            for postreq in current_class.postreqs:
                if postreq in visited:
                    continue
                all_postreqs.append(postreq)
                queue.append(self.dataHandler.get_course(postreq))
                visited.add(postreq)
        return all_postreqs
