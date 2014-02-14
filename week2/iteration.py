# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # CRÜCIAL PŸTHON Week 2: Iteration

# <codecell>

from IPython.core.display import Image 
Image(url='http://labrosa.ee.columbia.edu/crucialpython/logo.png', width=600) 

# <markdowncell>

# ## Iterators
# Python makes it easy to iterate over objects which are collections of things (**generators**).  This makes for loops look really clean, among other things.

# <codecell>

a_list = ['hey', [1, 2, 3], 2, 10, {}]
for item in a_list:
    print item

# <codecell>

# Another example of an iterator is a file
with open('some_file.txt', 'r') as f:
    for line in f:
        print line

# <markdowncell>

# ## enumerate
# Often, you want to iterate over the indices of the items in an object.  A naive way to do it would be to construct an iterator of the list indices and then access your list using each index.  ``enumerate()`` provides a cleaner way...

# <codecell>

a_dict = {}
# This is kind of ugly and only works for objects with a len
for n in xrange(len(a_list)):
    if isinstance(a_list[n], int):
        a_dict[n] = n*a_list[n]
# You know about pprint (pretty print), right?
import pprint
pprint.pprint(a_dict)

# <codecell>

# file objects don't have a len() because they are not loaded into memory.
# But, you can still use enumerate, which will give you an index.
# Plus, it's cleaner.
for n, item in enumerate(open('some_file.txt', 'r')):
    a_dict[n + 5] = item
pprint.pprint(a_dict)

# <markdowncell>

# ## zip
# One situation where you might be tempted to iterate over list indices is when you need to access multiple lists at a time.  ``zip()`` is your friend here.

# <codecell>

b_list = ['cool', 'great', 'awesome', 'nice', 'sweet']
c_list = range(10, 15)
# Naw
for n in xrange(len(a_list)):
    print n, a_list[n], b_list[n], c_list[n]

# <codecell>

# Yeah
for a_item, b_item, c_item in zip(a_list, b_list, c_list):
    print a_item, b_item, c_item

# <codecell>

# When you need indices and items across lists, enumerate and zip!
for n, (a_item, b_item, c_item) in enumerate(zip(a_list, b_list, c_list)):
    print n, a_item, b_item, c_item

# <markdowncell>

# ## itertools
# The ``itertools`` module provides a lot of fancy and useful functions for combining iterators.  In general, if you have some kind of funky iteration you want to try, check that it isn't already done more cleanly here: http://docs.python.org/2/library/itertools.html

# <codecell>

import itertools

# <codecell>

# We can add lists to concatenate them, but we can't add list + file.
# Plus, we don't know how many items the file has in it.
# Chain lets us iterate over file first, then the list.
# We could do this in two for loops, but then we'd have to duplicate code.
for item in itertools.chain(open('some_file.txt', 'r'), a_list):
    print item

# <codecell>

# Zip for things of different length
for a, b in itertools.izip(a_list, open('some_file.txt', 'r')):
    print a, b

# <codecell>

for a, b in itertools.izip_longest(a_list, open('some_file.txt', 'r')):
    print a, b

# <codecell>

short_list = ['dang', 'cool', 'nice']
# Get all length-n combinations of items from the list, ordered
for item_a, item_b in itertools.permutations(short_list, 2):
    print item_a, item_b

# <codecell>

# Get all length-n combinations of items from the list, no repeats
for item_a, item_b in itertools.combinations(short_list, 2):
    print item_a, item_b

# <markdowncell>

# ## List comprehension
# A truly crucial tool: Create lists using a for loop

# <codecell>

# Basic example: Read in all lines
print [line for line in open('some_file.txt', 'r')]

# <codecell>

# We can apply functions to each item too
print [line.strip() for line in open('some_file.txt', 'r')]

# <codecell>

# Also can use conditional statements
print [line.strip() for line in open('some_file.txt', 'r') if not 'another' in line]

# <codecell>

# Also can do nested list comprehension! 
print [line.strip() for f in ['some_file.txt', 'some_other_file.txt'] for line in open(f, 'r')]

