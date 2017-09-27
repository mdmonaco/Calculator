# Calculadora

Calculadora simple con las siguientes funcionalidades:

							suma, 
							resta,  
							multiplicación, 
							división, 
							logaritmo con números de punto flotante.
							Ejemplo: (2+2)*log 10/3

	*** PARA EL CALCULO DE LOG 10/3 EL PARAMETRO DEBE SER PASADO DE LA SIGUIENTE MANERA log(10,3) ***

Persiste una sesión de cálculo.
Recupera una sesión de cálculo almacenada.

Ejemplo:
input: 2+2
output: 4
input: 5*3*(8-23)
output: -225
input: guardar sesion1
output: sesion1 almacenada
input: recuperar sesion1
output: 2+2
= 4
	5*3*(8-23)
     	= -225

## Getting Started

Instalar para python, Flask(microfram)

http://flask.pocoo.org/docs/0.12/installation/


Es necesario tener pip instalado

https://pip.pypa.io/en/stable/installing/



## Getting Started deploy

1. Crear un archivo .db llamado "database" en la carpeta "data"

2. Ejecutar por unica vez base
		
		python base.py

3. Ejecutar el programa "calculator.py"

		python calculator.py

4. Desde cuaquier navegador, ingresar a la url:

		http://localhost:5000/

## Authors

* **Mario Monaco** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)
