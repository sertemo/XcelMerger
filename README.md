# XcelMerger
**Desafío** final de Bootcamp Data Science para **AIPOWER** : 
Limpiar y unificar documentos en una única base de datos
### v0.1.0

![Tests](https://github.com/sertemo/XcelMerger/actions/workflows/tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/sertemo/XcelMerger/branch/develop/graph/badge.svg?token=IV1Z61N298)](https://codecov.io/gh/sertemo/XcelMerger)
![Dependabot](https://img.shields.io/badge/dependabot-enabled-blue.svg?logo=dependabot)
![GitHub](https://img.shields.io/github/license/sertemo/XcelMerger)

---

## Índice

1. [Antecedentes del proyecto](#1-antecedentes-del-proyecto)
2. [Participantes](#2-participantes)
3. [Descripción del reto](#3-descripción-del-reto)
   - [3.1- Objetivo del reto](#31--objetivo-del-reto)
   - [3.2- Criterios de evaluación](#32--criterios-de-evaluación)
4. [Estructura del proyecto](#4-estructura-del-proyecto)
   - [4.1- Arquitectura](#41--arquitectura)
   - [4.2- Estructura de carpetas y archivos](#42--estructura-de-carpetas-y-archivos)
5. [Metodología](#5-metodología)
6. [Unitesting](#6-unittesting)
   - [6.1- CI (Integración continua)](#61--ci-integración-continua)
7. [Despliegue](#7-despliegue)
   - [7.1- Servidor](#71--servidor)
     - [7.1.1- Datos técnicos](#711--datos-técnicos)
     - [7.1.2- Estructura de carpetas](#712--estructura-de-carpetas)
   - [7.2- CD (Despliegue continuo)](#72--cd-despliegue-continuo)
   - [7.3- https y certificado SSL](#73--https-y-certificado-ssl)
   - [7.4- URL](#74--url)
8. [Versiones](#8--versiones)
9. [Tecnologías](#9-tecnologías)
10. [Licencia](#10-licencia)

---

## 1- Antecedentes del proyecto
Tras finalizar el Bootcamp en Data Science de la Cámara de Comercio de Bilbao, ésta nos propuso participar en un desafío o reto (equivalente a un trabajo final de master) con la intención de poner en práctica todos los conocimientos adquiridos.

Carlos, Afonso y yo aceptamos el reto con la condición de realizarlo en equipo. La Cámara de comercio se encargaría de buscarnos un reto.

Tras varias semanas de espera, C2B se puso en contacto con nosotros describiendo las bases del reto que se describen a continuación.

## 2- Participantes
- [Carlos García](https://github.com/cagcruz) - carlosalberto8717@gmail.com
- [Afonso Teixeira](https://github.com/ATS-data) - afonsoteixeirasilva@gmail.com
- Sergio Tejedor - tejedor.moreno@gmail.com

## 3- Descripción del reto
El **11/07/2024** tuvimos la primera toma de contacto mediante videoconferencia con el que será el tutor de nuestro proyecto, [Miguel Ramos](miguel@thegoodriders.com) perteneciente a la empresa [AIPower](http://aipower.ai/).

### 3.1- Objetivo del reto
El objetivo de este reto es desarrollar una solución de data science que permita unificar,
normalizar, limpiar y completar nuestra base de datos de empresas y contactos. Esta
solución debe:
1. **Unificar los Datos**: Integrar todas las fuentes de datos en una única base de
datos centralizada.
2. **Normalización** de Campos: Estandarizar los campos para garantizar la
consistencia de la información.
3. Detección y **Corrección de Errores**: Identificar y corregir datos erróneos,
incluidos nombres de empresas, nombres de contactos, direcciones de correo
electrónico, etc.
4. Detección de **Duplicados**: Implementar mecanismos para detectar registros
duplicados, incluso cuando los nombres estén escritos de forma diferente,
utilizando técnicas avanzadas de deduplicación.
5. **Relleno de Datos Faltantes**: Completar datos obligatorios faltantes como CIF,
correos electrónicos, etc., mediante web scraping de fuentes confiables.

### 3.2- Criterios de evaluación
Exactitud y Precisión: Efectividad en la corrección y normalización de datos.
- **Eficiencia**: Tiempo y recursos utilizados para procesar los datos.
- **Escalabilidad**: Capacidad para manejar grandes volúmenes de datos y nuevas
fuentes de información.
- **Documentación y Reproducibilidad**: Calidad de la documentación y facilidad
para reproducir los resultados.


## 4- Estructura del proyecto
### 4.1- Arquitectura

### 4.2- Estructura de carpetas y archivos
```
XcelMerger/
│
├── common/  # Archivos usados por todos los servicios
│   ├── logging_config.py  # Configuración del logging
│   └── settings.py  # Rutas, constantes y algunos parámetros
│
├── services/  # Aquí estarán todos los servicios. Cada uno es un proyecto independiente
│   ├── auth/
│   │   ├── Dockerfile
│   │   ├── .env  # Variables de entorno y secret keys usadas en auth
│   │   ├── src/  # Código fuente del servicio
│   │   │   ├── __init__.py
│   │   │   └── main.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       └── test_auth.py
│   │
│   └─── frontend/
│        ├── Dockerfile
│        ├── .env  # Variables de entorno y secret keys usadas en frontend
│        ├── src/
│        │   ├── __init__.py
│        │   └── app.py
│        └── tests/
│            ├── __init__.py
│            └── test_frontend.py
│   
│   
│
├── docker-compose.yml
└── pyproject.toml
```

## 5- Metodología

## 6- Unitesting
### 6.1- CI (Integración continua)



## 7- Despliegue
### 7.1- Servidor
#### 7.1.1- Datos técnicos
Para las pruebas de despliegue, se desplegará el proyecto en mi servidor casero. Se trata de un mini ordenador Beelink con las siguientes características:
```sh
Architecture:             x86_64
  CPU op-mode(s):         32-bit, 64-bit
  Address sizes:          39 bits physical, 48 bits virtual
  Byte Order:             Little Endian
CPU(s):                   4
  On-line CPU(s) list:    0-3
Vendor ID:                GenuineIntel
  Model name:             Intel(R) N100
    CPU family:           6
    Model:                190
    Thread(s) per core:   1
    Core(s) per socket:   4
    Socket(s):            1
    Stepping:             0
    CPU(s) scaling MHz:   84%
    CPU max MHz:          3400,0000
    CPU min MHz:          700,0000
```

#### 7.1.2- Estructura de carpetas
Dentro del servidor la estructura de carpetas será la siguiente:

```
XcelMerger/
│
├── common/  # Archivos usados por todos los servicios. Estos archivos son volúmenes usados por los contenedores Docker
│   ├── logging_config.py
│   └── settings.py
│
├── auth/
│   └──.env  # Las variables de entorno y secretos usados por el contenedor
│
├── frontend/
│   └──.env
├── docker-compose.yml
```

El archivo `docker-compose.yml` del servidor difiere ligéramente del archivo que tenemos en local para el desarrollo del proyecto ya que el docker-compose del servidor descarga las imágenes de cada servicio alojadas en el **DockerHub**, no las construye.

`docker-compose.yml`
```yml
services:
  auth:
    image: sertemo/xcelmerger:auth
    env_file:
      - ./auth/.env
    ports:
      - "8000:8000"
    volumes:
      - ./logs:/app/logs
      - ./common:/app/common
    container_name: auth_container
    networks:
      - xm_network
    restart: unless-stopped

  frontend:
    image: sertemo/xcelmerger:frontend
    env_file:
      - ./frontend/.env
    ports:
      - "5050:5050"
    volumes:
      - ./logs:/app/logs
      - ./common:/app/common
    container_name: frontend_container
    networks:
      - xm_network
    restart: unless-stopped

networks:
  xm_network:
    driver: bridge

```

### 7.2- CD (Despliegue continuo)
Se configura un workflow para levantar la red automáticamente en el servidor con cada `push` a la rama `main`.

Los trabajos realizados son:
- login en mi **DockerHub**
- Creación de las imágenes de cada servicio y push al Hub
- Copia de los archivos comunes a la carpeta del proyecto dentro del servidor mediante **SCP**.
- Construcción de los contenedores e inicialización de la red con docker-compose dentro del servidor mediante **SSH**.
- Limpieza de imágenes antiguas.

El archivo que realiza dichas tareas es el siguiente:

`deploy.yml`
```yml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up QEMU
      uses: docker/setup-qemu-action@v3

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Login to DockerHub 
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_PASSWORD }}

    - name: Build and push auth image
      uses: docker/build-push-action@v5
      with:
        context: ./services/auth
        push: true
        tags: ${{ secrets.DOCKERHUB_USERNAME }}/xcelmerger:auth

    - name: Build and push frontend image
      uses: docker/build-push-action@v5
      with:
        context: ./services/frontend
        push: true
        tags: ${{ secrets.DOCKERHUB_USERNAME }}/xcelmerger:frontend

    - name: Copy common folder to server
      uses: appleboy/scp-action@v0.1.7
      with:
        host: ${{ secrets.SERVER_SSH_HOST }}
        username: ${{ secrets.SERVER_SSH_USER }}
        password: ${{ secrets.SERVER_SSH_KEY }}
        port: ${{ secrets.SERVER_SSH_PORT }}
        source: "common/*"
        target: "${{ secrets.SERVER_PROJECT_PATH }}"
        debug: true

    - name: Deploy to server
      uses: appleboy/ssh-action@v1.0.3
      with:
        host: ${{ secrets.SERVER_SSH_HOST }}
        username: ${{ secrets.SERVER_SSH_USER }}
        password: ${{ secrets.SERVER_SSH_KEY }}
        port: ${{ secrets.SERVER_SSH_PORT }}
        script: |
          source ~/.bashrc  # Para que las rutas estén en el path
          cd ${{ secrets.SERVER_PROJECT_PATH }}
          /usr/libexec/docker/cli-plugins/docker-compose pull
          /usr/libexec/docker/cli-plugins/docker-compose up -d

    - name: Cleanup old images
      uses: appleboy/ssh-action@v1.0.3
      with:
        host: ${{ secrets.SERVER_SSH_HOST }}
        username: ${{ secrets.SERVER_SSH_USER }}
        password: ${{ secrets.SERVER_SSH_KEY }}
        port: ${{ secrets.SERVER_SSH_PORT }}
        script: |
          docker image prune -f
```


### 7.3- https y certificado SSL
Se describirán los pasos realizados para obtener un certificado SSL renovable automáticamente de cara a utilizar el protocolo https.

### 7.4- URL
La URL para las pruebas es [esta](http://trymlmodels.com:5050).

## 8- Versiones
- 0.1.0: versión inicial del proyecto

## 9- Tecnologías
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Poetry](https://img.shields.io/badge/Poetry-60A5FA?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23F7DF1E.svg?style=for-the-badge&logo=javascript&logoColor=black)


## 10- Licencia
Copyright 2024 Carlos García, Afonso Teixeira, Sergio Tejedor

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

