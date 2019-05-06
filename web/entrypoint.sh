#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "run migrations and static"
python manage.py migrate

if [ "$DEBUG" = "FASLE" ] 
then
	 python manage.py collectstatic --no-input
fi

exec "$@"