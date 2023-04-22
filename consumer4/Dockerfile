FROM python:latest
WORKDIR /app
COPY consume3.py .
# RUN pip install --no-cache-dir -r requirements.txt
# RUN apt update
# ENV MY_NETWORK_IP=172.18.0.2
RUN pip3 install flask
RUN pip3 install pika
RUN pip3 install uuid
RUN pip3 install mysql-connector-python
# Expose port 5000
EXPOSE 3306
# RUN pip install json
# RUN python3 rope.py

CMD ["python", "consume3.py"]

