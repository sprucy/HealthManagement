del healthmanage/migrations/00*.py
del db.sqlite3

python manage.py makemigrations healthmanage
python manage.py migrate