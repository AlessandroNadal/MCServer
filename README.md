# PuigCraft

Implementación del protocolo de Minecraft en Python
![Lobby header](https://www.cubecraft.net/attachments/minecraft-screenshot-2020-07-28-17-26-41-71-png.172335/)

## Documentación

La documentación estará dividida entre los diferentes paquetes que haya en el proyecto.
En el README que estás leyendo ahora contiene información general sobre el proyecto,
a medida que vayas entrando en subdirectorios habrá un nuevo README dedicado a esa parte del proyecto
en [src/](https://github.com/AlessandroNadal/MCServer/tree/main/src) se encontrará documentación con el código
y en [src/stages/](https://github.com/AlessandroNadal/MCServer/tree/main/src/stages) la lógica de como funciona el
código

## Instalación

Linux (Debian)

```bash
git clone https://github.com/AlessandroNadal/MCServer.git
cd MCServer

sudo apt install python3-venv
sudo apt install python3-pip

python3 -m venv .venv
source .venv/bin/activate

python3 -m pip install -r requirements.txt
```

## Despliegue

```bash
python3 main.py
```
