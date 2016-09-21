# bottle-ssl

[Bottle][bottle] is a great micro web framework that can be as minimalist or
feature rich as one wants.  Bottle is great for rapid development and for
debugging. However, Bottle is not recommended to be deployed in production as it
lacks security [and speed][serverOptions].  The developers of Bottle know this
and so made Bottle easily extendible.

A common want in web programming is having a secure login page and to remember
the logged in user.  This cannot be achieved without extending Bottle through
various plugins.  What this page shows is how to configure bottle so that this
want can be satisified.  In the end the web page will be able to take a user
name and password and verify it on a linux server.

## Reqiurements:

- Python 2.5+.  Minimum requirement to run Bottle and friends.
- [Bottle][bottle]: This will be the web framework that will have everything based on it.
- [CherryPy][cherrypy]: Bottle can't achieve SSL or heavy traffic, so this is where CherryPy comes in.
- [Beaker][beaker]: Will be used as Bottle middleware that allows session data.
- [PyOpenSSL][pyopenssl]: CherryPy can't operate SSL without this!
- [OpenSSL][openssl]: Program used to generate the self signed certificate.

Before you `pip install` the python depenencies you will need to install
Openssl and libffi-dev (most likely with the command `sudo apt-get install
openssl libffi-dev`)

## OpenSSL and Self Signed Certificates

First the SSL certificate and private key are generated using OpenSSL.  It is
absolutley critical to generate a private key with at least 1024 bits
(recommended: 2048/4096) else you'll run into security or other issues (eg.
[Internet Explorer will not display the page no matter what if there are less
than 1024 bits][1024bit]).  The generated files, in this case are privkey.pem and
cacert.pem.  For simplicity's sake, these are stored inside the directory.

```bash

openssl genrsa -out privkey.pem 2048
openssl req -new -x509 -key privkey.pem -out cacert.pem -days 1095

```

While the source code can speak for itself I thought I would highlight some
more of confusing aspects of this project. 

## Bottle and SSL

As previously dicussed, Bottle does not support SSL; however, CherryPy has it
implemented.  The question is, how can we run Bottle with a SSL enabled CherryPy
server?  When starting the Bottle application, one can specify the server to run
on with `server='<serverName>'`.  The first thought is to have
`server='cherrypy'`, but this starts the default CherryPy server which is not
SSL enabled.  We don't want the default server, we want a way to specify options
such as where the private key and certificate are located.  The Bottle
documentation is nonexistant on how to accomplish this, so I didn't know if this
was even possible.  When encountered with a siutation such as this, a definitive
answer will be found inside the [source code][bottleGitHub].  I found that
instead of string parameter for `server` that a subclass of Bottle's
`ServerAdapter` is also valid.  That was the hard part. Subsequently I looked at
[another website][cherrypySSL] as to how to configure CherryPy so that it used
my private key and certification.

[bottle]: http://bottlepy.org/
[bottleGitHub]: https://github.com/defnull/bottle/blob/master/bottle.py
[cherrypy]: http://cherrypy.org/
[cherrypySSL]: http://webpy.org/cookbook/ssl
[beaker]: http://beaker.readthedocs.org/en/latest/
[pyopenssl]: https://launchpad.net/pyopenssl 
[openssl]: http://openssl.org/
[serverOptions]: http://bottlepy.org/docs/dev/deployment.html#server-options
[1024bit]: http://technet.microsoft.com/en-us/security/advisory/2661254
