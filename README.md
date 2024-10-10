# Relif-Test
Repositorio para la entrega de la prueba tecnica de Relif de Emilio Arias Zuñiga


# Instrucciones de ejecucion
pip install requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

# Ruta base
localhost:8000/clients

# Generacion del prompt
Se uso OpenAi, en la cual se le asignaron distintas frases como prompt para el modelo, de esta forma el modelo es capaz de rellenar las oraciones con distintas palabras ademas de indicarle que es un asistente de ventas por lo que intentara vender distintos modelos de autos.

# Deploy
El codigo se encuentra adicionalmente en heroku por lo que para el testeo hacia la plataforma se usa el siguiente link: https://relif-test-5795fa68bfb5.herokuapp.com/clients

