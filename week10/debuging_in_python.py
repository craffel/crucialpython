# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from IPython.core.display import Image
Image(url='http://labrosa.ee.columbia.edu/crucialpython/logo.png', width=600)

# <markdowncell>

# One very good feature of MATLAB is that it is very easy for debugging, which is one of the main reason that many people still use MATLAB. Since correcting bugs is so important in coding, today we are going to share some python feature for debugging. 

# <headingcell level=1>

# Debug in python

# <headingcell level=2>

# Some quick commands

# <markdowncell>

# Assume we have a very simple piece of code

# <codecell>

import numpy as np
X = 1
Y = 'c'
Z = X+Y
A = 3
B = 4

# <markdowncell>

# display variables

# <codecell>

whos

# <codecell>

locals()

# <codecell>

%connect_info

# <codecell>

%qtconsole

# <codecell>

%debug

# <headingcell level=2>

# Break points?

# <markdowncell>

# Pdb/Ipdb is the python debug module, it provides the standatd debug function, including the break points, step in etc. After version 1.0 ipython notebook support the pdb. So we can directly debug in ipython notebook.

# <headingcell level=4>

# Pdb commands

# <markdowncell>

# - pdb.set_trace(): set break point
# - h : help
# - n : next
# - l : list
# - s : step in
# - r : return
# - c : continue
# - q : quit
# - p : print value
# 
# - %run -d theprogram.py : run debuger inside ipython

# <headingcell level=4>

# Set break points

# <codecell>

def square_sum(a,b):
    c=a*a
    d=b*b
    return c+d

# <codecell>

import ipdb as pdb
X = 1
pdb.set_trace()
Y = 1
Z= square_sum(X,Y)
for i in xrange(20):
    X=X+ square_sum(X,Y)/(X*X)
    print X
    pdb.set_trace()

# <codecell>

%run -d sample_debug.py : run debuger inside ipython

# <codecell>

%pdb

# <codecell>

X = 1
Y = 'c'
Z = X+Y
A = 1

