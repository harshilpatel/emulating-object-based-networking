FROM python:2.7-slim
WORKDIR /app
COPY . /app
EXPOSE 8081

CMD ["python","client.py"]
# CMD python client.py && tail -f '/app/client.log'