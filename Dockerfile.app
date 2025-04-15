FROM apache/spark:3.5.5-java17-python3

USER root

ENV HADOOP_AWS_VERSION=3.3.4 \
    AWS_SDK_VERSION=1.11.1026 \
    SPARK_JARS_DIR=/opt/spark/jars \
    GIT_PYTHON_REFRESH=quiet

RUN curl -fsSL -o ${SPARK_JARS_DIR}/hadoop-aws-${HADOOP_AWS_VERSION}.jar \
        https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_AWS_VERSION}/hadoop-aws-${HADOOP_AWS_VERSION}.jar && \
    curl -fsSL -o ${SPARK_JARS_DIR}/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar \
        https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_SDK_VERSION}/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar

ENV POETRY_HOME="/opt/poetry"
ENV PATH="${POETRY_HOME}/bin:${PATH}"
ENV POETRY_VIRTUALENVS_CREATE=false

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry && \
    ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /app
COPY . .
RUN poetry install

RUN chown -R spark:spark /app

USER spark

CMD ["poetry", "run", "python", "main.py"]
