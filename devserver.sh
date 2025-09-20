source venv/bin/activate
exec python mysite/manage.py runserver 0.0.0.0:${PORT:-8000}