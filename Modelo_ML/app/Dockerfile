FROM python:3.14.0rc2
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
EXPOSE 5000