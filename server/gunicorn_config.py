command = '/home/lucas/www/socialrank.lucasou.com/socialrank-env/bin/gunicorn'
pythonpath = '/home/lucas/www/socialrank.lucasou.com/socialrank-env/socialrank'
bind = '127.0.0.1:8080'
workers = 1
user = 'lucas'
accesslog = '/home/lucas/logs/socialrank.lucasou.com/gunicorn-access.log'
errorlog = '/home/lucas/logs/socialrank.lucasou.com/gunicorn-error.log'
