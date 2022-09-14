'''
Assignment #3
1. Add / modify code ONLY between the marked areas (i.e. "Place code below"). Do not modify or add code elsewhere.
2. Run the associated test harness for a basic check on completeness. A successful run of the test cases does not guarantee accuracy or fulfillment of the requirements. Please do not submit your work if test cases fail.
3. To run unit tests simply use the below command after filling in all of the code:
    python 03_assignment.py
  
4. Unless explicitly stated, please do not import any additional libraries but feel free to use built-in Python packages
5. Submissions must be a Python file and not a notebook file (i.e *.ipynb)
6. Do not use global variables
7. Make sure your work is committed to your master branch in Github
8. Use the test cases to infer requirements wherever feasible
'''
import csv, json, math, pandas as pd, requests, unittest, uuid

# ------ Create your classes here \/ \/ \/ ------

# Box class declaration below here

class Box:
    '''
    A class used to represent a box with integer dimensions length and width
    '''
   
    def __init__(self, length, width):
        '''
        Initializes the Box with dimensions length and width


        Parameters
        ----------
        length : int
            the length of the Box.
        width : int
            the width of the Box.

        Raises
        ------
        TypeError
            length and width must be integers.
        
        ValueError
            length and width must be positive.

        '''

        if isinstance(length, int):
            if length > 0:
                self.__length = length
            else:
                raise ValueError("length must be positive")
        else:
            raise TypeError("length must be an integer")

        if isinstance(width, int):
            if width > 0:
                self.__width = width
            else:
                raise ValueError("width must be positive")
        else:
            raise TypeError("width must be an integer")
        
    def __eq__(self, other):
        '''
        tests that two Box objects have the same dimensions


        Parameters
        ----------
        other : Box
            Box object to test equality

        Returns
        -------
        bool
            a boolean value indicating that the two Box objects have the same dimensions.

        '''
        
        return isinstance(other, Box) and (self.__length == other.get_length()) and (self.__width == other.get_width())
    
    def __str__(self):
        '''
        string conversion

        
        Returns
        -------
        str
            a string representation of the Box.

        '''

        return str('{length} x {width}'.format(length = self.__length, width = self.__width))
    
    def combine(self, other):
        '''
        Creates a Box by adding the dimensions of two Box objects


        Parameters
        ----------
        other : Box
            a Box to add dimensions

        Returns
        -------
        Box
            a Box with dimensions created by adding the length and width from the original two Box objects.

        '''

        if isinstance(other, Box):
            return Box(self.__length + other.get_length(), self.__width + other.get_width())
        else:
            raise TypeError("other must be of type Box")
    
    def double(self):
        '''
        Doubles the dimensions of the Box


        Returns
        -------
        Box
            A Box with double the length and width as the original Box.

        '''

        return Box(2 * self.__length, 2 * self.__width)
    
    def get_area(self):
        '''
        Calculates the area of the Box
        

        Returns
        -------
        int
            the area of the Box.

        '''

        return self.__length * self.__width
    
    def get_dim(self):
        '''
        the dimensions (length,width) of the Box
        

        Returns
        -------
        int
            length of the Box object.
        int
            width of the Box object.

        '''
        
        return self.__length, self.__width
    
    def get_hypot(self):
        '''
        Calculates the length of the diagonal of the Box

        
        Returns
        -------
        float
            the length of the diagonal of the Box.

        '''
        
        return (self.__length ** 2 + self.__width ** 2) ** .5
    
    def get_length(self):
        '''
        length of the Box
        

        Returns
        -------
        int
            the length of the Box.

        '''

        return self.__length
    
    def get_perimeter(self):
        '''
        Calculates the perimiter of the Box
        

        Returns
        -------
        int
            the perimeter of the Box.

        '''
        
        return 2 * (self.__length + self.__width)
    
    def get_width(self):
        '''
        width of the Box
        

        Returns
        -------
        int
            the width of the Box.

        '''
        
        return self.__width
    
    def invert(self):
        '''
        Creates a Box by swapping the length and width dimensions of the Box
        

        Returns
        -------
        Box
            a Box with swapped dimensions.

        '''
        
        return Box(length = self.__width, width = self.__length)

    def print_dim(self):
        '''
        prints a string representation of the dimensions of the Box

        '''

        print(self)
    
    def render(self):
        '''
        prints a representation of the Box
        
        '''
        
        for i in range(self.__length):
            print('*' * self.__width)


# MangoDB class declaration below here

class MangoDB:
    '''
    A class that implements a dictionary of dictionaries
    '''

    def __init__(self):
        '''
        Initializes the MangoDB class with a default collection


        '''

        self.wipe()
        
    def add_collection(self, collection_name):
        '''
        Adds collection to database
        

        Parameters
        ----------
        collection_name : str
            name of a new collection.

        Raises
        ------
        ValueError
            collection_name must not be an existing collection in the database.

        '''

        if collection_name not in self.get_collection_names():
            self.__dict[collection_name] = {}
        else:
            raise ValueError("Collection already exists: {}".format(collection_name))

    def display_all_collections(self):
        '''
        prints all collections in the database


        '''

        for collection_name in self.get_collection_names():
            self.display_collection(collection_name)

    def display_collection(self, collection_name):
        '''
        prints a collection in the database.

        Parameters
        ----------
        collection_name : str
            collection_name must exist in the database.

        Raises
        ------
        ValueError
            collection_name is not an existing collection in the database.

        '''

        if collection_name in self.get_collection_names():
            print("collection: {}".format(collection_name))
            for key, value in self.__dict[collection_name].items():
                print("    {}: {}".format(key, value))
        else:
            raise ValueError("Collection NOT found: {}".format(collection_name))
        
    def get_collection_names(self):
        '''
        a list of collection names in the database


        Returns
        -------
        list
            list of collections in the database.

        '''

        return self.__dict.keys()
    
    def get_collection_size(self, collection_name):
        '''
        the number of elements in the collection


        Parameters
        ----------
        collection_name : str
            collection to search.

        Raises
        ------
        ValueError
            collection_name is not an existing collection in the database.

        Returns
        -------
        int
            number of elements in the collection.

        '''

        if collection_name in self.get_collection_names():
            return len(self.__dict[collection_name].keys())
        else:
            raise ValueError("Collection NOT found: {}".format(collection_name))

    def list_collections(self):
        '''
        prints a list of the collections in the database


        '''
        for collection_name in self.get_collection_names():
            print(collection_name)
            
    def remove_collection(self, collection_name):
        '''
        removes a collection from the database
        

        Parameters
        ----------
        collection_name : str
            the collection to be removed from the database.

        Raises
        ------
        ValueError
            Cannot remove the default collection.
            collection_name is not an existing collection in the database.

        '''
        if collection_name == 'default':
            raise ValueError("Cannot remove default Collection")
        elif collection_name in self.get_collection_names():
            del self.__dict[collection_name]
        else:
            raise ValueError("Collection NOT found: {}".format(collection_name))

    def to_json(self, collection_name):
        '''
        json representation of a collection in the database


        Parameters
        ----------
        collection_name : str
            collection to convert to a json string.

        Raises
        ------
        ValueError
            collection_name is not an existing collection in the database.

        Returns
        -------
        str
            json representation of a collection in the database.

        '''
        if collection_name in self.get_collection_names():
            return json.dumps(self.__dict[collection_name])
        else:
            raise ValueError("Collection NOT found: {}".format(collection_name))

    def update_collection(self, collection_name, dict_items):
        '''
        updates an existing collection in the database


        Parameters
        ----------
        collection_name : str
            collection to update.
        dict_items : dict
            dictionary items to update.

        Raises
        ------
        ValueError
            collection_name is not an existing collection in the database.

        '''
        if collection_name == 'default':
            raise ValueError("Cannot update default collection")
        elif collection_name in self.get_collection_names():
            self.__dict[collection_name].update(dict_items)
        else:
            raise ValueError("Collection NOT found: {}".format(collection_name))

    def wipe(self):
        '''
        Cleans the database creating the default collection


        '''
        self.__dict = {
            'default': {
                'version':'1.0',
                'db':'mangodb',
                'uuid': str(uuid.uuid4())
            }
        }
        
# ------ Create your classes here /\ /\ /\ ------





def exercise01():

    '''
        Create an immutable class Box that has private attributes length and width that takes values for length and width
        upon construction (instantiation via the constructor). Make sure to use Python 3 semantics. Make sure the length
        and width attributes are private and accessible only via getters. Immutable here means that any change to its internal
        state results in a new Box being returned. This means there are no setter methods and any time the internal state
        (length or width) is modified, a new Box is created containing the modified values. 
        This is applicable to combine(), invert() and double()
        
        Good article on immutability: https://towardsdatascience.com/https-towardsdatascience-com-python-basics-mutable-vs-immutable-objects-829a0cb1530a
        
        In addition, create:
        - A method called render() that prints out to the screen a box made with asterisks of length and width dimensions
        - A method called invert() that switches length and width with each other
        - Methods get_area() and get_perimeter() that return appropriate geometric calculations
        - A method called double() that doubles the size of the box. Hint: Pay attention to return value here
        - Implement __eq__ so that two boxes can be compared using ==. Two boxes are equal if their respective lengths and widths are identical.
        - A method print_dim that prints to screen the length and width details of the box
        - A method get_dim that returns a tuple containing the length and width of the box
        - A method combine() that takes another box as an argument and increases the length and width by the dimensions of the box passed in
        - A method get_hypot() that finds the length of the diagonal that cuts throught the middle
        In the function exercise01():
        - Instantiate 3 boxes of dimensions 5,10 , 3,4 and 5,10 and assign to variables box1, box2 and box3 respectively 
        - Print dimension info for each using print_dim()
        - Evaluate if box1 == box2, and also evaluate if box1 == box3, print True or False to the screen accordingly
        - Combine box3 into box1 (i.e. box1.combine()) creating box4
        - Double the size of box2 creating box5
        - Combine box5 into box4 creating box6
        - Using a for loop, iterate through and print the tuple received from calling box2's get_dim()
        - Find the size of the diagonal of box2
'''

    # ------ Place code below here \/ \/ \/ ------

    # Instantiate 3 boxes of dimensions 5,10 , 3,4 and 5,10 and assign to variables box1, box2 and box3 respectively 
    box1 = Box(5,10)
    box2 = Box(3,4)
    box3 = Box(5,10)
    
    # Print dimension info for each using print_dim()
    box1.print_dim()
    box2.print_dim()
    box3.print_dim()
    
    # Evaluate if box1 == box2, and also evaluate if box1 == box3, print True or False to the screen accordingly
    print(box1 == box2)
    print(box1 == box3)
    
    # Combine box3 into box1 (i.e. box1.combine()) creating box4
    box4 = box1.combine(box3)
    
    # Double the size of box2 creating box5
    box5 = box2.double()
    
    # Combine box5 into box4 creating box6
    box6 = box4.combine(box5)
    
    # Using a for loop, iterate through and print the tuple received from calling box2's get_dim()
    for x in box2.get_dim():
        print(x)

    # Find the size of the diagonal of box2
    print(box2.get_hypot())
    
    return box1, box2, box3, box4, box5, box6

    # ------ Place code above here /\ /\ /\ ------


def exercise02():
    '''
    Create a class called MangoDB. The MangoDB class wraps a dictionary of dictionaries. At the the root level, each key/value will be called a 
    collection, similar to the terminology used by MongoDB, an inferior version of MangoDB ;) A collection is a series of 2nd level key/value paries. 
    The root value key is the name of the collection and the value is another dictionary containing arbitrary data for that collection.
    For example:
        {
            'default': {
            'version':1.0,
            'db':'mangodb',
            'uuid':'0fd7575d-d331-41b7-9598-33d6c9a1eae3'
            },
        {
            'temperatures': {
                1: 50,
                2: 100,
                3: 120
            }
        }
    
    The above is a representation of a dictionary of dictionaries. Default and temperatures are dictionaries or collections. The default collection 
    has a series of key/value pairs that make up the collection. The MangoDB class should create only the default collection, as shown, on 
    instantiation including a randomly generated uuid using the uuid4() method and have the following methods:
        - display_all_collections() which iterates through every collection and prints to screen each collection names and the collection's 
        content underneath and may look something like:
            collection: default
                version 1.0
                db mangodb
                uuid 739bd6e8-c458-402d-9f2b-7012594cd741
            collection: temperatures
                1 50
                2 100 
        - add_collection(collection_name) allows the caller to add a new collection by providing a name. The collection will be empty but will have a name.
        - update_collection(collection_name,updates) allows the caller to insert new items into a collection i.e. 
                db = MangoDB()
                db.add_collection('temperatures')
                db.update_collection('temperatures',{1:50,2:100})
        - remove_collection() allows caller to delete a specific collection by name and its associated data
        - list_collections() displays a list of all the collections
        - get_collection_size(collection_name) finds the number of key/value pairs in a given collection
        - to_json(collection_name) that converts the collection to a JSON string
        - wipe() that cleans out the db and resets it with just a default collection
        - get_collection_names() that returns a list of collection names
        Make sure to never expose the underlying data structures
        For exercise02(), perform the following:
        - Create an instance of MangoDB
        - Add a collection called testscores
        - Take the test_scores list and insert it into the testscores collection, providing a sequential key i.e 1,2,3...
        - Display the size of the testscores collection
        - Display a list of collections
        - Display the db's UUID
        - Wipe the database clean
        - Display the db's UUID again, confirming it has changed
    '''

    test_scores = [99,89,88,75,66,92,75,94,88,87,88,68,52]

    # ------ Place code below here \/ \/ \/ ------

    # Create an instance of MangoDB
    db = MangoDB()

    # Add a collection called testscores
    db.add_collection('testscores')

    # Take the test_scores list and insert it into the testscores collection, providing a sequential key i.e 1,2,3...
    for i in range(len(test_scores)):
        db.update_collection('testscores', {i+1: test_scores[i]})

    # Display the size of the testscores collection
    print("size of testscores collection: {}".format(db.get_collection_size('testscores')))
    
    # Display a list of collections
    print("list of collections:")
    db.list_collections()
    
    # Display the db's UUID
    
    print("uuid: {}".format(json.loads(db.to_json('default'))["uuid"]))

    # Wipe the database clean
    print("wipe database")
    db.wipe()
    
    # Display the db's UUID again, confirming it has changed
    print("uuid: {}".format(json.loads(db.to_json('default'))["uuid"]))
    
    # ------ Place code above here /\ /\ /\ ------


def exercise03():
    '''
    1. Avocado toast is expensive but enormously yummy. What's going on with avocado prices? Read about avocado prices (https://www.kaggle.com/neuromusic/avocado-prices/home)
    2. Load the avocado.csv file included in this Github repository and display every line to the screen
    3. Open the file name under csv_file
    4. The reader should be named reader
    5. Use only the imported csv library to read and print out the avacodo file
    
    '''

    # ------ Place code below here \/ \/ \/ ------

    with open('avocado.csv') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            print(row)

    # ------ Place code above here /\ /\ /\ ------

class TestAssignment3(unittest.TestCase):
    def test_exercise01(self):
        print('Testing exercise 1')
        b1, b2, b3, b4, b5, b6 = exercise01()
        self.assertEqual(b1.get_length(),5)
        self.assertEqual(b1.get_width(),10)
        self.assertEqual(b2.get_length(),3)
        self.assertEqual(b2.get_width(),4)
        self.assertEqual(b3.get_length(),5)
        self.assertEqual(b3.get_width(),10)            
        self.assertEqual(b4.get_length(),10)
        self.assertEqual(b4.get_width(),20)        
        self.assertEqual(b5.get_length(),6)
        self.assertEqual(b5.get_width(),8)
        self.assertEqual(b6.get_length(),16)
        self.assertEqual(b6.get_width(),28)
        self.assertTrue(b1==Box(5,10))
        self.assertEqual(b2.get_hypot(),5.0)
        self.assertEqual(b1.double().get_length(),10)
        self.assertEqual(b1.double().get_width(),20)
        self.assertTrue(3 in b2.get_dim())
        self.assertTrue(4 in b2.get_dim())
        self.assertTrue(6 in b2.double().get_dim())
        self.assertTrue(8 in b2.double().get_dim())
        self.assertTrue(b2.combine(Box(1,1))==Box(4,5))
        self.assertTrue(b1.invert()==Box(10,5))

    def test_exercise02(self):
        print('Testing exercise 2')
        exercise02()
        db = MangoDB()
        self.assertEqual(db.get_collection_size('default'),3)
        self.assertEqual(len(db.get_collection_names()),1)
        self.assertTrue('default' in db.get_collection_names() )
        db.add_collection('temperatures')
        self.assertTrue('temperatures' in db.get_collection_names() )
        self.assertEqual(len(db.get_collection_names()),2)
        db.update_collection('temperatures',{1:50})
        db.update_collection('temperatures',{2:100})
        self.assertEqual(db.get_collection_size('temperatures'),2)
        self.assertTrue(type(db.to_json('temperatures')) is str)
        self.assertEqual(db.to_json('temperatures'),'{"1": 50, "2": 100}')
        db.wipe()
        self.assertEqual(db.get_collection_size('default'),3)
        self.assertEqual(len(db.get_collection_names()),1)
        
    def test_exercise03(self):
        print('Exercise 3 not tested')
        exercise03()
     

if __name__ == '__main__':
    unittest.main()
