PyHTTP-Console
==============

This program is inspired by Cloudhead's node.js based http-console
located at <http://github.com/cloudhead/http-console>

QuickStart
--------
Assuming you have CouchDB installed and running on port 5984, this is how a typical session looks like.
![Usage Example][1]

[1]: http://dl.dropbox.com/u/7409018/http-console.png

Features
--------

1. Server Navigation using a filesystem like approach: cd
1. Server queries on relative and absolute paths using GET or POST
1. Header highlights

Other features thanks to nifty python modules:

1. Tab completion of commands
1. Command History


Installation
------------

Prerequisites: termcolor and colorama

    easy_install termcolor
    easy_install colorama

Alternatively, if you are a pip user

    pip install termcolor
    pip install colorama

Get the code:

    git clone http://github.com/divyekapoor/pyhttp-console.git

Or alternatively, just download the source from the Downloads section and extract it.
Just run the http-console.py from wherever you may be and enjoy!

Feedback
--------

I would love to hear from you as to the improvements that can be made to this project.
Catch me on Twitter at <http://twitter.com/divyekapoor> and drop your thoughts.
In case you encounter bugs, feel free to add an issue to the project.

Major Similarities
------------------

1. Terminal colours
1. HTTP Support

Todo
----

1. PUT, HEAD support
1. Tests
1. Headers add and remove support

