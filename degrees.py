import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass

#class declaration
class Node():
    def __init__(self, state, parent):#the action attribute is not included, no need to determine cost here
        self.state = state
        self.parent = parent

    def __repr__(self):
        return f"(State: {self.state}, Parent: {self.parent})"
    
#define class of frontier, it containts used frontier and function that checks if the node has been used    
class frontier():
    def __init__(self):
        self.frontier = []
        self.usedSpace=set()
        self.parentSpace=[]
        self.Tracking=[]
        self.nouran = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state): 
        return any(node.state == state for node in self.frontier)

    def Used_node(self, id):
        return id in self.usedSpace

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
    def path(self, searchedfor):
        #print(f"\n Now looking at the {searchedfor} node\n")
        
        while True: #the goal of this loop is to retrace back all the nodes to get the path after having found the target node
            if searchedfor.parent=="Grandparent": #node is root, return the entire space
                #print("Reached a root node, it is parent is Grandparent, end of path function\n")
                #print(f"searched for is {searchedfor}\n")
                
                for x in self.Tracking:
                    self.nouran.append(x.state)
                self.nouran.reverse()
                return self.nouran
            else:
                for node in self.parentSpace:
                    if node.state == searchedfor.parent:
                        #print(f"\n Found parent it is {node}\n")
                        self.Tracking.append(searchedfor)
                        #print(f"nouran is now {self.nouran} and tracking is {self.Tracking}\n")            
                        return self.path(node)

Space = frontier() #this is the instance of the class frontier, this the actual frontier we will use

def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)
    print(f"The obtained path result was {path}")

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    #TODO

    #APPROACH

    first_instance = list(neighbors_for_person(source))
    for x in first_instance:
        if x[1]==source:
            Space.frontier.append(Node(x,"Grandparent"))
            break
    #print(f"The first instance is\n {first_instance}")
    #print(f"The root node is included in the froniter, the space is now \n {Space.frontier}") #left off debugging here
    #print(f"our target is {target}")
    #start loop

    while True:  #recursive function would start here

        #check if frontier is empty if so, it means there is no path
        if not len(Space.frontier):
            #print(f"Space frontier is empty, it is value is \n{Space.frontier}")
            return None

        #Pick first node, check if it is target node
        if Space.frontier[0].state[1]==target:
            #print(f"found statement, target is {target} and the value of that things' state is {Space.frontier[0]}")
            #in this case, you have found the proper node, you have to trace back and extract its parents
            #print(F"\nYou have found the proper node, it is the one in question currenly, Your node is {Space.frontier[0]} and target is {target}")
            
            return Space.path(Space.frontier[0]) 
            
        else:
            Space.usedSpace.add(Space.frontier[0].state[1]) #if not add it to used space
            Space.parentSpace.append(Space.frontier[0])
            #print(f"\n\nNEW ITERATION\n\n")
            #print(f"Neither of the ending condistions is satisfied, we added node {Space.frontier[0]} to used space, \nvalue of used space:\n{Space.usedSpace}\n")
            #expand it, add those nodes to frotier, for each one check if it is already in the used space, if it is don't add it
            lst = list(neighbors_for_person(Space.frontier[0].state[1]))
            #print("we exapnded the node")
            for x in lst:
                #check if node is in used space, if it is it won't be included
                if Space.Used_node(x[1]):
                    #print(f"The node {x} is in used space")
                    continue
                Space.frontier.append(Node(x,Space.frontier[0].state))#node is added to frontier
                Space.usedSpace.add(x[1])
            Space.frontier.remove(Space.frontier[0]) #removing the first node #Space.remove(Space.frontier[0])
            #print(f"\nThe value of used space is \n{Space.usedSpace}\n")
            #print(f"we removed the first node, now frontier is \n {Space.frontier}")
            #if recursion is used recall function under this line
            
        
        

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
