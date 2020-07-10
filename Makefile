run:
	gunicorn -b localhost:5000 wsgi:app

requirements:
	pip install --user -r requirements.txt
