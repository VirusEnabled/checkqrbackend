wsgi_app = 'checkqrgpcbackend.wsgi:application'
bind = '0.0.0.0:80'
workers = 4
accesslog = '-'
access_log_format = '%({X-Real-IP}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
