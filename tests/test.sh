#!/bin/bash

export POSTGRES_HOST=127.0.0.1
export POSTGRES_PORT=5432
export POSTGRES_USER=test
export POSTGRES_PASSWORD=test
export POSTGRES_DB=postgres
export SECRET_KEY=4o7wrqsup*pc*m_etd$mu$8klfl2r$l1_073a+-j_tkvq9a+b7
python3 manage.py test $1