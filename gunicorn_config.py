# gunicorn_config.py
bind = '0.0.0.0:{}'.format(os.environ.get('PORT', '5000'))
workers = 3
