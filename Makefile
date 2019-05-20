make_migr:
	docker-compose run --rm web sh -c "python manage.py makemigrations bank"
migr:
	docker-compose run --rm web sh -c "python manage.py migrate"
test:
	docker-compose run --rm web sh -c "python manage.py test"
super:
	docker-compose run --rm web sh -c "python manage.py createsuperuser"
shell:
	docker-compose run --rm web sh -c "python manage.py shell"
ssh_w:
	docker-compose exec web sh
test_prod:
	docker-compose -f docker-compose.prod.yml run --rm web sh -c "python manage.py test"