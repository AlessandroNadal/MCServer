# PuigCraft
![Lobby header](https://www.cubecraft.net/attachments/minecraft-screenshot-2020-07-28-17-26-41-71-png.172335/)

PuigCraft es una implementación parcial del protocolo de Minecraft Java Edition desarrollada en Python. El proyecto tiene como objetivo recrear el funcionamiento interno de un servidor de Minecraft, gestionando directamente la comunicación entre clientes y servidor mediante sockets TCP, procesamiento de paquetes y control de estados del protocolo.

El servidor utiliza una arquitectura modular basada en procesos y estados. Cada jugador conectado es gestionado mediante un `ServerProcess` independiente, mientras que el comportamiento de la conexión se controla a través de un sistema de `Stage`, encargado de manejar las distintas fases del protocolo como handshake, status, login o play.

El proyecto está orientado principalmente al aprendizaje y experimentación con:
- Protocolos de red
- Arquitectura cliente-servidor
- Programación asíncrona
- Procesamiento de paquetes binarios
- Concurrencia y gestión de conexiones
- Funcionamiento interno de Minecraft Java Edition

---

# Características

- Implementación del protocolo de Minecraft Java Edition
- Gestión concurrente de múltiples clientes
- Arquitectura modular basada en estados
- Programación asíncrona utilizando Twisted
- Serialización y deserialización de paquetes binarios
- Sistema preparado para ampliar nuevos paquetes y funcionalidades
- Documentación distribuida por módulos y directorios

---

# Arquitectura general

```text
Cliente Minecraft
        │
        ▼
ServerFactory
        │
        ├── ServerProcess (Jugador 1)
        │           │
        │           └── Stage actual
        │
        ├── ServerProcess (Jugador 2)
        │           │
        │           └── Stage actual
        │
        └── ...
```

- `main.py`  
  Punto de entrada principal del proyecto.

- `ServerFactory`  
  Responsable de aceptar nuevas conexiones y crear un proceso independiente por jugador.

- `ServerProcess`  
  Gestiona toda la comunicación de un cliente concreto.

- `Stage`  
  Controla el comportamiento del servidor según el estado actual de la conexión.

---

# Estructura del proyecto

```text
MCServer/
├── main.py
├── requirements.txt
├── src/
│   ├── serverprocess/
│   ├── stages/
│   ├── packets/
│   ├── utils/
│   └── ...
└── README.md
```

## Directorios principales

### `src/`
Contiene todo el código fuente del servidor.

### `src/stages/`
Implementación de los distintos estados del protocolo y la lógica asociada a cada fase de conexión.

### `src/serverprocess/`
Gestión de conexiones individuales y procesos asociados a cada jugador.

### `src/packets/`
Definición y procesamiento de paquetes enviados y recibidos.

### `src/utils/`
Funciones auxiliares y herramientas utilizadas por el resto del sistema.

---

# Tecnologías utilizadas

- Python 3
- Twisted
- struct
- TCP Sockets

---

# Instalación

## Linux (Debian/Ubuntu)

```bash
git clone https://github.com/AlessandroNadal/MCServer.git
cd MCServer

sudo apt install python3-venv
sudo apt install python3-pip

python3 -m venv .venv
source .venv/bin/activate

python3 -m pip install -r requirements.txt
```

---

# Ejecución

```bash
python3 main.py
```

---

# Documentación

La documentación del proyecto está distribuida entre los distintos directorios del repositorio.

- El README principal contiene información general del proyecto.
- Algunos subdirectorios incluyen documentación específica sobre sus componentes.
- En `src/` se encuentra documentación relacionada con el código y la arquitectura interna.
- En `src/stages/` se documenta el funcionamiento del sistema de estados y el flujo del protocolo.

---

# Objetivos del proyecto

Este proyecto nace con fines educativos y de investigación técnica, buscando comprender en profundidad cómo funciona el protocolo de Minecraft Java Edition y cómo se implementa un servidor multijugador desde bajo nivel.

Entre los principales objetivos se encuentran:
- Comprender protocolos de red complejos
- Trabajar con programación asíncrona
- Diseñar una arquitectura modular y escalable
- Gestionar conexiones concurrentes
- Manipular datos binarios directamente

---

# Estado del proyecto

El proyecto se encuentra en desarrollo activo y algunas partes del protocolo todavía no están completamente implementadas.

---

# Bibliografía y referencias

- Minecraft Java Edition Protocol  
  https://minecraft.wiki/w/Java_Edition_protocol

- Twisted Documentation  
  https://twisted.org/

- Python struct Documentation  
  https://docs.python.org/3/library/struct.html
