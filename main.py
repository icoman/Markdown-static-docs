#!/usr/bin/python

"""

MIT License

Copyright (c) 2019 Ioan Coman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

from __future__ import print_function

import os
import sys
import socket
import bottle
import markdown
from beaker.middleware import SessionMiddleware

'''

pip install bottle
pip install waitress
pip install markdown

http://pygments.org/
pip install Pygments
pygmentize -S default -f html -a .codehilite > styles.css

'''



#cookie session
SESSION_NAME = 'bottleserver.session'
COOKIE_CRYPT_KEY = 'alfa123-12345-a87-123-asiu-23423532-oapsaas'
MD_FOLDER = None

current_dir = os.path.dirname(__file__)
static_folder = os.path.join(current_dir,'static')


session_opts = {
    #session stored only in cookie (max 4096 bytes) is best for cluster
    'session.cookie_expires': 24*60*60, #in seconds - 24 de ore
    #'session.cookie_expires': True,
    'session.auto': True, # When set, calling the save() method is no longer required, and the session will be saved automatically anytime its accessed during a request.
    'session.key':SESSION_NAME,
}

app = bottle.Bottle()

def js_redirect(location):
    return '<html><script>location.href="%s";</script></html>' % (location)

@app.route('/')
def default():
    return js_redirect("/README")

@app.route('/static/<path:path>')
def callback(path):
    return bottle.static_file(path, root=static_folder)

@app.route('/<path:path>')
def callback(path):
    '''
        Any page
    '''
    try:
        #assume is markdown document
        if path.endswith('.md'):
            filename = path
        else:
            filename = '{}.md'.format(path)
        fullname = os.path.sep.join((MD_FOLDER, filename))
        with open(fullname, 'rt') as f:
            extensions = [
                #'markdown.extensions.fenced_code', #is included in "extra"
                'markdown.extensions.codehilite',
                'markdown.extensions.extra'
            ]
            mdtext = markdown.markdown(f.read(), extensions=extensions)
            ret = '''<html>
<head>
   <link rel="stylesheet" type="text/css" href="/static/styles.css">
</head>
<body>
{}
</body>
</html>
'''.format(mdtext)
    except Exception as ex:
        #assume is static file - maybe an image
        #print(ex)
        #mdtext = ''
        ret = bottle.static_file(path, root=MD_FOLDER)
    return ret


def main():
    sess_root = SessionMiddleware(app, session_opts)
    PORT = int(os.getenv('PORT') or 80)
    HOST = os.getenv('HOST','localhost')
    global MD_FOLDER
    MD_FOLDER = os.getenv('MD_FOLDER', os.getcwd())
    if os.getenv('BOTTLE_CHILD'):
        print ('Start web server on port {}.'.format(PORT))
        print ('Hostname and IP:')
        for ip in socket.gethostbyname_ex(socket.gethostname()):
            if ip:
                print ('\t{}'.format(ip))
        print ('Python version: {}'.format(sys.version))
        print('MD_FOLDER =',MD_FOLDER)
    #bottle.run(app=sess_root, server='paste',      host=HOST, port=PORT, debug=True, reloader=True)
    #bottle.run(app=sess_root, server='cherrypy', host=HOST, port=PORT, debug=True, reloader=True)
    bottle.run(app=sess_root, server='waitress', host=HOST, port=PORT, debug=True, reloader=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(ex)






