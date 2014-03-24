#!/bin/bash

exec /home/lucas/www/socialrank.lucasou.com/socialrank-env/bin/gunicorn -c /home/lucas/www/socialrank.lucasou.com/socialrank-env/socialrank/server/gunicorn_config.py socialrank.wsgi
