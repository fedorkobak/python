FROM ghcr.io/fedorkobak/jlb:latest

# installation of the airflow.
# the apache-airflow-providers-fab
RUN pip3 install apache-airflow==3.2.1 && \
    airflow db migrate

RUN sed -i 's/load_examples = True/load_examples = False/g' /root/airflow/airflow.cfg

WORKDIR /knowledge
COPY dockerfiles/airflow.cfg /root/airflow/airflow.cfg

CMD ["sh", "-c", "jupyter lab --ip 0.0.0.0 --allow-root & airflow standalone"]
