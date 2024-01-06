#!/bin/bash

podman run -d --rm --name tododb \
  -e POSTGRESQL_USER=todouser \
  -e POSTGRESQL_PASSWORD=todopassword \
  -e POSTGRESQL_DATABASE=todos \
  -p 5432:5432 \
  registry.redhat.io/rhel9/postgresql-15@sha256:802c7926383f9e4b31ac48dd42e5b7cce920c8ef09920abe2724e50a84fbea0b
