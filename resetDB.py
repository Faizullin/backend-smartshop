import os
os.system('find . -path "*/migrations/*.py" -not -name "__init__.py" -delete')
os.system('find . -path "*/migrations/*.pyc"  -delete')
os.system('python3 manage.py makemigrations')
os.system('python3 manage.py migrate')

