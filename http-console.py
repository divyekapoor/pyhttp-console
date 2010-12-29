#!/usr/bin/env python
import optparse, sys, urllib2
import simplejson as json

from colorama import init, Style, Fore, Back
from termcolor import colored
init()

from urlparse import urlparse,urlunparse
from cmd2 import Cmd
from urllib2 import Request


class HTTPRepl(Cmd):
    ''' 
        HTTPRepl aims to implement a Read, Eval, Print Loop for working with HTTP Servers.
        It has been inspired by cloudhead's http-console located at http://github.com/cloudhead/http-console
        but it's been implemented in python to leverage the cool command line history features of the cmd2 module.
    '''
    Cmd.shortcuts.update({ "." : "cd" })
    Cmd.multilineCommands = [ "data" ]
    DEFAULT_PROMPT_TERMINATOR = "> "

    def __init__(self, *args, **kwargs):
        Cmd.__init__(self, *args, **kwargs)
        self.headers = {
            "Accept" : "*/*",
        }
        self._save_url("http://localhost:5984/")
        self.data = ""
        self.json_mode = False
        self._update_prompt()
    
    def _save_url(self, url):
        """ Convert a raw url into its parts and save it as part of the class """
        parsed_url = urlparse(url)
        self.urlparts = { 
            "scheme" : parsed_url.scheme,
            "netloc" : parsed_url.netloc,
            "path" : parsed_url.path,
            "params" : parsed_url.params,
            "query" : parsed_url.query,
            "fragment" : parsed_url.fragment,
        }
        self._update_prompt()
    
    def _get_url(self):
        """ Convert the split parts of the url back into a unified string """
        return urlunparse(self.urlparts[key] for key in ["scheme", "netloc", "path", "params", "query", "fragment"])

    def _update_prompt(self):
        """ Update the prompt to reflect changes to the url """
        self.prompt = colored(self._get_url() + HTTPRepl.DEFAULT_PROMPT_TERMINATOR, 'white', attrs=['dark', 'bold'])
    
    def _execute(self, request):
        """ Execute an HTTP request. Currently, only GET and POST are supported """
        try:
            f = urllib2.urlopen(request)
            print colored("HTTP Status: " + str(f.getcode()) + " " + f.msg, 'green', attrs=['bold'])
            for h,v in f.headers.dict.items():
                print colored(h.capitalize() + ": ","white", attrs=['bold']), v
            print "\n"
            print f.read()
        except urllib2.HTTPError, e:
            print colored(e, 'red', attrs=['bold'])
 
    def do_get(self, line):
        """ Perform a GET request on the server indicated by the current path """
        old_path = self.urlparts["path"]
        old_query = self.urlparts["query"]

        self.urlparts["path"] += line
        self.urlparts["query"] = self.data

        request = Request(self._get_url(), None, self.headers)
        self._execute(request)

        self.urlparts["query"] = old_query
        self.urlparts["path"] = old_path


    def do_post(self, line):
        """ Perform a POST request on a URL. Set the data for the post request via the data argument."""
        request = Request(self._get_url() + line, self.data, self.headers)
        self._execute(request)

    def do_headers(self, line):
        print json.dumps(self.headers, indent=1)

    def do_url(self, line):
        if line is not None and line != "":
            self._save_url(line)
        else:
            print self._get_url()

    def do_port(self, line):
        if line == "":
            print self.urlparts["netloc"].split(":")[-1]
        else:
            host, port = self.urlparts["netloc"].split(":", 1)
            port = line
            self.urlparts["netloc"] = host + ":" + port

        self._update_prompt()

    def do_data(self, line):
        ''' Set the data to be sent as the query string in a GET request or as the POST body for POST '''
        self.data = line


    def do_cd(self, line):
        ''' Change the current path on the server. Use ./ to create a relative path, / for an absolute path and ../ to go up '''
        if line == "":
            self.urlparts["path"] = "/"
        elif line.startswith("./"):
            self.urlparts["path"] += line[line.index("/"):]
        elif line.startswith("/"):
            self.urlparts["path"] = line
        elif line.startswith(".."):
            self.urlparts["path"] = self.urlparts["path"].rsplit("/", line.count(".."))[0]
        
        self.urlparts["path"].replace("//", "/")
        self._update_prompt()

    def do_json(self, line):
        ''' Switch on JSON Mode by altering the Accept Header '''
        self.json_mode = not self.json_mode # Toggle
        if self.json_mode:
            self.headers["Accept"] = "application/json"
        else:
            self.headers["Accept"] = "*/*"
        print "JSON mode is now %s" % (self.json_mode and "ON" or "OFF")

    def do_path(self, line):
        ''' Shows the current path on the server. Use cd if you want to change paths '''
        print self.urlparts["path"]
       

if __name__ == "__main__":
    shell = HTTPRepl()
    shell.cmdloop()
