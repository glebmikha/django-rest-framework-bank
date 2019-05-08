make_migr:
	docker-compose run --rm web sh -c "python manage.py makemigrations sites"
migr:
	docker-compose run --rm web sh -c "python manage.py migrate"
test:
	docker-compose run --rm web sh -c "python manage.py test -v 2"
super:
	docker-compose run --rm web sh -c "python manage.py createsuperuser"