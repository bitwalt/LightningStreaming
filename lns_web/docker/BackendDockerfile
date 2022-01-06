FROM python:3
ENV   PYTHONUNBUFFERED 1
RUN mkdir /app
COPY backend/requirements.txt /app/
RUN pip install -r app/requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 8000
# RUN python manage.py migrate
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]