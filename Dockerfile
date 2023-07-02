FROM python:3.10
WORKDIR /docker-app
COPY /telegrambot /docker-app
COPY /docker /docker-app
ARG TOKEN CCTV_SERVER_HOST CCTV_MQTT_TOPIC
# Use the build-time ARG to set an environment variable
ENV TOKEN=$TOKEN CCTV_SERVER_HOST=$CCTV_SERVER_HOST CCTV_MQTT_TOPIC=$CCTV_MQTT_TOPIC
# Rest of your Dockerfile instructions...
RUN pip install --no-cache-dir -r docker_env.yml 
CMD ["python", "bot.py"]