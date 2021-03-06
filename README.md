# HipFrog
<img width=100px align=right alt="Hipfrog" src="/glassfrog/static/hipfrog.png">
<a href="https://travis-ci.org/wardweistra/hipfrog"><img alt="Build Status" src="https://travis-ci.org/wardweistra/hipfrog.svg?branch=master"></a>

<a href="https://codecov.io/gh/wardweistra/hipfrog"><img alt="codecov" src="https://codecov.io/gh/wardweistra/hipfrog/branch/master/graph/badge.svg"></a>

An open source [Hipchat](http://hipchat.com/) bot for accessing the [Holacracy](http://www.holacracy.org/) tool [Glassfrog](https://glassfrog.com).

## Installation in your Hipchat room
Follow https://marketplace.atlassian.com/plugins/hipfrog to install the plugin in your Hipchat room.

## Development
Hipfrog is using [Glassfrog API V3 beta](https://github.com/holacracyone/glassfrog-api/tree/API_v3). Tested on Python 3.5.2.

* Download: `git clone https://github.com/wardweistra/hipfrog.git`  
* Install: `python3 setup.py install`  
* Create and upgrade the database with [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/). Tested on Postgres.  
* Test: `python3 tests/glassfrog_tests.py`  
* Run: `python3 runserver.py --debug`  

## Environment settings

Default settings are found at [glassfrog/settings/config.py](glassfrog/settings/config.py). Set your own by following the steps in [settings.cfg](settings.cfg).

## Deployment
Hipfrog can be deployed to run your own managed version of it with Apache2.

Example hipfrog.wsgi (at /var/www/hipfrog/ where application at /var/www/hipfrog/hipfrog/ and dependencies installed with virtualenv):

    #!/usr/bin/env python3
    activate_this = '/var/www/hipfrog/hipfrog/venv/bin/activate_this.py'
    with open(activate_this) as file_:
            exec(file_.read(), dict(__file__=activate_this))
    
    import sys
    import logging
    import os
    
    logging.basicConfig(stream=sys.stderr)
    sys.path.insert(0,"/var/www/hipfrog/hipfrog/")
    
    os.environ["HIPFROG_SETTINGS"] = "/var/www/hipfrog/hipfrog/prod_settings.cfg"
    
    from glassfrog import app as application

Example hipfrog.conf (at /etc/apache2/sites-available):

    WSGIPythonHome "/var/www/hipfrog/hipfrog/venv/bin"
    WSGIPythonPath "/var/www/hipfrog/hipfrog/venv/lib/python3.5/site-packages"
    
    Listen 45277
    
    <VirtualHost *:443>
            ServerName host.wardweistra.nl
            ServerAdmin w@rdweistra.nl
            WSGIScriptAlias /hipfrog /var/www/hipfrog/hipfrog.wsgi
            WSGIDaemonProcess hipfrog-ssl user=ward threads=5
            <Directory /var/www/hipfrog/hipfrog/>
                Order allow,deny
                Allow from all
            </Directory>
            Alias /static /var/www/hipfrog/hipfrog/glassfrog/static
            <Directory /var/www/hipfrog/hipfrog/glassfrog/static/>
                Order allow,deny
                Allow from all
            </Directory>
            ErrorLog ${APACHE_LOG_DIR}/error.log
            LogLevel warn
            CustomLog ${APACHE_LOG_DIR}/access.log combined
    SSLCertificateFile /etc/letsencrypt/live/host.wardweistra.nl/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/host.wardweistra.nl/privkey.pem
    Include /etc/letsencrypt/options-ssl-apache.conf
    </VirtualHost>
