"""
#API Controllers
This is where you define controllers for your api

> Blockquotes are very handy in email to emulate reply text.
> This line is part of the same quote.

That was important

"""

def simple_function(stuff):
    """
    Just a simple function to show documentation features
    :param stuff:
    :return:
    """

class BaseController(object):
    """
    Base class for all controllers

    Use this class for writing controllers and other stuff
    * Cool Features
        - Like this
        - and this
        - and this
    * Stable
        - Kind of
        - Don't break it
    * Fast

    **Optional**: use it for the staticmethod only
    """

    __controller_name = None

    def __init__(self, name):
        self.__controller_name = name

    def controller_name(self, name):
        """
        Method to return the controller name
        :param name: The name of the controller
        :return:
        """
        self.__controller_name = name
        return True

    def class_method(cls):
        """
        Example of a class method
        """
        return

    @staticmethod
    def static_method():
        """
        Example of a static method
         * Nice method
         * Has bugs

        """
        return


class MyController(BaseController):
    """
    Sub class of the Base class

    Go to this Link for more details on this design: [click here](https://www.google.com)

    """

    def some_method(self):
        """
        Method to extend the base class

        Sample Output
        ```json
        {"menu": {
          "id": "file",
          "value": "File",
          "popup": {
            "menuitem": [
              {"value": "New", "onclick": "CreateNewDoc()"},
              {"value": "Open", "onclick": "OpenDoc()"},
              {"value": "Close", "onclick": "CloseDoc()"}
            ]
          }
        }}
        ```

        :return:
        """
        raise NotImplemented