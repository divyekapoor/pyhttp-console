PyHTTP-Console
==============

Every once in a while when developing a web-app, it becomes useful to send out custom requests
to the server to see how it responds in particular scenarios. Also, just accessing servers
over HTTP on a command line is a nifty tool to have.

This project is a python implementation of a Read, Eval, Print Loop (similar to a Shell) 
which helps you work with HTTP servers easily and efficiently.

This program is inspired by Cloudhead's node.js based http-console
located at <http://github.com/cloudhead/http-console>

QuickStart
--------
Assuming you have [CouchDB](http://couchdb.apache.org) installed and running on port 5984, this is how a typical session looks like.
 
![Usage Example][1]

You can also use this with a Django Development server by just changing the port by issuing:

    http://localhost:5984> port 8000

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

Todo
----

1. PUT, HEAD support
1. Tests
1. Headers add and remove support
1. HTTP response body colorize
