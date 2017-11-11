# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import os
import re
@auth.requires_membership('Representante_liceo')
@auth.requires_login()
def index():
    T.force('es')
    username = auth.user.username
    representante_liceo=db(db.representante_liceo.ci==username).select().first()
    usuario = db(db.usuario.username==username).select().first()

    formDatosBasicos = SQLFORM.factory(
        Field('first_name' +  'last_name',
            type='string',
            default=usuario.first_name + " " + usuario.last_name,
            requires=db.usuario.first_name.requires and db.usuario.last_name.requires,
            label='nombre'
            ),
        Field('username',
            type='string',
            notnull = True,
            default=usuario.username,
            requires=db.usuario.username.requires,
            label='ci'
            ),
        Field('email',
            type='string',
            default=usuario.email,
            requires=db.usuario.email.requires,
            label='email'),
        readonly = True
        )

    if formDatosBasicos.process(session=None, formname='perfil basico del Representante liceo de sede', keepvalues=True).accepted:
        response.flash = 'El formulario fue aceptado exitosamente.'

    elif formDatosBasicos.errors:
        response.flash = 'Hay un error en un campo.'

    formRepresentanteLiceo = SQLFORM.factory(
        Field('ci',
            type='string',
            notnull=True,
            default=representante_liceo.ci,
            requires=db.representante_liceo.ci.requires,
            label='ci'
            ),
        Field('first_name' +  'last_name',
            type='string',
            default=usuario.first_name + " " + usuario.last_name,
            requires=db.usuario.first_name.requires and db.usuario.last_name.requires,
            label='nombre'
            ),
        Field('nombre_liceo',
            type='string',
            default=representante_liceo.nombre_liceo,
            requires=db.representante_liceo.nombre_liceo.requires,
            label='nombre_liceo'
            ),
        Field('email',
            type='date',
            default=usuario.email,
            requires=db.usuario.email.requires,
            label='email'),
        readonly = True
        )

    if formRepresentanteLiceo.process(session=None, formname='perfil del Representante Liceo de sede', keepvalues=True).accepted:
        response.flash = 'El formulario fue aceptado exitosamente.'

    elif formRepresentanteLiceo.errors:
        response.flash = 'Hay un error en un campo.'
    return dict(formRepresentanteLiceo=formRepresentanteLiceo,
                formDatosBasicos=formDatosBasicos)

@auth.requires_membership('Representante_liceo')
@auth.requires_login()
def cargarArchivo():
    erroresCarga = [] # Los errores en la carga van aqui
    cargaExitosa = [] # Los usuarios agregados exitosamente van aqui
    cohorte = db(db.cohorte.status=="Activa").select()[0].identificador # Cohorte Actual
    liceo = db(db.representante_liceo.ci == auth.user.username).select()[0].nombre_liceo # Liceo al que pertenece el representante logiado

    formularioArchivo = FORM(
                            INPUT(_name='tituloArchivo', _type='text'),
                            INPUT(_name='archivo', _type='file')
                            )
    if formularioArchivo.accepts(request.vars,formname='formularioArchivo'): # Chequeamos si hay un archivo cargado
        archivo =request.vars.fileToUpload.filename.split(".")  # Separamos el nombre del archivo de la extension
        nombreArchivo, extension = archivo[0], archivo[1]
        if extension == "csv":          # Chequeamos la extension del archivo
            ######################
            # Cargando Estudiantes
            ######################
            f = request.vars.fileToUpload.file      # Archivo cargado
            texto = f.read().splitlines()           # Leer el archivo
            cabecera = texto[0].split(";")          # Extraemos la cabecera
            chequeoFormato = texto[1].split(";")    # Extraemos la segunda linea del archivo
            texto.remove(texto[1])                  # Eliminamos la segunda linea del archivo para no iterar sobre ella
            texto.remove(texto[0])                  # Eliminamos del texto la cabecera para no iterar sobre ella
            if (cabecera[0]=="C.I." and cabecera[1]=='Nombres' and
                cabecera[2]=='Apellidos' and cabecera[3]=='Promedio (00.00)' and
                chequeoFormato[0]=="A continuacion coloque sus estudiantes con el formato indicado"): # Verificamos que la cabecera tenga el formato correcto
                datos = []                          # Los usuarios a agregar van aqui
                for i in texto:
                    if i != ";;;;":
                        dato = i.split(";")         # Separamos los datos del usuario
                        datos.append(dato)          # Agregamos el usuario a la lista de usuarios por agregar

                for i in datos:
                    if (not(db(db.usuario.username == i[0]).select()) and
                       not(db(db.estudiante.ci == i[0]).select())):         # Verificar que no existe un usuario para esa cedula
                        if 0 <= float(i[3]) <= 20:                          # Verificamos que el indice sea correcto
                            if db(db.liceo.nombre == liceo).select():       # Verificamos que el liceo este en la base de datos
                                if re.match('^[0-9]{1,8}$', i[0]):      # Verificamos que la cedula cumpla la expresion regular
                                    id = db.usuario.insert(first_name = i[1],last_name = i[2], email = "", username = i[0],
                                                  password = db.usuario.password.validate(i[0])[0], registration_key = "",
                                                  reset_password_key = "", registration_id = "" )       # Agregar el usuario
                                    db.auth_membership.insert(user_id = id, group_id= 1)                # Agregar permisos de estudiante (group_id=1)
                                    db.estudiante.insert(nombre=i[1], apellido=i[2], ci=i[0], promedio=float(i[3]), direccion="", telefono_habitacion="",
                                                    telefono_otro="", fecha_nacimiento="", sexo="", estatus="Pre-inscrito",
                                                    cohorte=cohorte, ci_representante="", nombre_representante="",
                                                    apellido_representante="", sexo_representante="", correo_representante="",
                                                    direccion_representante="", nombre_liceo=liceo, telefono_representante_oficina="",
                                                    telefono_representante_otro="", sufre_enfermedad="", enfermedad="",
                                                    indicaciones_enfermedad="")     # Agregamos el estudiante Cohorte deberia ser una variable global
                                    cargaExitosa.append(i)                          # Agregarlo a los estudiantes cargados exitosamente
                                else:
                                    erroresCarga.append([i,"Cedula incorrecta"])  # Error de Carga
                            else:
                                erroresCarga.append([i,"Su liceo no esta en la base de datos. Contacte al administrador"])  # Error de Carga
                        else:
                            erroresCarga.append([i,"El promedio debe ser un numero entre 0 y 20"])                          # Error de Carga
                    else:
                        erroresCarga.append([i,"Ya existe un usuario en el sistema con esta cedula"])                       # Error de Carga

            else: #Error
                erroresCarga.append("Formato de los datos del archivo invalido. Consulte el manual")                        # Error de Carga

        else: #Error
            erroresCarga.append("El formato del archivo debe ser \".csv\". Consulte el manual de usuario")
    else:
        pass
    return dict(erroresCarga=erroresCarga, cargaExitosa=cargaExitosa)
