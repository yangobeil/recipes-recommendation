FROM base_image

COPY scraping.py .
COPY app.py .

CMD gunicorn --bind 0.0.0.0:5000 --workers=1 --threads=4 app:app --timeout=0