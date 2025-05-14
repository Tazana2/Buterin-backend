#!/bin/sh

pip install -r requirements.txt

cd backend/

# Ejecutar el script que trae los NFTs
echo "Fetching NFTs..."
python get_nfts.py

# Poblamos la base de datos
echo "Populating database..."
python populate_db_nfts.py

# Ejecutamos migraciones por si acaso
echo "Applying migrations..."
python manage.py makemigrations
python manage.py migrate

# Finalmente, arrancamos el servidor
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
