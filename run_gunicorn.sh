#!/bin/bash
/home/lucas/www/socialrank.codelucas.com/socialrank-env/bin/gunicorn -c /home/lucas/www/socialrank.codelucas.com/socialrank-env/socialrank/server/gunicorn_config.py socialrank.wsgi
