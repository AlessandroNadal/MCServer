# SRC - Código del servidor

Dentro de este directorio se encontrarán todos los archivos, clases, metodos y constantes del servidor.<br>

## ¿Cómo funciona?

El entrypoint del proyecto es [main.py](https://github.com/AlessandroNadal/MCServer/blob/main/main.py) que se encuentra en el directorio principal, este solo llama al método [start()](https://github.com/AlessandroNadal/MCServer/blob/main/src/serverprocess.py#L75) de [serverprocess.py](https://github.com/AlessandroNadal/MCServer/blob/main/src/serverprocess.py)<br>

### [serverprocess](https://github.com/AlessandroNadal/MCServer/blob/main/src/serverprocess.py)
[serverprocess](https://github.com/AlessandroNadal/MCServer/blob/main/src/serverprocess.py) contiene 2 clases, [ServerFactory](https://github.com/AlessandroNadal/MCServer/blob/main/src/serverprocess.py#L67) que es el proceso principal del servidor que irá creando un [ServerProcess](https://github.com/AlessandroNadal/MCServer/blob/main/src/serverprocess.py#L34)
por cada jugador, más explicado en ServerProcess

#### ServerProcess
ServerProcess es el encargado como mencionado anteriormente de manejar todas las peticiones del usuario espécifico de
ese proceso.

Este se caracteriza por tener un atributo de tipo [Stage](stages/stage.py),
esta clase se encarga de manejar las peticiones dentro de cada estado del jugador, explicado a detalle en [src/stages/](stages/)