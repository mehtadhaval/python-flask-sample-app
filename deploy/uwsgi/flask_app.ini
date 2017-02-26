[uwsgi]
chdir = /home/deploy/python-flask-sample-app
wsgi-file = run.py
virtualenv = /home/deploy/python-flask-sample-app/venv

socket = /var/run/uwsgi/flask_app.sock
uid = deploy
gid = deploy

processes = 4
threads = 4

logto = /var/log/uwsgi/flask_app.log

#master mode - will be able to respawn processes if they die
master

#Multiple apps will share the same python interpreter env
single-interpreter

#socket listen backlog queue size
listen = 100

#all logging activity will be offloaded to a thread
threaded-logger

#write master process pid to a file so that can be used for reloading / shutting down
pidfile = /var/run/uwsgi/flask_app.pid
