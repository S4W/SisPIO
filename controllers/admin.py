# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import os,re,time
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
                            response.flash = "El formato de la cédula no es el correcto"
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
                        if not(db(db.representante_liceo.nombre_liceo==request.vars.liceo).select()):
                            id = db.usuario.insert(first_name = request.vars.nombres ,
                                                   last_name = request.vars.apellidos,
                                                   email = request.vars.email,
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
                            response.flash = "Ya existe un representante para este liceo"
                    else:
                        response.flash = "El formato de la cédula no es el correcto"
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
                        response.flash = "El formato de la cédula no es el correcto"
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
                    if db(db.materia.nombre==request.vars.materia).select():
                        id = db.usuario.insert(first_name = request.vars.nombres,
                                                        last_name = request.vars.apellidos,
                                                        email = "",
                                                        username = request.vars.cedula,
                                                        password = db.usuario.password.validate(request.vars.cedula)[0],
                                                        registration_key = "",
                                                        reset_password_key = "",
                                                        registration_id = "" ) # Agregar el usuario
                        db.auth_membership.insert(user_id = id, group_id= 2) # Agregar permisos de profesor

                        db.profesor.insert(ci = request.vars.cedula, materia=request.vars.materia)
                        response.flash = 'Agregado profesor exitosamente'
                    else:
                        response.flash = "La materia no se encuentra en la base de datos"
                else:
                    response.flash= "El formato de la cédula no es el correcto"
            else:
                response.flash = "Ya existe un usuario con esa cédula"
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
                    response.flash= "El formato de la cédula no es el correcto"
            else:
                response.flash = "Ya existe un usuario con esa cédula"
    elif formularioAgregarManual.errors:
        response.flash = "Formulario no fue aceptado VERSION 1"

    #######################
    # Para los desplegables
    #######################

    ordenAlfabeticoLiceos = db.liceo.nombre.lower()
    ordenAlfabeticoSedes = db.sede.zona.lower()
    ordenAlfabeticoCohortes = db.cohorte.identificador.lower()
    ordenAlfabeticoMaterias = db.materia.nombre.lower()

    materias = db(db.materia.id>0).select(orderby = ordenAlfabeticoMaterias)
    liceos = db(db.liceo.id>0).select(orderby = ordenAlfabeticoLiceos)
    sedes = db(db.sede.id>0).select(orderby = ordenAlfabeticoSedes)
    profesores = db(db.profesor.id>0).select()
    cohortes = db(db.cohorte.id>0).select(orderby = ordenAlfabeticoCohortes)

    ##########################
    # Fin de los desplegables
    ##########################

    return dict(liceos=liceos, sedes=sedes, profesores=profesores,
                cohortes=cohortes,materias=materias)

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
                if len(cabecera) == 5 and len(texto)>=2:
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
                        response.flash = "Formato de los datos del archivo inválido. Consulte el manual"             # Error de Carga
                else:
                    response.flash = "Formato de los datos del archivo inválido. Consulte el manual"             # Error de Carga
            #################################
            # Cargando Representantes de sede
            #################################
            elif request.vars.optradio == "sede":
                f = request.vars.fileToUpload.file      # Archivo cargado
                texto = f.read().splitlines()           # Leer el archivo
                cabecera = texto[0].split(";")          # Extraemos la cabecera
                texto.remove(texto[0])                  # Eliminamos del texto la cabecera para no iterar sobre ella
                if len(cabecera) == 5 and len(texto)>=1:
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
                                        erroresCarga.append([i,"Cédula incorrecta"])                                                # Error de Carga
                                else:
                                    erroresCarga.append([i,"Su sede no esta en la base de datos. Contacte al administrador"])  # Error de Carga
                            else:
                                erroresCarga.append([i,"Ya existe un usuario en el sistema con esta cédula"])                   # Error de Carga
                    else: #Error
                        response.flash = "Formato de los datos del archivo inválido. Consulte el manual"             # Error de Carga
                else: #Error
                    response.flash = "Formato de los datos del archivo inválido. Consulte el manual"             # Error de Carga
            ##################################
            # Cargando Representante de liceos
            ##################################
            elif request.vars.optradio == "liceo":
                f = request.vars.fileToUpload.file      # Archivo cargado
                texto = f.read().splitlines()           # Leer el archivo
                cabecera = texto[0].split(";")          # Extraemos la cabecera
                texto.remove(texto[0])                  # Eliminamos del texto la cabecera para no iterar sobre ella
                if len(cabecera) == 5 and len(texto)>=1:
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
                                        if not(db(db.representante_liceo.nombre_liceo==i[3]).select()):
                                            id = db.usuario.insert(first_name = i[1],last_name = i[2], email = "", username = i[0],
                                                          password = db.usuario.password.validate(i[0])[0], registration_key = "",
                                                          reset_password_key = "", registration_id = "" ) # Agregar el usuario
                                            db.auth_membership.insert(user_id = id, group_id=3) # Agregar permisos de representante liceo (group_id=3)
                                            db.representante_liceo.insert(ci=i[0], nombre_liceo=i[3]) # Agregar el representante de liceo
                                            cargaExitosa.append(i) # Agregarlo a los usuarios cargados exitosamente
                                        else:
                                            erroresCarga.append([i, "Ya existe un representante para este liceo"])
                                    else:
                                        erroresCarga.append([i,"Cedula incorrecta"])                                            # Error de Carga
                                else:
                                    erroresCarga.append([i,"Su liceo no esta en la base de datos. Contacte al administrador"])  # Error de Carga
                            else:
                                erroresCarga.append([i,"Ya existe un usuario en el sistema con esta cédula"])                   # Error de Carga
                    else: #Error
                        response.flash= "Formato de los datos del archivo inválido. Consulte el manual"                          # Error de Carga
                else: #Error
                    response.flash= "Formato de los datos del archivo inválido. Consulte el manual"
            #####################
            # Cargando Profesores
            #####################
            elif request.vars.optradio == "profesor":
                f = request.vars.fileToUpload.file      # Archivo cargado
                texto = f.read().splitlines()           # Leer el archivo
                cabecera = texto[0].split(";")          # Extraemos la cabecera
                if len(cabecera) == 5 and len(texto)>=2:
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
                                    if db(db.materia.nombre==i[3]).select():
                                        id = db.usuario.insert(first_name = i[1],last_name = i[2], email = "", username = i[0],
                                                      password = db.usuario.password.validate(i[0])[0], registration_key = "",
                                                      reset_password_key = "", registration_id = "" ) # Agregar el usuario
                                        db.auth_membership.insert(user_id = id, group_id=2) # Agregar permisos de profesor(group_id=2)
                                        db.profesor.insert(ci=i[0],materia=i[3]) # Agregar el profesor FALTA LA MATERIA EN LA BD
                                        cargaExitosa.append(i) # Agregarlo a los usuarios cargados exitosamente
                                    else:
                                        erroresCarga.append([i,"La materia no se encuentra en la base de datos"])
                                else:
                                    erroresCarga.append([i,"Cedula incorrecta"])                                            # Error de Carga
                            else:
                                erroresCarga.append([i,"Ya existe un usuario en el sistema con esta cédula"])                   # Error de Carga
                    else: #Error
                        response.flash= "Formato de los datos del archivo inválido. Consulte el manual"
                else: #Error
                    response.flash= "Formato de los datos del archivo inválido. Consulte el manual"
            #####################
            # Cargando Liceos
            #####################
            elif request.vars.optradio == "liceos":
                f = request.vars.fileToUpload.file      # Archivo cargado
                texto = f.read().splitlines()           # Leer el archivo
                cabecera = texto[0].split(";")          # Extraemos la cabecera
                texto.remove(texto[0])                  # Eliminamos del texto la cabecera para no iterar sobre ella
                if len(cabecera) == 6 and len(texto)>=1:
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
                        response.flash = "Formato de los datos del archivo inválido. Consulte el manual"                    # Error de Carga
                else: #Error
                    response.flash = "FFormato de los datos del archivo inválido. Consulte el manual"                    # Error de Carga
            ###############################
            # Cambiando estados estudiantes
            ###############################
            elif request.vars.optradio == "estadoEstudiante":
                f = request.vars.fileToUpload.file      # Archivo cargado
                texto = f.read().splitlines()           # Leer el archivo
                cabecera = texto[0].split(";")          # Extraemos la cabecera
                if len(cabecera) == 3 and len(texto)>=2:
                    estado = texto[1].split(";")             # Extraemos la linea que contiene el estado a colocar en los estudiantes
                    texto.remove(texto[1])                  # Eliminamos del texto la linea del liceo para no iterar sobre ella
                    texto.remove(texto[0])                  # Eliminamos del texto la cabecera para no iterar sobre ella
                    if (cabecera[0]=="C.I." and cabecera[1]=='' and
                    cabecera[2]=='NO MODIFICAR LA CABECERA' and
                    estado[0] == "Estado:" and estado[2] == "NO MODIFICAR LA CABECERA"): # Verificamos que la cabecera y la linea del liceo tenga el formato correcto
                        estado = estado[1]                    # Seleccionamos el nombre del liceo
                        datos = []                          # Los usuarios a agregar van aqui
                        for i in texto:
                            if i != ";;;;":
                                dato = i.split(";")         # Separamos los datos del usuario
                                datos.append(dato)          # Agregamos el usuario a la lista de usuarios por agregar
                        for i in datos:
                            if (db(db.usuario.username == i[0]).select() and
                               db(db.estudiante.ci == i[0]).select()):         # Verificar que existe un estudiante para esa cedula
                                     db(db.estudiante.ci == i[0]).update(estatus=estado)
                                     cargaExitosa.append(i)                          # Agregarlo a los estudiantes cargados exitosamente
                            else:
                                erroresCarga.append([i,"No existe un estudiante en el sistema con esta cedula"])                       # Error de Carga
                    else:
                        response.flash = "Formato de los datos del archivo inválido. Consulte el manual"             # Error de Carga
                else:
                    response.flash = "Formato de los datos del archivo inválido. Consulte el manual"             # Error de Carga

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
        if not(db(db.liceo.nombre == request.vars.Nombre).select()):
            db.liceo.insert(nombre = request.vars.Nombre,
                            tipo = request.vars.tipoInst,
                            sede = request.vars.sede)
            response.flash = "Agregado liceo exitosamente"
        else:
            response.flash = "Ya existe en el sistema un liceo con ese nombre"

    #######################
    # Para los desplegables
    #######################

    ordenAlfabeticoLiceos = db.liceo.nombre.lower()
    ordenAlfabeticoSedes = db.sede.zona.lower()
    ordenAlfabeticoCohortes = db.cohorte.identificador.lower()

    liceos = db(db.liceo.id>0).select(orderby = ordenAlfabeticoLiceos)
    sedes = db(db.sede.id>0).select(orderby = ordenAlfabeticoSedes)
    profesores = db(db.profesor.id>0).select()
    cohortes = db(db.cohorte.id>0).select(orderby = ordenAlfabeticoCohortes)

    ##########################
    # Fin de los desplegables
    ##########################
    return dict(liceos=liceos, sedes=sedes,profesores=profesores,
                cohortes=cohortes)

@auth.requires_membership('Administrador')
@auth.requires_login()
def consultarUsuarios():
    consulta=None

    if request.vars:
        #############################
        # Consulta de administradores
        #############################
        if request.vars.tipoUsuario=="administrador":

            # Orden
            orden = None
            if request.vars.tipoOrden=="cedula":
                orden = db.usuario.username
            elif request.vars.tipoOrden=="nombre":
                orden = db.usuario.first_name

            session.consulta = db((db.auth_membership.user_id==db.usuario.id) &
                          (db.auth_membership.group_id=="5")
                          ).select(db.usuario.first_name,db.usuario.last_name,
                          db.usuario.username,db.usuario.email, orderby=orden)

            redirect(URL('resultadosConsulta'))
        #########################
        # Consulta de estudiantes
        #########################
        elif request.vars.tipoUsuario=="estudiante":
            # Filtros
            query =(db.estudiante.ci==db.usuario.username)
            if request.vars.Cohorte != "Todos":
                query = query & (db.estudiante.cohorte==request.vars.Cohorte)
            if request.vars.Estado != "Todos":
                query = query & (db.estudiante.estatus==request.vars.Estado)
            if request.vars.Sexo != "Todos":
                query = query & (db.estudiante.sexo==request.vars.Sexo)
            if request.vars.Institucion != "Todos":
                query = query & (db.estudiante.nombre_liceo==request.vars.Institucion)
            if request.vars.MaxPromedioEntero != "0" or request.vars.MaxPromedioDecimal != "0":
                query = query & (db.estudiante.promedio<=(int(request.vars.MaxPromedioEntero)+(float(request.vars.MaxPromedioDecimal))/100))
            if request.vars.MinPromedioEntero != "0" or request.vars.MinPromedioDecimal != "0":
                query = query & (db.estudiante.promedio>=int(request.vars.MinPromedioEntero)+(float(request.vars.MinPromedioDecimal)/100))

            # Orden
            orden = None
            if request.vars.tipoOrden == "cedula":
                orden = db.usuario.username
            elif request.vars.tipoOrden == "institucion":
                orden = db.estudiante.nombre_liceo
            elif request.vars.tipoOrden == "cohorte":
                orden = db.estudiante.cohorte
            elif request.vars.tipoOrden == "estado":
                orden = db.estudiante.estatus
            elif request.vars.tipoOrden == "promedio":
                orden = db.estudiante.promedio

            if request.vars.tipoEstudiante == "Todos":
                session.consulta = db(query).select(db.usuario.username,db.usuario.first_name,
                                            db.usuario.last_name,db.estudiante.cohorte,
                                            db.estudiante.promedio,db.estudiante.estatus,
                                            db.estudiante.nombre_liceo, orderby=orden)
            elif request.vars.tipoEstudiante == "No eximidos":
                session.consulta = db(query)(~db.estudiante.ci.belongs(
                                    db(db.exime.ci_estudiante)._select(db.exime.ci_estudiante))
                                    ).select(db.usuario.username,db.usuario.first_name,
                                        db.usuario.last_name,db.estudiante.cohorte,
                                        db.estudiante.promedio,db.estudiante.estatus,
                                        db.estudiante.nombre_liceo, orderby=orden)
            elif request.vars.tipoEstudiante == "Eximidos":
                query = query & (db.estudiante.ci==db.exime.ci_estudiante)
                session.consulta = db(query).select(db.usuario.username,db.usuario.first_name,
                                            db.usuario.last_name,db.estudiante.cohorte,
                                            db.estudiante.promedio,db.estudiante.estatus,
                                            db.estudiante.nombre_liceo, orderby=orden)
            redirect(URL('resultadosConsulta'))
        ######################
        # Consulta de profesor
        ######################
        elif request.vars.tipoUsuario=="profesor":
            query = (db.usuario.username==db.profesor.ci)

            # Filtros
            if request.vars.Materia != "Todos":
                query = query & (db.profesor.materia==request.vars.Materia)

            # Orden
            orden = None
            if request.vars.tipoOrden=="cedula":
                orden = db.usuario.username
            elif request.vars.tipoOrden=="materia":
                orden = db.profesor.materia

            session.consulta = db(query).select(db.usuario.username,db.usuario.first_name,
                                        db.usuario.last_name,db.profesor.materia,
                                        db.usuario.email, orderby=orden)
            redirect(URL('resultadosConsulta'))
        #####################################
        # Consulta de representantes de liceo
        #####################################
        elif request.vars.tipoUsuario=="representanteLiceo":
            query = (db.usuario.username==db.representante_liceo.ci) & (db.representante_liceo.nombre_liceo==db.liceo.nombre)

            # Filtros
            if request.vars.Materia != "Todos":
                query = query & (db.profesor.materia==request.vars.Materia)

            # Orden
            orden = None
            if request.vars.tipoOrden=="institucion":
                orden = db.representante_liceo.nombre_liceo
            elif request.vars.tipoOrden=="tipoInstitucion":
                orden = db.liceo.tipo

            session.consulta = db(query).select(db.usuario.username,db.usuario.first_name,
                                        db.usuario.last_name,db.representante_liceo.nombre_liceo,
                                        db.representante_liceo.telefono,db.usuario.email,
                                        db.liceo.tipo,orderby=orden)
            redirect(URL('resultadosConsulta'))
        ####################################
        # Consulta de representantes de sede
        ####################################
        elif request.vars.tipoUsuario=="representanteSede":
            query = (db.usuario.username==db.representante_sede.ci)

            # Filtros
            if request.vars.sede != "Todos":
                query = query & (db.representante_sede.sede==request.vars.sede)

            # Orden
            orden = None
            if request.vars.tipoOrden=="cedula":
                orden = db.representante_sede.ci
            elif request.vars.tipoOrden=="sede":
                orden = db.representante_sede.sede

            session.consulta = db(query).select(db.usuario.username,db.usuario.first_name,
                                        db.usuario.last_name,db.representante_sede.sede,
                                        db.representante_sede.telefono,db.usuario.email,
                                        orderby=orden)
            redirect(URL('resultadosConsulta'))

    #######################
    # Para los desplegables
    #######################

    ordenAlfabeticoLiceos = db.liceo.nombre.lower()
    ordenAlfabeticoSedes = db.sede.zona.lower()
    ordenAlfabeticoCohortes = db.cohorte.identificador.lower()
    ordenAlfabeticoMaterias = db.materia.nombre.lower()

    liceos = db(db.liceo.id>0).select(orderby = ordenAlfabeticoLiceos)
    sedes = db(db.sede.id>0).select(orderby = ordenAlfabeticoSedes)
    materias = db(db.materia.id>0).select(orderby = ordenAlfabeticoMaterias)
    cohortes = db(db.cohorte.id>0).select(orderby = ordenAlfabeticoCohortes)

    ##########################
    # Fin de los desplegables
    ##########################
    return dict(cohortes=cohortes,sedes=sedes,liceos=liceos,materias=materias)

@auth.requires_membership('Administrador')
@auth.requires_login()
def consultarInstituciones():
    consulta = None

    if request.vars:
        if request.vars.tipoInstitucion == "Todas":
            query = db.liceo.id>0
        elif request.vars.tipoInstitucion == "Publica":
            query = db.liceo.tipo=="Publico"
        elif request.vars.tipoInstitucion == "Subsidiada":
            query = db.liceo.tipo=="Subsidiado"

        if request.vars.Sede != "Todas":
            query = query & (db.liceo.sede==request.vars.Sede)


        session.consulta = db(query).select(db.liceo.nombre,db.liceo.tipo,
                      db.liceo.sede, db.liceo.telefono, db.liceo.direccion,
                      orderby=db.liceo.nombre)

        redirect(URL('resultadosConsulta'))
    #######################
    # Para los desplegables
    #######################

    ordenAlfabeticoSedes = db.sede.zona.lower()
    sedes = db(db.sede.id>0).select(orderby = ordenAlfabeticoSedes)

    ##########################
    # Fin de los desplegables
    ##########################
    return dict(sedes=sedes)

@auth.requires_membership('Administrador')
@auth.requires_login()
def resultadosConsulta():
    consulta = session.consulta
    session.consulta = None
    return dict(consulta=consulta)

@auth.requires_membership('Administrador')
@auth.requires_login()
def modificarInstitucion():
    #######################
    # Para los desplegables
    #######################

    ordenAlfabeticoLiceos = db.liceo.nombre.lower()
    ordenAlfabeticoSedes = db.sede.zona.lower()
    ordenAlfabeticoCohortes = db.cohorte.identificador.lower()

    liceos = db(db.liceo.id>0).select(orderby = ordenAlfabeticoLiceos)
    sedes = db(db.sede.id>0).select(orderby = ordenAlfabeticoSedes)
    profesores = db(db.profesor.id>0).select()
    cohortes = db(db.cohorte.id>0).select(orderby = ordenAlfabeticoCohortes)

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
    if request.vars.ci != auth.user.username:
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
                response.flash = 'No hay un usuario para esta cédula'
    else:
        response.flash = "No puede modificarse usted mismo con esta opción."

    return dict()

@auth.requires_membership('Administrador')
@auth.requires_login()
def modificarEstudiante():
    usuario = db(db.usuario.username==session.cedula).select()[0]
    estudiante = db(db.estudiante.ci==session.cedula).select()[0]
    errorPromedio = False

    cohorte = estudiante.cohorte

    eximido = False
    if db(db.exime.ci_estudiante==estudiante.ci).select():
        eximido = True

    if request.vars:
        if ((not(db(db.usuario.username==request.vars.cedula).select()) and
            request.vars.cedula!=usuario.username) or
            (request.vars.cedula==usuario.username)):
            # Chequemos el limite de estudiantes eximidos para el liceo
            if (not(eximido)and (request.vars.eximido=="True") and
                not(db(db.exime.ci_estudiante==estudiante.ci).select())):
                db.exime.insert(ci_estudiante=estudiante.ci, liceo=estudiante.nombre_liceo,
                                cohorte=estudiante.cohorte)
                eximido=True
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

            if errorPromedio:
                response.flash = "Modificado con éxito. Hubo un error en el Promedio"
            else:
                response.flash = "Modificado con èxito"
        else:
            response.flash = "Ya hay un usuario con esa cédula"

    #######################
    # Para los desplegables
    #######################

    ordenAlfabeticoLiceos = db.liceo.nombre.lower()
    ordenAlfabeticoSedes = db.sede.zona.lower()
    ordenAlfabeticoCohortes = db.cohorte.identificador.lower()

    liceos = db(db.liceo.id>0).select(orderby = ordenAlfabeticoLiceos)
    cohortes = db(db.cohorte.id>0).select(orderby = ordenAlfabeticoCohortes)

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
        if ((not(db(db.usuario.username==request.vars.cedula).select()) and
            request.vars.cedula!=usuario.username) or
            (request.vars.cedula==usuario.username)):
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
            response.flash = "Modificado con éxito"
        else:
            response.flash = "Ya hay un usuario con esa cédula"

    # Para los desplegables
    ordenAlfabeticoSedes = db.sede.zona.lower()
    sedes = db(db.sede.id>0).select(orderby = ordenAlfabeticoSedes)
    return dict(usuario=usuario,sedes=sedes,representante=representante)

@auth.requires_membership('Administrador')
@auth.requires_login()
def modificarRepresentanteLiceo():
    representante = db(db.representante_liceo.ci==session.cedula).select()[0]
    usuario = db(db.usuario.username==session.cedula).select()[0]
    if request.vars:
        if ((not(db(db.usuario.username==request.vars.cedula).select()) and
            request.vars.cedula!=usuario.username) or
            (request.vars.cedula==usuario.username)):
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
            response.flash = "Modificado con éxito"
        else:
            response.flash = "Ya hay un usuario con esa cédula"

    # Para los desplegables
    ordenAlfabeticoLiceos = db.liceo.nombre.lower()
    liceos = db(db.liceo.id>0).select(orderby = ordenAlfabeticoLiceos)

    return dict(usuario=usuario,liceos=liceos,representante=representante)

@auth.requires_membership('Administrador')
@auth.requires_login()
def modificarAdmin():
    usuario = db(db.usuario.username==session.cedula).select()[0]

    if request.vars:
        if ((not(db(db.usuario.username==request.vars.cedula).select()) and
            request.vars.cedula!=usuario.username) or
            (request.vars.cedula==usuario.username)):
            db(db.usuario.username==session.cedula).update(first_name=request.vars.nombres)
            db(db.usuario.username==session.cedula).update(last_name=request.vars.apellidos)
            db(db.usuario.username==session.cedula).update(email=request.vars.email)
            db(db.usuario.username==session.cedula).update(username=request.vars.cedula) # La cedula se actualiza de ultimo
            response.flash = "Modificado exitosamente"

            # Para actualizar sin recargar
            usuario = db(db.usuario.username==session.cedula).select()[0]
        else:
            response.flash = "Ya hay un usuario con esa cédula"
    return dict(usuario=usuario)

@auth.requires_membership('Administrador')
@auth.requires_login()
def modificarProfesor():
    usuario = db(db.usuario.username==session.cedula).select()[0]
    profesor = db(db.profesor.ci==session.cedula).select()[0]

    if request.vars:
        if ((not(db(db.usuario.username==request.vars.cedula).select()) and
            request.vars.cedula!=usuario.username) or
            (request.vars.cedula==usuario.username)):
            # Si cambia la cedula, actualizamos el profesor, el username del usuario y restablecemos la contraseña
            if db(db.profesor.ci==session.cedula).select()[0].ci != request.vars.cedula:
                db(db.profesor.ci==session.cedula).update(ci=request.vars.cedula)
                db(db.usuario.username==session.cedula).update(username=request.vars.cedula)
                db(db.usuario.username==session.cedula).update(password=db.usuario.password.validate(request.vars.cedula)[0])
                session.cedula = request.vars.cedula

            db(db.usuario.username==session.cedula).update(first_name=request.vars.nombres)
            db(db.usuario.username==session.cedula).update(last_name=request.vars.apellidos)
            db(db.usuario.username==session.cedula).update(email=request.vars.email)
            response.flash = "Modificado con éxito"

            # Para actualizar sin recargar
            usuario = db(db.usuario.username==session.cedula).select()[0]
            profesor = db(db.profesor.ci==session.cedula).select()[0]
        else:
            response.flash = "Ya hay un usuario con esa cédula"

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

# Para generar csv
def csv_export(records, column_names, fields, mode = 'dal'):
    """Export DAL result set, list of dicts or list of lists to CSV stream for returning to user
    Arguments:
    records = the data to be returned
    column_names (list)= the column names/headings for the first row in the CSV file
                    Example ['First Name', 'Last Name', 'Email']
    fields (list) = the names of the fields (as they appear in records) in the order they
                    should be in the CSV. Example ['f_name', 'l_name', 'email']
                    or ['table_a.f_name', 'table_a.l_name', 'table_b.email']
                    If mode = 'list' and your records are in the correct order then fields may be None
                    otherwise use [1,3,0] if you list is in a different order
    mode (string) = what type of data is in records? 'dal' (Default), 'dict' or 'list'
                    'dal' if records came from a regular dal query (Default)
                    'dict' if records are a list of dicts (for example using db.executesql() with as_dict = True)
                    'list' if records are a list of lists/tuples (for example using db.executesql() with as_dict = False)

    """

    #create fake file object
    import cStringIO
    file = cStringIO.StringIO()
    #setup csv writer
    import csv
    csv_file = csv.writer(file)
    #write first row withspecified column headings/names
    csv_file.writerow(column_names)
    #which mode - dal or dict?
    if mode.lower() == 'dal' or mode.lower() == 'dict':
        for record in records:
            csv_file.writerow([record[field] for field in fields])
    elif mode.lower() == 'list':
        if fields == None:
            csv_file.writerows(records)
        else:
            for record in records:
                csv_file.writerow([record[field] for field in fields])
    return file

def modificarProcesos():
    cargaEstudiantes = db(db.periodo.nombre=="Carga Estudiantes").select()[0].Activo
    testVocacional = db(db.periodo.nombre=="Test Vocacional").select()[0].Activo
    modificarProcesos = FORM()
    if modificarProcesos.accepts(request.vars,formname="modificarProcesos"):
        db(db.periodo.nombre=="Carga Estudiantes").update(Activo=request.vars.cargaEstudiantes)
        db(db.periodo.nombre=="Test Vocacional").update(Activo=request.vars.testVocacional)
        response.flash= "Modificado con exito"
        # Actualizar sin recargar
        cargaEstudiantes = db(db.periodo.nombre=="Carga Estudiantes").select()[0].Activo
        testVocacional = db(db.periodo.nombre=="Test Vocacional").select()[0].Activo

    return dict(testVocacional=testVocacional, cargaEstudiantes=cargaEstudiantes)
