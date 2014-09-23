
from openmdao.main.interfaces import Interface, implements
from zope.interface import implementer
from openmdao.main.api import Component, Assembly, VariableTree
from openmdao.lib.datatypes.api import Slot, Instance


# FUSED Framework ----------------------------------
def interface(comp_cls):
    """Returns the class ICompCls(Interface)"""
    class MyInterface(Interface):pass
    MyInterface.__name__ = 'I' + comp_cls.__name__
    return MyInterface

def base(cls):
    """Decorator for a FUSED base class"""
    return implementer(interface(cls))(cls)


def strip_init(cls):
    """Decorator function that removes the __init__ of 
    a class to avoid the super(MyClass) bug). 

    Usage
    -----

    class A(object):
        def __init__(self):
            print 'init A'
        
    def my_deco(cls):
        obj = strip_init(cls2)()
        print obj.__class__.__name__
        return cls
            
    @my_deco        
    class B(A):
        def __init__(self):
            print 'init B'
            super(B, self).__init__()    # <--- create the bug because 
                                         #   B does not exist in the context
                                         # of my_deco

    """
    try:
        obj = cls()
        return cls
    except NameError as e:
        print 'Warning:',e
        print 'The __init__ of this class is going to be removed for checking the interfaces'
        print 'see the strip_init function in interface.py'
        mdic = dict(cls.__dict__)
        mdic['__init__'] = cls.__base__.__init__
        cls2 = type(cls.__name__, (cls,), mdic)
        return cls2

class _implement_base(object):
    """
    tag the curent class with the base class interface. 
    Add a check on the I/O. 

    Usage:
    ------

    @base
    class BaseClass(object):
        vi1 = Float(iotype='in')
        vi2 = Float(iotype='in')
        vo1 = Float(iotype='out')

    @_implement_base(BaseClass)
    class MyClass(object):    
        vi1 = Float(iotype='in')
        vi2 = Float(iotype='in')
        vo1 = Float(iotype='out')
    """
    def __init__(self, cls):
        """Store the base calss in the object variable __base

        parameters
        ----------
        cls     class
                the base class to store

        """
        self.__base = cls
        
    def __call__(self, cls):
        """Check if the new class satisfy the requirements 
        of the base class and return the implementation of 
        the new class

        parameters
        ----------
        cls     class
                the new class to process

        """
        self.check(cls)
        return base(implementer(interface(self.__base))(cls))

    def check(self, cls):
        """Do some checks on the I/O compatibility of the class with its base:

        TODO:
        -----
            * Add test on variable type
        """

        ob = strip_init(cls)()
        ob_base = strip_init(self.__base)()
        #ob = cls()
        #ob_base = self.__base()
        if issubclass(cls, VariableTree) or issubclass(self.__base, VariableTree):
            try: 
                assert set(ob_base.list_vars()).issubset(set(ob.list_vars()))
            except:
                raise Exception('Variables of the class %s are different from base %s:'%(cls.__name__, self.__base.__name__), ob.list_vars(), ob_base.list_vars())
        else: ## Assuming it's a Component or Assembly
            try: 
                assert set(ob_base.list_inputs()).issubset(set(ob.list_inputs()))
            except:
                raise Exception('Inputs of the class %s are different from base %s.  The missing input(s) of %s are: %s'%(cls.__name__, self.__base.__name__,cls.__name__, (set(ob_base.list_inputs())-set(ob.list_inputs())))) #, ob.list_inputs(), ob_base.list_inputs())
            try:
                assert set(ob_base.list_outputs()).issubset(ob.list_outputs())
            except:
                raise Exception('Outputs of the class %s are different from base %s.  The missing output(s) of %s are: %s'%(cls.__name__, self.__base.__name__,cls.__name__, (set(ob_base.list_outputs())-set(ob.list_outputs())))) #, ob.list_outputs(), ob_base.list_outputs())


class implement_base(object):
    """
    Decorator to implements the bases. Can both be used for Components and Assemblies

    Usage:
    ------

    @base
    class BaseClass1(object):
        vi1 = Float(iotype='in')
        vi2 = Float(iotype='in')
        vo1 = Float(iotype='out')

    @base
    class BaseClass2(object):
        vi3 = Float(iotype='in')
        vi4 = Float(iotype='in')
        vo2 = Float(iotype='out')

    @implement_base(BaseClass1, BaseClass2)
    class MyClass(object):
        vi1 = Float(iotype='in')
        vi2 = Float(iotype='in')
        vi3 = Float(iotype='in')
        vi4 = Float(iotype='in')

        vo1 = Float(iotype='out')
        vo2 = Float(iotype='out')


    """
    def __init__(self, *args):
        self.__bases = args
    def __call__(self, cls):
        out = cls
        for base in self.__bases:
            out = _implement_base(base)(out)
        return out

    
def InterfaceInstance(cls, *args, **kwargs):
    return Instance(interface(cls), *args, **kwargs)

