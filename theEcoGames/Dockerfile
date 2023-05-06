FROM python:3.10
COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt --no-cache-dir
COPY . theEcoGames
WORKDIR /theEcoGames
EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000