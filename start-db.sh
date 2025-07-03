#!/bin/bash

podman run -d --rm --name tododb \
  -e POSTGRESQL_USER=todouser \
  -e POSTGRESQL_PASSWORD=todopassword \
  -e POSTGRESQL_ADMIN_PASSWORD=adminpassword \
  -e POSTGRESQL_DATABASE=todos \
  -v "$(pwd)/db-data":/var/lib/pgsql/data \
  -p 5432:5432 \
  registry.redhat.io/rhel9/postgresql-16:9.6-1751360823
