FROM  postgres:12

COPY 010.rates.sql /docker-entrypoint-initdb.d/
COPY 015.dummy_latvian_data.sql /docker-entrypoint-initdb.d/
COPY 020.region_tree_and_points.sql /docker-entrypoint-initdb.d/

ENV POSTGRES_PASSWORD=ratestask
