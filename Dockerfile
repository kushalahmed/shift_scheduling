FROM python:3.5.1

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 6542

CMD ["sh", "./entrypoint.sh"]