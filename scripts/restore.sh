#!/usr/bin/env sh
# Example restore — **destructive**; test on staging first.
set -eu
# PGPASSWORD="$POSTGRES_PASSWORD" psql -h localhost -U "$POSTGRES_USER" "$POSTGRES_DB" < backup.sql
