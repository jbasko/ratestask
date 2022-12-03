FROM  postgres:12

COPY db-setup/010.rates.sql /docker-entrypoint-initdb.d/
COPY db-setup/020.region_tree_and_points.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
ENV POSTGRES_PASSWORD=ratestask
