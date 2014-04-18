#!/usr/bin/env python
# First, we import the argparse module
import argparse
import sys

# Let's define a silly function to add and multiply numbers
def my_function(lower_bound, upper_bound, multiply=None, verbose=False):
    
    value = 0
    for x in range(lower_bound, upper_bound):
        if verbose:
            print 'value <- %3d + %3d' % (value, x)
        value = value + x
        
            
    if multiply:
        for x in multiply:
            if verbose:
                print 'value <- %3d * %3d' % (value, x)
            value = value * x
    
    return value

# Let's define a function to process a list of string arguments
def process_arguments(args):

    # First, construct the parser
    parser = argparse.ArgumentParser(description="Adds a set of numbers, and then multiplies by an optional list")
    
    # Let's add our first argument
    parser.add_argument('-l',                                  # Short switch
                        '--lower-bound',                       # Long switch
                        dest='lower_bound',                    # Destination in our option dict
                        type=int,                              # Type of argument we expect
                        default=0,                             # Default value
                        help='Lower bound for the summation'   # Descriptive text
                        )
    
    # And another
    parser.add_argument('-u',
                        '--upper-bound',
                        dest='upper_bound',
                        type=int,
                        default=10,
                        help='Upper bound for the summation')
    
    # How about optional positional arguments?
    parser.add_argument(dest='multiply',
                        nargs='*',
                        type=float,
                        default=None,
                        help='One or numbers to multiply with the sum')
    
    # A binary switch?
    parser.add_argument('-v',
                        '--verbose',
                        dest='verbose',
                        action='store_true',
                        default=False,
                        help='verbose output')
    
    # Finally, apply the parser to the argument list
    options = parser.parse_args(args)
    
    # And return it as a dict
    return vars(options)

if __name__ == '__main__':
    options = process_arguments(sys.argv[1:])
    print my_function(  options['lower_bound'], 
                        options['upper_bound'], 
                        multiply=options['multiply'], 
                        verbose=options['verbose'])

