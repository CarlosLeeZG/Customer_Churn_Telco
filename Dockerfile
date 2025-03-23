# Select appropriate python ()
FROM python:3.10

WORKDIR /flask-app

COPY ./requirements.txt /flask-app/requirements.txt
COPY ./src /flask-app/src
COPY ./models /flask-app/models

# Add /src directory to PYTHONPATH, so that model.py Python module can be found
# To add multiple directories, delimit with colon e.g. /flask-app/src:/flask-app
ENV PYTHONPATH /flask-app/src


RUN pip install -r /flask-app/requirements.txt --no-cache-dir
EXPOSE 80

# Start the Flask app using gunicorn
CMD ["gunicorn", "--bind=0.0.0.0:80", "src.app:app"]