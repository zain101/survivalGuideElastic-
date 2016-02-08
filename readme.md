#run migrations using old fashion
`
python manage.py syncdb

python manage.py migrate


python manage.py makemigrations
`

#Create a super user
###Add notes from admin panel

#Basic app for making list to events to attend i;e event list
##http://localhost:8000/talks/lists/   for list-view


#Note taking app

##http://localhost:8000/talks/lists/search

##http://localhost:8000/talks/lists/search_auto_temp

Refer to haystack [Docs](http://django-haystack.readthedocs.org/en/v2.4.1/)