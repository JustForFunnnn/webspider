#!/bin/sh

export MYSQL_USERNAME="${MYSQL_USERNAME:=root}"
export MYSQL_PASSWORD="${MYSQL_PASSWORD:=}"
export MYSQL_HOST="${MYSQL_HOST:=localhost}"
export MYSQL_DATABASE="${MYSQL_DATABASE:=test}"

echo 'Running unittest.......'
env/bin/nosetests -vsd --with-coverage --cover-package=app
