web: gunicorn storefront.wsgi --log-file -
worker: celery -A storefront worker --loglevel=info
