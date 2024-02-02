FROM postgres:13
COPY ./selteq_task.sql /docker-entrypoint-initdb.d/selteq_task.sql
CMD ["docker-entrypoint.sh", "postgres"]
