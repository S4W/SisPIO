# [SisPIO](syspio.dex.usb.ve "Conoce SisPIO")
*Sistema de Gestión para la Coordinación de Igualdad de Oportunidades (CIO) de la Universidad Simon Bolivar.*

## Pasos para la instalación:
- Descargar e Instalar PostgreSQL 9.X
- Iniciar sesión como usuario postgres y crear la BD SisPIO:
```
sudo -su postgres
psql
CREATE DATABASE "SisPIO";
```
- Crear usuario SisPIO y garantarizar el acceso a la BD:
```
CREATE USER "SisPIO" WITH PASSWORD 'SisPIO';
GRANT ALL PRIVILEGES ON DATABASE "SisPIO" to "SisPIO";
```
- Y a trabajar.
