### Ver el md en modo grafico
Usar el built-in preview con Ctrl+Shift+V

# Crear venv para el proyecto
Ir a la carpeta del proyecto y a continuación crear el entorno, para este ejemplo fastapi-mysql
```
python -m venv fastapi-mysql     
```

# Activar el entorno venv
```
fastapi-mysql\Scripts\activate
```

# Instalar fastapi y uvicorn
```
pip install fastapi uvicorn
```

# Instalar sqlalchemy - ORM para conexión a base de datos
```
pip install sqlalchemy
```

# Instalar pymysql - conexión hacia MySQL o MariaDB
```
pip install pymysql
```

# Instalar autopep8 para formatear el documento
```
pip install autopep8
```

# Instalar cryptography para cifrar la contraseña
```
pip install cryptography
```

# Ejecutar el servidor con autorefresh
uvicorn app:app --reload

## Si queremos enviar nuestra API hacia Lambda, debemos instalar mangum
```
pip install mangum
```

# Crear el requirements.txt
```
pip freeze > requirements.txt
```

# Para poder ejecutar en lambda
```
pip install -r requirements.txt --target=dependencies/ --platform manylinux2014_x86_64 --implementation cp --python-version 3.12 --only-binary=:all: --upgrade
```

# Crear un zip de main.py y los contenidos de las carpetas claves models, routes, schemas y dependencias
```
Compress-Archive -Path @('.\app.py', '.\config', '.\routes', '.\models', '.\schemas', '.\dependencies\*') -DestinationPath .\aws_lambda_artifact.zip -Force
```

# Crear la funcion lambda en AWS y cargar nuestro aws_lambda_artifact.zip
Luego cambiar el handler, le damos edit a runtime settings, cambiaremos el lambda_function.lambda_handler a app.handler (dado que el app está en app.py y el mangum lo llamamos con la variable handler)

```
app.handler
```

# Para configurar git, se deben establecer el user.name y user.email previo a hacer commit
```
git config --global user.name "Marco Meza"
git config --global user.email "maco@guatesuper.com"
```