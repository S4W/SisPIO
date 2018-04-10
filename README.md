# [SisPIO](http://syspio.dex.usb.ve "Conoce SisPIO")
*Sistema de Gestión para la Coordinación de Igualdad de Oportunidades (CIO) de la Universidad Simon Bolivar.*

## Desarrolladores:

- Software for the World (S4W)
  + Miguel Canedo
  + Maria Bracamonte
  + Rafael Cisneros
  + Carlos Perez
  + Andres Buelvas
  + Jose Donato Bracuto


## Requerimientos del Sistema:
   + PostgreSQL 9.X
   + Python v2.7.x o superior.
   + Libreia "psycopg2".

## Pasos para la instalación:
- Descargar Web2Py. Puede descargarlo mediante este [link](http://www.web2py.com/init/default/download "Descargar web2py").
- Extraer la carpeta contenida en el comprimido de web2py en su home.
- Abrir una terminal.
- Clonar el repositorio de SisPIO.
```bash
git clone https://github.com/S4W/SisPIO SisPIO
```
- Mover la carpeta "SisPIO" al directorio "web2py/applications/".
```bash
mv SisPIO web2py/applications/
```
- Ingresar al directorio "web2py/applications/SisPIO/", dar permisos para ejecutar el script de instalación de la Base de Datos y ejecutarlo.
```bash
cd web2py/applications/SisPIO/
sudo chmod 777 dbinstall.sh
sudo ./dbinstall.sh
```
- Ingresar "SisPIO" cuando solicite la contraseña para crear el nuevo role.

### Para añadir más tipos de estudiantes
En la carpeta `private` se encuentra un archivo llamado `appconfig.ini`.
Este archivo se compone en secciones denotadas con `[seccion]` y atributos
debajo de estas secciones.

Si se desean añadir o remover tipos de estudiantes, simplemente
debe añadirse estos tipos, sin comillas, separados por comas, sin espacios entre
separadores, así como se visualiza en el siguiente ejemplo:

- Antes de añadir nuevos tipos de ingreso.
```ini
; Tipos de ingreso para los estudiantes
[ingreso]
tipos_ingreso = Prueba interna,Admisión directa
```

- Luego de añadir nuevos tipos de ingreso.
```ini
; Tipos de ingreso para los estudiantes
[ingreso]
tipos_ingreso = Prueba interna,Admisión directa,Admisión indirecta
```
