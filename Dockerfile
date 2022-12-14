FROM rabbitmq:3.11-management
EXPOSE 5672
EXPOSE 15672
EXPOSE 1883
RUN rabbitmq-plugins enable --offline rabbitmq_mqtt