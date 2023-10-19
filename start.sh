#!/bin/bash

# Start tailwind
python manage.py tailwind start &

# Start Django server
python manage.py runserver 0.0.0.0:8000