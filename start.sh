#!/bin/bash
# Запуск фоновых процессов
python3 djnagoPRC/djangoRPC/manage.py runserver 0.0.0.0:8080 &
python3 djnagoPRC/djangoRPC/manage.py grpcserver &
# Ожидание завершения всех процессов (опционально)
wait
