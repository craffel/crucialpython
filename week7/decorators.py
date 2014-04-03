# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # CRÜCIAL PYTHON Week 7: Decorators

# <codecell>

from IPython.core.display import Image
Image(url='http://labrosa.ee.columbia.edu/crucialpython/logo.png', width=600)

# <markdowncell>

# This session of crucial python borrows heavily from 
# http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
# which covers decorators from the ground up.

# <markdowncell>

# ### Background: Functions as first-class objects
# In Python, functions are objects that you can pass around and manipulate just as you would a normal variable.

# <codecell>

def say_hey():
    """ A function which always returns the string 'hey' """
    return 'hey'
def print_function_output(function):
    """ A function which calls an input function and prints its output """
    print function()

print_function_output(say_hey)

# <codecell>

# Functions can also be returned just like normal variables 
def i_return_a_function():
    """ A function which builds a new function and returns it """
    def i_get_returned():
        """ This is a nested function, which gets built during i_return_a_function """
        print "I was built in i_return_a_function"
    return i_get_returned

result = i_return_a_function()
print result
result()

# <markdowncell>

# ### Background: Function closures
# When you define a function within another function, it will remember what the local namespace looked like *at definition time*.

# <codecell>

def make_printer(print_me):
    """ Construct a function which prints whatever was input to make_printer """
    def printer():
        """ Print the value of print_me passed to make_printer when printer was created """
        print print_me
    return printer

hey_printer = make_printer('hey')
you_printer = make_printer('you')
hey_printer()
you_printer()

# <markdowncell>

# Aside: `functools.partial` is a more useful example.  From the documentation: "The partial() is used for partial function application which “freezes” some portion of a function’s arguments and/or keywords resulting in a new object with a simplified signature."

# <codecell>

print int.__doc__

# <codecell>

import functools
basetwo = functools.partial(int, base=2)
basetwo('0110')

# <markdowncell>

# ## Decorators!
# Decorators are simply functions which take a function as input and return a function.

# <codecell>

def double_function(function):
    """ Return a version of function which doubles its output """
    def doubler():
        return function()*2
    return doubler

def return_10():
    return 10
return_double_10 = double_function(return_10)
print return_10()
print return_double_10()

# <markdowncell>

# The syntax `function = decorator(function)` ends up popping up a lot when you start using decorators.  So, as a convenience, Python includes the @ syntax.  Placing @decorator above a function definition replaces the function at definition time with its decorated version.  You might remember seeing this syntax last week; it's used by `flask` extensively.

# <codecell>

@double_function
def return_20():
    return 10
print return_20()

# <markdowncell>

# ### Practical Example
# Say we have a bunch of functions, all of which take at least one input: `x`, which should be a float which is greater than 0.  We can use a decorator to check for appropriate values of `x` and apply it to each function

# <codecell>

import warnings
def validate_x(x_function):
    """ Validates the input values of a function. """
    # The *args and **kwargs variables are any function arguments beyond the first
    def x_function_validated(x, *args, **kwargs):
        # Check that x is a float, and try casting it
        if not type(x) is float:
            warnings.warn('x is not a float')
            try:
                x = float(x)
            except:
                raise TypeError('Could not cast x to a float')
        # Confirm that x is greater than 0
        if not x > 0:
            raise TypeError('x should be greater than 0')
        return x_function(x, *args, **kwargs)
    return x_function_validated

@validate_x
def root(x, n):
    """ Compute the n'th root of x """
    return x**(1/float(n))

@validate_x
def invert_multiply_add(x, multiply=1., add=0.):
    """ Computes multiply/x + add """
    return multiply/x + add

# <codecell>

print root(16, 4)

# <codecell>

print invert_multiply_add(0, 1)

# <markdowncell>

# More substantial examples are available here:
# https://wiki.python.org/moin/PythonDecoratorLibrary

