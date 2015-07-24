'''
API Controllers
This is where you define controllers for your api
'''

class BaseController(object):
    '''
    Base class for all controllers
    '''

    __controller_name = None

    def __init__(self, name):
        self.__controller_name = name

    @property
    def controller_name(self):
        '''
        Method to return the controller name
        :return:
        '''
        return self.__controller_name


class MyController(BaseController):
    '''
    Sub class of the Base class
    '''

    def some_function(self):
        '''
        Method to extend the base class
        :return:
        '''
        raise NotImplemented