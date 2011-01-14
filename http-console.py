#!/usr/bin/env python
#
#          Copyright Divye Kapoor 2010
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)
#
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
    Cmd.multilineCommands = [ "data", "headers" ]
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

    def _update_headers(self, header, value):
        header = header.capitalize()
        if value != "":
            self.headers[header] = value
        elif value == "" and header in self.headers:
            del(self.headers[header])

    def _print_headers(self, headers):
        for h,v in headers.items():
            print colored(h.capitalize() + ":","white", attrs=['bold']), v

    def _execute(self, request):
        """ Execute an HTTP request. Currently, only GET and POST are supported """
        try:
            f = urllib2.urlopen(request)
            print colored("HTTP Status: " + str(f.getcode()) + " " + f.msg, 'green', attrs=['bold'])
            self._print_headers(f.headers.dict)
            print "\n"
            print f.read()
            f.close()
        except (urllib2.HTTPError, urllib2.URLError, IOError) as e:
            print colored(e, 'red', attrs=['bold'])

    def _set_temp_path(self, line):
        """ This function temporarily modifies the path to include the relative/absolute path provided
        as part of the GET or POST request """
        self._old_path = self.urlparts["path"]

        if not line.startswith("/"):
            if not self.urlparts["path"].endswith("/"):
                self.urlparts["path"] += "/"
            self.urlparts["path"] += line
        else:
            self.urlparts["path"] = line

    def _restore_path(self):
        self.urlparts["path"] = self._old_path

    def _prepare_url(self, line):
        self._set_temp_path(line)
        url = self._get_url()
        self._restore_path()
        print "Requesting ", colored(url, "yellow")
        return url

    def do_get(self, line):
        """ Perform a GET request on the server indicated by the current path """
        old_query = self.urlparts["query"]
        self.urlparts["query"] = self.data
        
        url = self._prepare_url(line)
        request = Request(url, None, self.headers)
        self._execute(request)

        self.urlparts["query"] = old_query

    def do_post(self, line):
        """ Perform a POST request on a URL. Set the data for the post request via the data command."""
        url = self._prepare_url(line)
        request = Request(url, self.data, self.headers)
        self._execute(request)

    def do_put(self, line):
        """Perform a PUT request on a URL. Set the data for the PUT request via the data command."""
        url = self._prepare_url(line)
        request = Request(url, self.data, self.headers)
        # HACK: support PUT, HEAD and DELETE - 
        # via http://stackoverflow.com/questions/111945/is-there-any-way-to-do-http-put-in-python
        request.get_method = lambda: "PUT" 
        self._execute(request)

    def do_delete(self, line):
        """Perform a DELETE request on a URL. Set the data for the DELETE request via the data command."""
        url = self._prepare_url(line)
        request = Request(url, self.data, self.headers)
        # HACK: support PUT, HEAD and DELETE - 
        # via http://stackoverflow.com/questions/111945/is-there-any-way-to-do-http-put-in-python
        request.get_method = lambda: "DELETE"
        self._execute(request)

    def do_head(self, line):
        """Perform a HEAD request on a URL. The head request should typically have no data supplied."""
        url = self._prepare_url(line)
        request = Request(url, self.data, self.headers)
        # HACK: support PUT, HEAD and DELETE - 
        # via http://stackoverflow.com/questions/111945/is-there-any-way-to-do-http-put-in-python
        request.get_method = lambda: "HEAD"
        self._execute(request)
        

    def do_headers(self, line):
        """ Get or set the headers that will be sent along with the request.
        For example:
            headers
            > Content-type: text/plain
            >
            Accept: */*
            Content-type: text/plain
        """
        if line != "":
            for headerline in line.split('\n'):
                try:
                    header,value = headerline.split(':',1)
                    value = value.lstrip()
                    self._update_headers(header, value)
                except Exception as e:
                    print colored(e, 'red', attrs=['bold'])

        self._print_headers(self.headers)

    def do_url(self, line):
        if line is not None and line != "":
            self._save_url(line)
        else:
            print self._get_url()

    def do_port(self, line):
        hostport = self.urlparts["netloc"].split(":", 1)
        if line == "":
            if len(hostport) > 1:
                print hostport[1]
            else:
                print 80 # Assume default port for HTTP
        else:
            host = hostport[0]
            port = line
            self.urlparts["netloc"] = host + ":" + port

        self._update_prompt()

    def do_data(self, line):
        ''' Set the data to be sent as the query string in a GET request or as the POST body for POST '''
        self.data = line


    def do_cd(self, line):
        ''' Change the current path on the server. Use ./ to create a relative path, / for an absolute path and ../ to go up '''
        if line == "":
            self.urlparts["path"] = ""
        elif line.startswith("/"):
            self.urlparts["path"] = line[1:]
        elif line.startswith(".."):
            self.urlparts["path"] = self.urlparts["path"].rsplit("/", line.count(".."))[0]
        else:
            if not self.urlparts["path"].endswith("/"):
                self.urlparts["path"] += "/"
            self.urlparts["path"] += line

        self.urlparts["path"].replace("//", "/")
        self._update_prompt()

    def do_json(self, line):
        ''' Switch on JSON Mode by altering the Accept Header '''
        self.json_mode = not self.json_mode # Toggle
        if self.json_mode:
            self._update_headers("Accept", "application/json")
        else:
            self._update_headers("Accept", "*/*")
        print "JSON mode is now %s" % (self.json_mode and "ON" or "OFF")

    def do_path(self, line):
        ''' Shows the current path on the server. Use cd if you want to change paths '''
        print self.urlparts["path"]

#    def precmd(self, line):
#        if line.parsed[0].endswith(":"):
#            self._update_headers(line.parsed[0][:-1], line.lstrip())
#            return line
#        return Cmd.precmd(self,line)
#

if __name__ == "__main__":
    print ">", colored("pyhttp-console v.0.1", "white", attrs=["bold"])
    print """> Simple Operations: get, post, url, port, cd, data, json, path
> Type help for help, quit or q to exit
    """

    shell = HTTPRepl()
    shell.cmdloop()

