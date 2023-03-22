#!/usr/bin/python3
"""
Holds tests to the console
"""


HBNBCommand = __import__('console').HBNBCommand
from models import storage
import unittest
from unittest.mock import patch
from io import StringIO
from random import randint


class TestConsole(unittest.TestCase):
    """
    Contains test cases for the console
    """
    
    __cache = storage.all()
    _models = ['Amenity', 'BaseModel', 'City', 
                'Place', 'Review', 'State','User']
    __cls, __id = "", ""
    def setUp(self):
        storage.reload()

    def test_create(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            self.assertEqual(f.getvalue(), 
            "** class name missing **\n")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create MyModel")
            self.assertEqual(f.getvalue(), 
            "** class doesn't exist **\n")
        
        with patch('sys.stdout', new=StringIO()) as f:
            TestConsole.__cls = TestConsole.__get_m_class(
                TestConsole._models[randint(0, 6)])
            HBNBCommand().onecmd(f"create {eval(TestConsole.__cls)}")
            TestConsole.__id = f.getvalue()
            self.assertRegex(TestConsole.__id,
            "^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}$")
    
    def test_show(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
            self.assertEqual(f.getvalue(), 
            "** class name missing **\n")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show MyModel")
            self.assertEqual(f.getvalue(), 
            "** class doesn't exist **\n")
        
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel")
            self.assertEqual(f.getvalue(), 
            "** instance id missing **\n")
        
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                "show " + eval(TestConsole.__cls) + " " + eval(TestConsole.__id))
            # _list = f.getvalue().split(" ")
            # k, v = _list[0], _list[2]
            # self.assertEqual(k, str(TestConsole.__cls))
            self.assertEqual(f.getvalue(), 
            "** class name missing **\n")
    
    @classmethod
    def __get_m_class(cls, name):
        """
        Returns a Model Class if present
        Args:
            name (str): Possible class name
        Return:
            Class identifier if present else None
        """
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        for ele in dir():
            if name == ele:
                return eval(ele)
        return None


if __name__ == "__main__":
    unittest.main()