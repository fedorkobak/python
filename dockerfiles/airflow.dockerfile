FROM ghcr.io/fedorkobak/jlb:latest

ENV AIRFLOW__CORE__AUTH_MANAGER=airflow.providers.fab.auth_manager.fab_auth_manager.FabAuthManager

# installation of the airflow.
# the apache-airflow-providers-fab
RUN pip3 install apache-airflow==3.2.1 apache-airflow-providers-fab==3.6.3 && \
    airflow db migrate && \
    airflow users create \
        --username admin \
        --password admin \
        --firstname Fedor \
        --lastname Kobak \
        --role Admin \
        --email spiderman@superhero.org;

RUN sed -i 's/load_examples = True/load_examples = False/g' /root/airflow/airflow.cfg

CMD ["sh", "-c", "jupyter lab --ip 0.0.0.0 --allow-root & airflow api-server"]
