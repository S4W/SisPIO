## SistemaPIO
# Pasos para la isntalacion:
- Descargar e Instalar PostgreSQL 9.X
- Iniciar sesion como usuario postgres y crear la BD SisPIO:
```
sudo -su postgres
CREATE DATABASE "SisPIO";
```
- Creat usuario SisPIO y garantarizar el acceso a la BD:
```
CREATE USER "SisPIO" WITH PASSWORD "SisPIO";
GRANT ALL PRIVILEGES ON DATABASE "SisPIO" to "SisPIO";
```
- Y a trabajar :D
