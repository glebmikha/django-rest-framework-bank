make_migr:
	docker-compose run --rm web sh -c "python manage.py makemigrations bank"
migr:
	docker-compose run --rm web sh -c "python manage.py migrate"
test:
	docker-compose run --rm web sh -c "python manage.py test"
super:
	docker-compose run --rm web sh -c "python manage.py createsuperuser"
ssh_w:
	docker-compose exec web sh