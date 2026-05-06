#!/usr/bin/env sh
# Example pg_dump — requires network access to Postgres and credentials in the environment.
set -eu
# PGPASSWORD="$POSTGRES_PASSWORD" pg_dump -h localhost -U "$POSTGRES_USER" "$POSTGRES_DB" > backup.sql
