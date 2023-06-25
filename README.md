# Obligatorio Machine Learning en Produccion

## Configuración de Ambiente

- Instalar [Git](https://git-scm.com/)
- Instalar [DVC](https://dvc.org/doc/install)
    - Windows: ```choco install dvc```
    - Mac: ```brew install dvc```
- Se puede correr la aplicacion mediante el siguiente comando:
    - ```uvicorn main:app --reload```
    - Para generar una nueva clave usar ```openssl rand -hex 32```

Para correr el Docker usar:
- ```docker build -t fastapi .```
- ```docker run -d -p 8000:8000 fastapi```