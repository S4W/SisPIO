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
@auth.requires_membership('Administrador')
@auth.requires_login()
def index():

    ########################
    ###Consula de datos
    ########################
    T.force('es')
    username = auth.user.username
    usuario = db(db.usuario.username==username).select().first()

    formAdministrador = SQLFORM.factory(
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

    if formAdministrador.process(session=None, formname='perfil del administrador', keepvalues=True).accepted:
        response.flash = 'El formulario fue aceptado exitosamente.'

    elif formAdministrador.errors:
        #error = True
        response.flash = 'Hay un error en un campo.'
    ############################
    ###fin de Consula de datos
    ############################

    return dict(formAdministrador=formAdministrador)

@auth.requires_membership('Administrador')
@auth.requires_login()
def agregarManual():
    #################
    # Agregar Manualmente Estudiante
    #################


    formularioAgregarManual = FORM()
    cohorte = db(db.cohorte.status=="Activa").select()[0].identificador # Cohorte Actual

    #SI ha pasado correctamente el formulario
    if formularioAgregarManual.accepts(request.vars,formname="formularioAgregarManual"):
        if request.vars.tipoUsuario == "estudiante":
            if (not(db(db.usuario.username == request.vars.cedula).select()) and not(db(db.estudiante.ci == request.vars.cedula).select())):
                if 0 <= int(request.vars.PromedioEntero) + float(request.vars.PromedioDecimal)/100 <= 20:
                    if db(db.liceo.nombre == request.vars.liceo).select():
                        if re.match('^[0-9]{1,8}$', request.vars.cedula):
                            usuario_nuevo = db.usuario.insert(
                                            username=request.vars.cedula,
                                            first_name=request.vars.nombres,
                                            last_name=request.vars.apellidos,
                                            email="",
                                            password=db.usuario.password.validate(request.vars.cedula)[0],
                                            registration_key = "",
                                            reset_password_key = "",
                                            registration_id = ""
                            )
                            db.auth_membership.insert(user_id = usuario_nuevo, group_id= 1) # Agregar permisos de estudiante

                            db.estudiante.insert(
                                            ci=request.vars.cedula,
                                            promedio=int(request.vars.PromedioEntero) + float(request.vars.PromedioDecimal)/100,
                                            direccion="",
                                            telefono_habitacion="",
                                            telefono_otro="",
                                            fecha_nacimiento="",
                                            sexo="",
                                            estatus="Pre-inscrito",
                                            cohorte=cohorte,
                                            ci_representante="",
                                            nombre_representante="",
                                            apellido_representante="",
                                            sexo_representante="",
                                            correo_representante="",
                                            direccion_representante="",
                                            nombre_liceo=request.vars.liceo,
                                            telefono_representante_oficina="",
                                            telefono_representante_otro="",
                                            sufre_enfermedad="",
                                            enfermedad="",
                                            indicaciones_enfermedad="")

                            response.flash = "Estudiante agregado exitosamente"
                        else:
                            response.flash = "El formato de la cedula no es el correcto"
                    else:
                        response.flash = "El liceo no se encuentra en la base de datos"
                else:
                    response.flash = "El promedio debe ser un valor comprendido entre 0 y 20"
            else:
                response.flash = "Ya existe un usuario con esa cédula"

    #######################
    # Agregar representante de liceo manualmente
    #######################

        elif request.vars.tipoUsuario == "representanteLiceo":
            if (not(db(db.usuario.username == request.vars.cedula).select()) and not(db(db.representante_liceo.ci == request.vars.cedula).select())):
                if db(db.liceo.nombre == request.vars.liceo).select():                # Verificamos que el liceo este en la base de datos
                    if re.match('^[0-9]{1,8}$', request.vars.cedula):
                        id = db.usuario.insert(first_name = request.vars.nombres ,
                                               last_name = request.vars.apellidos,
                                               email = "",
                                               username = request.vars.cedula,
                                               password = db.usuario.password.validate(request.vars.cedula)[0],
                                               registration_key = "",
                                               reset_password_key = "",
                                               registration_id = "" ) # Agregar el usuario

                        db.auth_membership.insert(user_id = id, group_id=3) # Agregar permisos de representante liceo (group_id=3)

                        db.representante_liceo.insert(ci=request.vars.cedula,
                                                      nombre_liceo=request.vars.liceo) # Agregar el representante de liceo
                        response.flash = "Representante del liceo agregado exitosamente"
                    else:
                        response.flash = "El formato de la cedula no es el correcto"
                else:
                    response.flash = "El liceo no se encuentra en la base de datos"
            else:
                response.flash = "Ya existe un usuario con esa cédula"

    #######################
    # Agregar representante de sede manualmente
    #######################

        elif request.vars.tipoUsuario == "representanteSede":
            if (not(db(db.usuario.username == request.vars.cedula).select()) and not(db(db.representante_sede.ci == request.vars.cedula).select())):
                if request.vars.sede=="Sartenejas" or request.vars.sede=="Litoral" or request.vars.sede=="Higuerote" or request.vars.sede=="Guarenas":
                    if re.match('^[0-9]{1,8}$', request.vars.cedula):
                        representante_nuevo = db.usuario.insert(first_name = request.vars.nombres,
                                                                last_name = request.vars.apellidos,
                                                                email = "",
                                                                username = request.vars.cedula,
                                                                password = db.usuario.password.validate(request.vars.cedula)[0],
                                                                registration_key = "",
                                                                reset_password_key = "",
                                                                registration_id = "" ) # Agregar el usuario

                        db.auth_membership.insert(user_id = representante_nuevo, group_id=4) # Agregar permisos de representante sede (group_id=4)

                        db.representante_sede.insert(ci=request.vars.cedula,
                                                    sede=request.vars.sede) # Agregar el representante de sede
                        response.flash = "Representante de sede agregado exitosamente"
                    else:
                        response.flash = "El formato de la cedula no es el correcto"
                else:
                    response.flash = "La sede no se encuentra en la base de datos"
            else:
                response.flash = "Ya existe un usuario con esa cédula"


    #######################
    # Agregar profesor manualmente
    #######################

        elif request.vars.tipoUsuario == "profesor":
            if (not(db(db.usuario.username == request.vars.cedula).select())):
                if re.match('^[0-9]{1,8}$', request.vars.cedula):
                    id = db.usuario.insert(first_name = request.vars.nombres,
                                                    last_name = request.vars.apellidos,
                                                    email = "",
                                                    username = request.vars.cedula,
                                                    password = db.usuario.password.validate(request.vars.cedula)[0],
                                                    registration_key = "",
                                                    reset_password_key = "",
                                                    registration_id = "" ) # Agregar el usuario
                    db.auth_membership.insert(user_id = id, group_id= 2) # Agregar permisos de profesor

                    db.profesor.insert(ci = request.vars.cedula)
                    response.flash = 'Agregado profesor exitosamente'

                else:
                    response.flash= "El formato de la cedula no es el correcto"
            else:
                response.flash = "Ya existe un usuario con esa cedula"
    #####################################
    # Agregar administradores manualmente
    #####################################

        elif request.vars.tipoUsuario == "admin":
            if (not(db(db.usuario.username == request.vars.cedula).select())):
                if re.match('^[0-9]{1,8}$', request.vars.cedula):
                    admin_nuevo = db.usuario.insert(first_name = request.vars.nombres,
                                                    last_name = request.vars.apellidos,
                                                    email = request.vars.email,
                                                    username = request.vars.cedula,
                                                    password = db.usuario.password.validate(request.vars.cedula)[0],
                                                    registration_key = "",
                                                    reset_password_key = "",
                                                    registration_id = "" ) # Agregar el usuario

                    db.auth_membership.insert(user_id = admin_nuevo, group_id= 5) # Agregar permisos de estudiantes
                    response.flash = "Adminitrador agregado exitosamente"
                else:
                    response.flash= "El formato de la cedula no es el correcto"
            else:
                response.flash = "Ya existe un usuario con esa cedula"
    elif formularioAgregarManual.errors:
        response.flash = "Formulario no fue aceptado VERSION 1"

    #######################
    # Para los desplegables
    #######################

    liceos = db(db.liceo.id>0).select()
    sedes = db(db.sede.id>0).select()
    profesores = db(db.profesor.id>0).select()
    cohortes = db(db.cohorte.id>0).select()

    ##########################
    # Fin de los desplegables
    ##########################

    return dict(liceos=liceos, sedes=sedes, profesores=profesores, cohortes=cohortes)

@auth.requires_membership('Administrador')
@auth.requires_login()
def agregarCohorte():
    return dict()

@auth.requires_membership('Administrador')
@auth.requires_login()
def cambioContrasena():
    return dict()

@auth.requires_membership('Administrador')
@auth.requires_login()
def cargarArchivo():
    ##################
    # Carga de archivo
    ##################
    erroresCarga = [] # Los errores en la carga van aqui
    cargaExitosa = [] # Los usuarios agregados exitosamente van aqui
    cohorte = db(db.cohorte.status=="Activa").select()[0].identificador # Cohorte Actual
    formularioArchivo = FORM()
    if formularioArchivo.accepts(request.vars,formname='formularioArchivo'): # Chequeamos si hay un archivo cargado
        archivo =request.vars.fileToUpload.filename.split(".")  # Separamos el nombre del archivo de la extension
        nombreArchivo, extension = archivo[0], archivo[1]
        if extension == "csv":          # Chequeamos la extension del archivo
            ######################
            # Cargando Estudiantes
            ######################
            if request.vars.optradio == "estudiante":   # Chequeamos el tipo de usuario a agregar
                f = request.vars.fileToUpload.file      # Archivo cargado
                texto = f.read().splitlines()           # Leer el archivo
                cabecera = texto[0].split(";")          # Extraemos la cabecera
                liceo = texto[1].split(";")             # Extraemos la linea que contiene el nombre del liceo
                texto.remove(texto[1])                  # Eliminamos del texto la linea del liceo para no iterar sobre ella
                texto.remove(texto[0])                  # Eliminamos del texto la cabecera para no iterar sobre ella
                if ((cabecera[0]=="C.I." and cabecera[1]=='Nombres' and
                cabecera[2]=='Apellidos' and cabecera[3]=='Promedio (00.00)') and
                (liceo[0] == "Nombre del Liceo:") and liceo[1] == "" and liceo[2] != ""): # Verificamos que la cabecera y la linea del liceo tenga el formato correcto
                    liceo = liceo[2]                    # Seleccionamos el nombre del liceo
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
                                    if re.match('^[0-9]{1,8}$', i[0]):          # Verificamos que la cedula cumpla la expresion regular
                                        id = db.usuario.insert(first_name = i[1],last_name = i[2], email = "", username = i[0],
                                                      password = db.usuario.password.validate(i[0])[0], registration_key = "",
                                                      reset_password_key = "", registration_id = "" )       # Agregar el usuario
                                        db.auth_membership.insert(user_id = id, group_id= 1)                # Agregar permisos de estudiante (group_id=1)
                                        db.estudiante.insert(ci=i[0], promedio=float(i[3]), direccion="", telefono_habitacion="",
                                                        telefono_otro="", fecha_nacimiento="", sexo="", estatus="Pre-inscrito",
                                                        cohorte=cohorte, ci_representante="", nombre_representante="",
                                                        apellido_representante="", sexo_representante="", correo_representante="",
                                                        direccion_representante="", nombre_liceo=liceo, telefono_representante_oficina="",
                                                        telefono_representante_otro="", sufre_enfermedad="", enfermedad="",
                                                        indicaciones_enfermedad="")
                                        cargaExitosa.append(i)                          # Agregarlo a los estudiantes cargados exitosamente
                                    else:
                                        erroresCarga.append([i,"Cedula incorrecta"])                                            # Error de Carga
                                else:
                                    erroresCarga.append([i,"Su liceo no esta en la base de datos. Contacte al administrador"])  # Error de Carga
                            else:
                                erroresCarga.append([i,"El promedio debe ser un numero entre 0 y 20"])                          # Error de Carga
                        else:
                            erroresCarga.append([i,"Ya existe un usuario en el sistema con esta cedula"])                       # Error de Carga

                else:
                    response.flash = "Formato de los datos del archivo invalido. Consulte el manual"                            # Error de Carga
            #################################
            # Cargando Representantes de sede
            #################################
            elif request.vars.optradio == "sede":
                f = request.vars.fileToUpload.file      # Archivo cargado
                texto = f.read().splitlines()           # Leer el archivo
                cabecera = texto[0].split(";")          # Extraemos la cabecera
                texto.remove(texto[0])                  # Eliminamos del texto la cabecera para no iterar sobre ella
                if (cabecera[0]=="C.I." and cabecera[1]=='Nombres' and
                    cabecera[2]=='Apellidos' and cabecera[3]=='Sede'): # Verificamos que la cabecera tenga el formato correcto
                    datos = []                          # Los usuarios a agregar van aqui
                    for i in texto:
                        if i != ";;;;":
                            dato = i.split(";")         # Separamos los datos del usuario
                            datos.append(dato)          # Agregamos el usuario a la lista de usuarios por agregar

                    for i in datos:
                        if (not(db(db.usuario.username == i[0]).select()) and
                            not(db(db.representante_sede.ci == i[0]).select())):    # Verificar que no existe un usuario para esa cedula
                            if db(db.sede.zona == i[3]).select():                # Verificamos que la sede este en la base de datos
                                if re.match('^[0-9]{1,8}$', i[0]):                      # Verificamos que la cedula cumpla la expresion regular
                                    id = db.usuario.insert(first_name = i[1],last_name = i[2], email = "", username = i[0],
                                                  password = db.usuario.password.validate(i[0])[0], registration_key = "",
                                                  reset_password_key = "", registration_id = "" ) # Agregar el usuario
                                    db.auth_membership.insert(user_id = id, group_id=4) # Agregar permisos de representante sede (group_id=4)
                                    db.representante_sede.insert(ci=i[0], sede=i[3]) # Agregar el representante de sede
                                    cargaExitosa.append(i) # Agregarlo a los usuarios cargados exitosamente
                                else:
                                    erroresCarga.append([i,"Cedula incorrecta"])                                                # Error de Carga
                            else:
                                erroresCarga.append([i,"Su sede no esta en la base de datos. Contacte al administrador"])  # Error de Carga
                        else:
                            erroresCarga.append([i,"Ya existe un usuario en el sistema con esta cedula"])                   # Error de Carga
                else: #Error
                    response.flash = "Formato de los datos del archivo invalido. Consulte el manual"                       # Error de Carga
            ##################################
            # Cargando Representante de liceos
            ##################################
            elif request.vars.optradio == "liceo":
                f = request.vars.fileToUpload.file      # Archivo cargado
                texto = f.read().splitlines()           # Leer el archivo
                cabecera = texto[0].split(";")          # Extraemos la cabecera
                texto.remove(texto[0])                  # Eliminamos del texto la cabecera para no iterar sobre ella
                if (cabecera[0]=="C.I." and cabecera[1]=='Nombres' and
                cabecera[2]=='Apellidos' and cabecera[3]=='Liceo'): # Verificamos que la cabecera tenga el formato correcto
                    datos = []                          # Los usuarios a agregar van aqui
                    for i in texto:
                        if i != ";;;;":
                            dato = i.split(";")         # Separamos los datos del usuario
                            datos.append(dato)          # Agregamos el usuario a la lista de usuarios por agregar

                    for i in datos:
                        if (not(db(db.usuario.username == i[0]).select()) and
                            not(db(db.representante_liceo.ci == i[0]).select())):    # Verificar que no existe un usuario para esa cedula
                            if db(db.liceo.nombre == i[3]).select():                # Verificamos que el liceo este en la base de datos
                                if re.match('^[0-9]{1,8}$', i[0]):      # Verificamos que la cedula cumpla la expresion regular
                                    id = db.usuario.insert(first_name = i[1],last_name = i[2], email = "", username = i[0],
                                                  password = db.usuario.password.validate(i[0])[0], registration_key = "",
                                                  reset_password_key = "", registration_id = "" ) # Agregar el usuario
                                    db.auth_membership.insert(user_id = id, group_id=3) # Agregar permisos de representante liceo (group_id=3)
                                    db.representante_liceo.insert(ci=i[0], nombre_liceo=i[3]) # Agregar el representante de liceo
                                    cargaExitosa.append(i) # Agregarlo a los usuarios cargados exitosamente
                                else:
                                    erroresCarga.append([i,"Cedula incorrecta"])                                            # Error de Carga
                            else:
                                erroresCarga.append([i,"Su liceo no esta en la base de datos. Contacte al administrador"])  # Error de Carga
                        else:
                            erroresCarga.append([i,"Ya existe un usuario en el sistema con esta cedula"])                   # Error de Carga
                else: #Error
                    response.flash= "Formato de los datos del archivo invalido. Consulte el manual"                          # Error de Carga
            #####################
            # Cargando Profesores
            #####################
            elif request.vars.optradio == "profesor":
                f = request.vars.fileToUpload.file      # Archivo cargado
                texto = f.read().splitlines()           # Leer el archivo
                cabecera = texto[0].split(";")          # Extraemos la cabecera
                chequeo = texto[1].split(";")             # Extraemos la linea que contiene el nombre del liceo
                texto.remove(texto[1])                  # Eliminamos del texto la linea del liceo para no iterar sobre ella
                texto.remove(texto[0])
                if (cabecera[0]=="C.I." and cabecera[1]=='Nombres' and
                    cabecera[2]=='Apellidos' and cabecera[3]=='Materia' and
                    chequeo[0] == "A continuacion ingrese los profesores" and
                    chequeo[1] == "" and chequeo[2] == ""):

                    datos = []                          # Los usuarios a agregar van aqui
                    for i in texto:
                        if i != ";;;;":
                            dato = i.split(";")         # Separamos los datos del usuario
                            datos.append(dato)

                    for i in datos:
                        if (not(db(db.usuario.username == i[0]).select()) and
                            not(db(db.profesor.ci == i[0]).select())):    # Verificar que no existe un usuario para esa cedula
                            if re.match('^[0-9]{1,8}$', i[0]):      # Verificamos que la cedula cumpla la expresion regular
                                id = db.usuario.insert(first_name = i[1],last_name = i[2], email = "", username = i[0],
                                              password = db.usuario.password.validate(i[0])[0], registration_key = "",
                                              reset_password_key = "", registration_id = "" ) # Agregar el usuario
                                db.auth_membership.insert(user_id = id, group_id=2) # Agregar permisos de profesor(group_id=2)
                                db.profesor.insert(ci=i[0]) # Agregar el profesor FALTA LA MATERIA EN LA BD
                                cargaExitosa.append(i) # Agregarlo a los usuarios cargados exitosamente
                            else:
                                erroresCarga.append([i,"Cedula incorrecta"])                                            # Error de Carga
                        else:
                            erroresCarga.append([i,"Ya existe un usuario en el sistema con esta cedula"])                   # Error de Carga
                else: #Error
                    response.flash= "Formato de los datos del archivo invalido. Consulte el manual"
            #####################
            # Cargando Liceos
            #####################
            elif request.vars.optradio == "liceos":
                f = request.vars.fileToUpload.file      # Archivo cargado
                texto = f.read().splitlines()           # Leer el archivo
                cabecera = texto[0].split(";")          # Extraemos la cabecera
                texto.remove(texto[0])                  # Eliminamos del texto la cabecera para no iterar sobre ella
                if (cabecera[0]=="Nombre del Liceo" and cabecera[2]=='Tipo del Liceo' and
                cabecera[4]=='Sede'):                   # Verificamos que la cabecera tenga el formato correcto
                    datos = []                          # Los liceos a agregar van aqui
                    for i in texto:
                        if i != ";;;;":
                            dato = i.split(";")         # Separamos los datos del usuario
                            datos.append(dato)          # Agregamos el usuario a la lista de usuarios por agregar

                    for i in datos:
                        if not(db(db.liceo.nombre == i[0]).select()):               # Verificar que no existe un liceo con ese nombre
                            db.liceo.insert(nombre = i[0], tipo = i[2], sede = i[4]) # Agregar el liceos
                            cargaExitosa.append(i) # Agregarlo a los liceos cargados exitosamente
                        else:
                            erroresCarga.append([i,"Ya existe un liceo en el sistema con ese nombre"])                      # Error de Carga
                else: #Error
                    erroresCarga.append("Formato de los datos del archivo invalido. Consulte el manual")                    # Error de Carga
            if erroresCarga:
                response.flash = 'Procesado archivo exitosamente, hubo problemas con algunos datos'
            else:
                response.flash = 'Procesado archivo exitosamente'
        else: #Error
            response.flash = "El formato del archivo debe ser \".csv\". Consulte el manual de usuario"
    else:
        pass

    return dict(erroresCarga=erroresCarga, cargaExitosa=cargaExitosa)

@auth.requires_membership('Administrador')
@auth.requires_login()
def cargarInstitucionManual():

    if request.vars:
        if not(db(db.liceo.nombre == request.vars.nombre).select()):
            db.liceo.insert(nombre = request.vars.nombre,
                            tipo = request.vars.tipoInst,
                            sede = request.vars.sede)
            response.flash = "Agregado liceo exitosamente"
        else:
            response.flash = "Ya existe en el sistema un liceo con ese nombre"

    #######################
    # Para los desplegables
    #######################

    liceos = db(db.liceo.id>0).select()
    sedes = db(db.sede.id>0).select()
    profesores = db(db.profesor.id>0).select()
    cohortes = db(db.cohorte.id>0).select()

    ##########################
    # Fin de los desplegables
    ##########################
    return dict(liceos=liceos, sedes=sedes,profesores=profesores,
                cohortes=cohortes)

@auth.requires_membership('Administrador')
@auth.requires_login()
def consultar():
    #############
    # Consulta
    #############
    consulta = None
    formularioConsulta = FORM()
    consultarTodo = FORM()

    if consultarTodo.accepts(request.vars,formname="consultarTodo"):
        consulta = db(db.usuario.id>0).select()

    if formularioConsulta.accepts(request.vars,formname="formularioConsulta"):
        pass

    ###############
    # Fin Consulta
    ###############
    return dict(consulta=consulta)

@auth.requires_membership('Administrador')
@auth.requires_login()
def modificarInstitucion():
    #######################
    # Para los desplegables
    #######################

    liceos = db(db.liceo.id>0).select()
    sedes = db(db.sede.id>0).select()
    profesores = db(db.profesor.id>0).select()
    cohortes = db(db.cohorte.id>0).select()

    ##########################
    # Fin de los desplegables
    ##########################
    return dict(liceos=liceos, sedes=sedes,profesores=profesores,
                cohortes=cohortes)

@auth.requires_membership('Administrador')
@auth.requires_login()
def enviarEmail():
    return dict()

@auth.requires_membership('Administrador')
@auth.requires_login()
def modificarUsuario():
    cedulaModificar = FORM()
    if cedulaModificar.accepts(request.vars,formname="cedulaModificar"):    # Verificamos que se haya introducido una cedula
        if db(db.estudiante.ci==request.vars.ci).select():
            session.cedula = request.vars.ci
            redirect(URL('modificarEstudiante'))
        elif db(db.representante_sede.ci==request.vars.ci).select():
            session.cedula = request.vars.ci
            redirect(URL('modificarRepresentanteSede'))
        elif db(db.representante_liceo.ci==request.vars.ci).select():
            session.cedula = request.vars.ci
            redirect(URL('modificarRepresentanteLiceo'))
        elif db(db.profesor.ci==request.vars.ci).select():
            session.cedula = request.vars.ci
            redirect(URL('modificarProfesor'))
        elif db(db.usuario.username==request.vars.ci).select():
            idAdmin = db(db.usuario.username==request.vars.ci).select()[0].id
            membership = db(db.auth_membership.user_id==idAdmin).select()[0].group_id
            if membership == 5:
                session.cedula = request.vars.ci
                redirect(URL('modificarAdmin'))

        else:
            response.flash = 'No hay un usuario para esta cedula'

    return dict()

@auth.requires_membership('Administrador')
@auth.requires_login()
def modificarEstudiante():
    usuario = db(db.usuario.username==session.cedula).select()[0]
    estudiante = db(db.estudiante.ci==session.cedula).select()[0]
    errorPromedio = False

    cohorte = estudiante.cohorte
    limiteEximidos = 0
    if db(db.liceo.nombre==estudiante.nombre_liceo).select()[0].tipo == "Publico":
        limiteEximidos = 3
    elif db(db.liceo.nombre==estudiante.nombre_liceo).select()[0].tipo == "Subsidiado":
        limiteEximidos = 1

    errorExime = False
    errorYaEximido = False

    numeroEximidos = db((db.exime.cohorte==cohorte) & (db.exime.liceo==estudiante.nombre_liceo)).count()

    eximido = False
    if db(db.exime.ci_estudiante==estudiante.ci).select():
        eximido = True

    if request.vars:

        # Chequemos el limite de estudiantes eximidos para el liceo
        if (not(eximido)and (request.vars.eximido=="True") and
           (numeroEximidos<limiteEximidos) and not(db(db.exime.ci_estudiante==estudiante.ci).select())):
            db.exime.insert(ci_estudiante=estudiante.ci, liceo=estudiante.nombre_liceo,
                            cohorte=estudiante.cohorte)
            eximido=True
        elif (not(eximido)and (request.vars.eximido=="True") and
           (numeroEximidos<limiteEximidos) and (db(db.exime.ci_estudiante==estudiante.ci).select())):
               errorYaEximido = True
        elif (not(eximido)and request.vars.eximido=="True" and numeroEximidos>=limiteEximidos):
            errorExime = True

        elif eximido and request.vars.eximido=="False":
            db(db.exime.ci_estudiante==estudiante.ci).delete()
        else:
            pass

        # Si cambia la cedula, actualizamos el estudiante, el username del usuario y restablecemos la contraseña
        if db(db.estudiante.ci==session.cedula).select()[0].ci != request.vars.cedula:
            db(db.estudiante.ci==session.cedula).update(ci=request.vars.cedula)
            db(db.usuario.username==session.cedula).update(username=request.vars.cedula)
            db(db.usuario.username==session.cedula).update(password=db.usuario.password.validate(request.vars.cedula)[0])
            session.cedula = request.vars.cedula

        db(db.usuario.username==session.cedula).update(first_name=request.vars.nombres)
        db(db.usuario.username==session.cedula).update(last_name=request.vars.apellidos)
        db(db.usuario.username==session.cedula).update(email=request.vars.email)

        # Chequeamos que el promedio sea valido
        promedio = float(request.vars.PromedioEntero)+(float(request.vars.PromedioDecimal)/100)
        if 0 <= promedio <= 20:
            db(db.estudiante.ci==session.cedula).update(promedio=promedio)
        else:
            errorPromedio = True

        db(db.estudiante.ci==session.cedula).update(direccion=request.vars.direccion)
        db(db.estudiante.ci==session.cedula).update(telefono_habitacion=request.vars.telefonoHabitacionE)
        db(db.estudiante.ci==session.cedula).update(telefono_otro=request.vars.telefonoOtroE)
        db(db.estudiante.ci==session.cedula).update(fecha_nacimiento=request.vars.fecha)
        db(db.estudiante.ci==session.cedula).update(sexo=request.vars.sexo)
        db(db.estudiante.ci==session.cedula).update(nombre_liceo=request.vars.liceo)
        db(db.estudiante.ci==session.cedula).update(estatus=request.vars.estatus)
        db(db.estudiante.ci==session.cedula).update(cohorte=request.vars.cohorte)
        db(db.estudiante.ci==session.cedula).update(ci_representante=request.vars.cedulaRepresentante)
        db(db.estudiante.ci==session.cedula).update(nombre_representante=request.vars.nombresRepresentante)
        db(db.estudiante.ci==session.cedula).update(apellido_representante=request.vars.apellidosRepresentante)
        db(db.estudiante.ci==session.cedula).update(sexo_representante=request.vars.sexoRepresentante)
        db(db.estudiante.ci==session.cedula).update(correo_representante=request.vars.emailRepresentante)
        db(db.estudiante.ci==session.cedula).update(direccion_representante=request.vars.direccionRepresentante)
        db(db.estudiante.ci==session.cedula).update(telefono_representante_oficina=request.vars.telefonoHabitacionRepresentanteE)
        db(db.estudiante.ci==session.cedula).update(telefono_representante_otro=request.vars.telefonoOtroRepresentanteE)
        db(db.estudiante.ci==session.cedula).update(sufre_enfermedad=request.vars.enfermedad)
        db(db.estudiante.ci==session.cedula).update(enfermedad=request.vars.informacionEnfermedad)
        db(db.estudiante.ci==session.cedula).update(indicaciones_enfermedad=request.vars.indicacionEnfermedad)

        # Para actualizar sin recargar
        usuario = db(db.usuario.username==session.cedula).select()[0]
        estudiante = db(db.estudiante.ci==session.cedula).select()[0]

        if errorPromedio and not(errorExime) and not(errorYaEximido):
            response.flash = "Modificado con exito. Hubo un error en el Promedio"
        elif not(errorPromedio) and errorExime:
            response.flash = "Datos modificado exitosamente, sin embargo no se \
                              puede eximir este alumno ya que se excedio el limite \
                              de eximidos de su liceo para esta cohorte"
        elif errorPromedio and errorExime:
            response.flash = "Datos modificado exitosamente, sin embargo no se \
                              puede eximir este alumno ya que se excedio el limite \
                              de eximidos de su liceo para esta cohorte. Hubo un error\
                              en el promedio"
        elif not(errorPromedio) and errorYaEximido:
            response.flash = "Datos modificado exitosamente, sin embargo no se \
                              puede eximir este alumno porque ya esta eximido"
        elif errorPromedio and errorYaEximido:
            response.flash = "Datos modificado exitosamente, sin embargo no se \
                              puede eximir este alumno poruqe ya esta eximido. \
                              Hubo un error en el promedio"

        else:
            response.flash = "Modificado con Exito"

    #######################
    # Para los desplegables
    #######################

    liceos = db(db.liceo.id>0).select()
    cohortes = db(db.cohorte.id>0).select()

    ##########################
    # Fin de los desplegables
    ##########################
    return dict(usuario=usuario,estudiante=estudiante,liceos=liceos,
                cohortes=cohortes,eximido=eximido)

@auth.requires_membership('Administrador')
@auth.requires_login()
def modificarRepresentanteSede():
    usuario = db(db.usuario.username==session.cedula).select()[0]
    representante = db(db.representante_sede.ci==session.cedula).select()[0]

    if request.vars:
        # Si cambia la cedula, actualizamos el representante_sede, el username del usuario y restablecemos la contraseña
        if db(db.representante_sede.ci==session.cedula).select()[0].ci != request.vars.cedula:
            db(db.representante_sede.ci==session.cedula).update(ci=request.vars.cedula)
            db(db.usuario.username==session.cedula).update(username=request.vars.cedula)
            db(db.usuario.username==session.cedula).update(password=db.usuario.password.validate(request.vars.cedula)[0])
            session.cedula = request.vars.cedula

        db(db.usuario.username==session.cedula).update(first_name=request.vars.nombres)
        db(db.usuario.username==session.cedula).update(last_name=request.vars.apellidos)
        db(db.usuario.username==session.cedula).update(email=request.vars.email)
        db(db.representante_sede.ci==session.cedula).update(sede=request.vars.sede)
        # Para actualizar sin recargar
        usuario = db(db.usuario.username==session.cedula).select()[0]
        representante = db(db.representante_sede.ci==session.cedula).select()[0]

    # Para los desplegables
    sedes = db(db.sede.id>0).select()
    return dict(usuario=usuario,sedes=sedes,representante=representante)

@auth.requires_membership('Administrador')
@auth.requires_login()
def modificarRepresentanteLiceo():
    representante = db(db.representante_liceo.ci==session.cedula).select()[0]
    usuario = db(db.usuario.username==session.cedula).select()[0]
    if request.vars:
        # Si cambia la cedula, actualizamos el representante_liceo, el username del usuario y restablecemos la contraseña
        if db(db.representante_liceo.ci==session.cedula).select()[0].ci != request.vars.cedula:
            db(db.representante_liceo.ci==session.cedula).update(ci=request.vars.cedula)
            db(db.usuario.username==session.cedula).update(username=request.vars.cedula)
            db(db.usuario.username==session.cedula).update(password=db.usuario.password.validate(request.vars.cedula)[0])
            session.cedula = request.vars.cedula

        db(db.usuario.username==session.cedula).update(first_name=request.vars.nombres)
        db(db.usuario.username==session.cedula).update(last_name=request.vars.apellidos)
        db(db.usuario.username==session.cedula).update(email=request.vars.email)
        db(db.representante_liceo.ci==session.cedula).update(nombre_liceo=request.vars.liceo)

        # Para actualizar sin recargar
        representante = db(db.representante_liceo.ci==session.cedula).select()[0]
        usuario = db(db.usuario.username==session.cedula).select()[0]

    # Para los desplegables
    liceos = db(db.liceo.id>0).select()
    return dict(usuario=usuario,liceos=liceos,representante=representante)

@auth.requires_membership('Administrador')
@auth.requires_login()
def modificarAdmin():
    usuario = db(db.usuario.username==session.cedula).select()[0]

    if request.vars:
        db(db.usuario.username==session.cedula).update(first_name=request.vars.nombres)
        db(db.usuario.username==session.cedula).update(last_name=request.vars.apellidos)
        db(db.usuario.username==session.cedula).update(email=request.vars.email)
        db(db.usuario.username==session.cedula).update(username=request.vars.cedula) # La cedula se actualiza de ultimo
        response.flash = "Modificado exitosamente"

        # Para actualizar sin recargar
        usuario = db(db.usuario.username==session.cedula).select()[0]

    return dict(usuario=usuario)

@auth.requires_membership('Administrador')
@auth.requires_login()
def modificarProfesor():
    usuario = db(db.usuario.username==session.cedula).select()[0]
    profesor = db(db.profesor.ci==session.cedula).select()[0]

    if request.vars:
        # Si cambia la cedula, actualizamos el profesor, el username del usuario y restablecemos la contraseña
        if db(db.profesor.ci==session.cedula).select()[0].ci != request.vars.cedula:
            db(db.profesor.ci==session.cedula).update(ci=request.vars.cedula)
            db(db.usuario.username==session.cedula).update(username=request.vars.cedula)
            db(db.usuario.username==session.cedula).update(password=db.usuario.password.validate(request.vars.cedula)[0])
            session.cedula = request.vars.cedula

        db(db.usuario.username==session.cedula).update(first_name=request.vars.nombres)
        db(db.usuario.username==session.cedula).update(last_name=request.vars.apellidos)
        db(db.usuario.username==session.cedula).update(email=request.vars.email)

        # Para actualizar sin recargar
        usuario = db(db.usuario.username==session.cedula).select()[0]
        profesor = db(db.profesor.ci==session.cedula).select()[0]

    return dict(usuario=usuario,profesor=profesor)

@auth.requires_membership('Administrador')
@auth.requires_login()
def noticias():
    return dict()

@auth.requires_membership('Administrador')
@auth.requires_login()
def perfil():
    return dict()

@auth.requires_membership('Administrador')
@auth.requires_login()
def reporte():
    return dict()
