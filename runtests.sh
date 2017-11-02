#!/bin/sh

#
while echo $1 | grep ^- > /dev/null; do
    declare $( echo $1 | sed 's/-//g' | sed 's/=.*//g' | tr -d '\012')=$( echo $1 | sed 's/.*=//g' | tr -d '\012');
    shift;
done


export MYSQL_USERNAME="${MYSQL_USERNAME:=root}"
export MYSQL_PASSWORD="${MYSQL_PASSWORD:=}"
export MYSQL_HOST="${MYSQL_HOST:=localhost}"
export MYSQL_DATABASE="${MYSQL_DATABASE:=test}"

echo $test-path

echo 'Running unittest......'
env/bin/nosetests $path -vd --with-coverage --cover-package=app
