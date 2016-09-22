from bottle import (route, response, run, redirect, request, static_file,
                    ServerAdapter, default_app)
from beaker.middleware import SessionMiddleware
from cherrypy import wsgiserver
from cherrypy.wsgiserver.ssl_pyopenssl import pyOpenSSLAdapter
from OpenSSL import SSL
import json
import crypt
import spwd
import pwd


@route('/<filename:path>')
def send_static(filename):
    return static_file(filename, root=".")


@route('/whoami')
def whoami():
    response.content_type = 'application/json; charset=utf-8'
    try:
        username = current_user()
    except:
        username = None
    finally:
        return json.dumps({"d": username})


@route('/')
def default():
    redirect("/index.html")


@route('/login', method='POST')
def login():
    name = request.forms.UserName
    passwd = request.forms.Password

    # if the username does not appear in the password
    # file, then a KeyError is thrown
    try:
        crypted = pwd.getpwnam(name)[1]
    except KeyError:
        redirect('/index.html')

    # use shadow password if needed
    if crypted and (crypted == 'x' or crypted == '*'):
        crypted = spwd.getspnam(name)[1]

    if crypt.crypt(passwd, crypted) == crypted:
        session = beakerSession()
        session['username'] = name

    redirect('/index.html')


@route('/logout', method='POST')
def logout():
    session = beakerSession()
    session.delete()


def beakerSession():
    return request.environ.get('beaker.session')


def current_user():
    session = beakerSession()
    username = session.get('username', None)
    if username is None:
        raise Exception("Unauthenticated user")
    return username


# By default, the server will allow negotiations with extremely old protocols
# that are susceptible to attacks, so we only allow TLSv1.2
class SecuredSSLServer(pyOpenSSLAdapter):
    def get_context(self):
        c = super(SecuredSSLServer, self).get_context()
        c.set_options(SSL.OP_NO_SSLv2)
        c.set_options(SSL.OP_NO_SSLv3)
        c.set_options(SSL.OP_NO_TLSv1)
        c.set_options(SSL.OP_NO_TLSv1_1)
        return c


# Create our own sub-class of Bottle's ServerAdapter
# so that we can specify SSL. Using just server='cherrypy'
# uses the default cherrypy server, which doesn't use SSL
class SSLCherryPyServer(ServerAdapter):
    def run(self, handler):
        server = wsgiserver.CherryPyWSGIServer((self.host, self.port), handler)
        server.ssl_adapter = SecuredSSLServer('cacert.pem', 'privkey.pem')
        try:
            server.start()
        finally:
            server.stop()

# define beaker options
# -Each session data is stored inside a file located inside a
#  folder called data that is relative to the working directory
# -The cookie expires at the end of the browser session
# -The session will save itself when accessed during a request
#  so save() method doesn't need to be called
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': True,
    'session.data_dir': './data',
    'session.auto': True
}

# Create the default bottle app and then wrap it around
# a beaker middleware and send it back to bottle to run
app = default_app()
myapp = SessionMiddleware(app, session_opts)
run(app=myapp, host='0.0.0.0', port=443, server=SSLCherryPyServer)
