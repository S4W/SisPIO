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
def cargaArchivo():
    erroresCarga = [] # Los errores en la carga van aqui
    cargaExitosa = [] # Los usuarios agregados exitosamente van aqui
    cohorte = db(db.cohorte.status=="Activa").select()[0].identificador # Cohorte Actual
    liceo = db(db.representante_liceo.ci == auth.user.username).select()[0].nombre_liceo # Liceo al que pertenece el representante logiado

    formularioArchivo = FORM()
    periodoActivo = db(db.periodo.nombre=="Carga Estudiantes").select()[0].Activo

    if periodoActivo:
        if formularioArchivo.accepts(request.vars,formname='formularioArchivo'): # Chequeamos si hay un archivo cargado
            archivo =request.vars.fileToUpload.filename.split(".")  # Separamos el nombre del archivo de la extension
            nombreArchivo, extension = archivo[0], archivo[1]
            if extension == "csv":          # Chequeamos la extension del archivo
                f = request.vars.fileToUpload.file      # Archivo cargado
                texto = f.read().splitlines()           # Leer el archivo
                cabecera = texto[0].split(";")          # Extraemos la cabecera
                if len(cabecera) == 5 and len(texto)>=2:
                    texto.remove(texto[0])                  # Eliminamos del texto la cabecera para no iterar sobre ella
                    texto.remove(texto[0])
                    if (cabecera[0]=="C.I." and cabecera[1]=='Nombres' and
                    cabecera[2]=='Apellidos' and cabecera[3]=='Promedio (00.00)'): # Verificamos que la cabecera y la linea del liceo tenga el formato correcto
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
                                            if float(i[3]) >= db(db.promedio_ingreso).select()[0].promedio:
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
                                                erroresCarga.append([i,"El promedio es menor al requerido para ingresar al PIO"])
                                        else:
                                            erroresCarga.append([i,"Cédula incorrecta"])                                            # Error de Carga
                                    else:
                                        erroresCarga.append([i,"Su liceo no esta en la base de datos. Contacte al administrador"])  # Error de Carga
                                else:
                                    erroresCarga.append([i,"El promedio debe ser un numero entre 0 y 20"])                          # Error de Carga
                            else:
                                erroresCarga.append([i,"Ya existe un usuario en el sistema con esta cédula"])                       # Error de Carga
                    else:
                        response.flash = "Formato de los datos del archivo inválido. Consulte el manual"               # Error de Carga
                else:
                    response.flash = "Formato de los datos del archivo inválido. Consulte el manual"               # Error de Carga
            else: #Error
                erroresCarga.append("El formato del archivo debe ser \".csv\". Consulte el manual de usuario")
        else:
            pass
    else:
        response.flash = "El periodo para cargar estudiantes ha finalizado"
    return dict(erroresCarga=erroresCarga, cargaExitosa=cargaExitosa,periodoActivo=periodoActivo)

@auth.requires_membership('Representante_liceo')
@auth.requires_login()
def agregarManual():
    periodoActivo = db(db.periodo.nombre=="Carga Estudiantes").select()[0].Activo
    cohorte = db(db.cohorte.status=="Activa").select()[0].identificador # Cohorte Actual
    liceo = db(db.representante_liceo.ci == auth.user.username).select()[0].nombre_liceo # Liceo al que pertenece el representante logiado
    if periodoActivo:
        if request.vars:
            if (not(db(db.usuario.username==request.vars.cedula).select()) and
                not(db(db.estudiante.ci==request.vars.cedula).select())):
                promedio = float(request.vars.PromedioEntero)+(float(request.vars.PromedioDecimal)/100)
                if 0 <= promedio <= 20:
                    if promedio >= db(db.promedio_ingreso).select()[0].promedio:
                        db.usuario.insert(first_name = request.vars.nombres, last_name = request.vars.apellidos,
                                          email = "", username = request.vars.cedula,
                                          password = db.usuario.password.validate(request.vars.cedula)[0],
                                          registration_key = "", reset_password_key = "",
                                          registration_id = "" )
                        db.estudiante.insert(ci=request.vars.cedula, promedio=promedio,
                                             direccion="", telefono_habitacion="", telefono_otro="",
                                             fecha_nacimiento="", sexo="", estatus="Pre-inscrito",
                                             cohorte=cohorte, ci_representante="", nombre_representante="",
                                             apellido_representante="", sexo_representante="",
                                             correo_representante="", direccion_representante="",
                                             nombre_liceo=liceo, telefono_representante_oficina="",
                                             telefono_representante_otro="", sufre_enfermedad="",
                                             enfermedad="", indicaciones_enfermedad="")
                        response.flash = "Agregado exitosamente"
                    else:
                        response.flash = "El promedio es menor al requerido para ingresar al PIO"
                else:
                    response.flash = "Promedio Inválido"
            else:
                response.flash = "Ya existe un usuario con esa cédula"
    else:
        response.flash = "El periodo para cargar estudiantes ha finalizado"
    return dict(periodoActivo=periodoActivo)

@auth.requires_membership('Representante_liceo')
@auth.requires_login()
def modificarUsuario():
    liceoRepresentante = db(db.representante_liceo.ci == auth.user.username).select()[0].nombre_liceo # Liceo al que pertenece el representante logiado
    if request.vars:
        if db(db.estudiante.ci==request.vars.ci).select():
            liceoEstudiante = db(db.estudiante.ci==request.vars.ci).select()[0].nombre_liceo
            if liceoEstudiante == liceoRepresentante:
                session.cedula = request.vars.ci
                redirect(URL('modificarEstudiante'))
            else:
                response.flash = "Ese estudiante no pertenece al liceo que usted representa"
        else:
            response.flash = "No hay un estudiante con esa cédula"

    return dict()

@auth.requires_membership('Representante_liceo')
@auth.requires_login()
def modificarEstudiante():
    usuario = db(db.usuario.username==session.cedula).select()[0]
    estudiante = db(db.estudiante.ci==session.cedula).select()[0]
    errorPromedio = False

    liceo = db(db.representante_liceo.ci == auth.user.username).select()[0].nombre_liceo # Liceo al que pertenece el representante logiado
    cohorte = estudiante.cohorte
    limiteEximidos = 0
    if db(db.liceo.nombre==liceo).select()[0].tipo == "Publico":
        limiteEximidos = 3
    elif db(db.liceo.nombre==liceo).select()[0].tipo == "Subsidiado":
        limiteEximidos = 1

    errorExime = False
    errorYaEximido = False

    numeroEximidos = db((db.exime.cohorte==cohorte) & (db.exime.liceo==liceo)).count()

    eximido = False
    if db(db.exime.ci_estudiante==estudiante.ci).select():
        eximido = True

    if request.vars:

        if ((not(db(db.usuario.username==request.vars.cedula).select()) and
            request.vars.cedula!=usuario.username) or
            (request.vars.cedula==usuario.username)):
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
                response.flash = "Modificado con éxito. Hubo un error en el Promedio"
            elif not(errorPromedio) and errorExime:
                response.flash = "Datos modificado exitosamente, sin embargo no se \
                                  puede eximir este alumno ya que se excedió el limite \
                                  de eximidos de su liceo para esta cohorte"
            elif errorPromedio and errorExime:
                response.flash = "Datos modificado exitosamente, sin embargo no se \
                                  puede eximir este alumno ya que se excedió el limite \
                                  de eximidos de su liceo para esta cohorte. Hubo un error\
                                  en el promedio"
            elif not(errorPromedio) and errorYaEximido:
                response.flash = "Datos modificado exitosamente, sin embargo no se \
                                  puede eximir este alumno porque ya está eximido"
            elif errorPromedio and errorYaEximido:
                response.flash = "Datos modificado exitosamente, sin embargo no se \
                                  puede eximir este alumno poruqe ya está eximido. \
                                  Hubo un error en el promedio"

            else:
                response.flash = "Modificado con éxito"

        else:
            response.flash = "Ya hay un usuario con esa cédula"
    #######################
    # Para los desplegables
    #######################

    ordenAlfabeticoCohortes = db.cohorte.identificador.lower()
    cohortes = db(db.cohorte.id>0).select(orderby = ordenAlfabeticoCohortes)

    ##########################
    # Fin de los desplegables
    ##########################
    return dict(usuario=usuario,estudiante=estudiante,cohortes=cohortes,
                eximido=eximido)

@auth.requires_membership('Representante_liceo')
@auth.requires_login()
def consultar():
    consultarTodo = FORM()
    formularioConsulta = FORM()
    liceo = db(db.representante_liceo.ci == auth.user.username).select()[0].nombre_liceo # Liceo al que pertenece el representante logiado
    if consultarTodo.accepts(request.vars,formname="consultarTodo"):
        session.consulta = db((db.estudiante.nombre_liceo==liceo) &
                     (db.estudiante.ci==db.usuario.username)).select(
                      db.usuario.username,db.usuario.first_name,db.usuario.last_name,
                      db.estudiante.promedio,db.estudiante.cohorte,db.estudiante.estatus,
                      orderby=db.usuario.username)

        redirect(URL('resultadosConsulta'))

    elif formularioConsulta.accepts(request.vars,formname="formularioConsulta"):

        # Filtros
        query = (db.estudiante.nombre_liceo==liceo) & (db.estudiante.ci==db.usuario.username)
        if request.vars.Cohorte:
            query = query & (db.estudiante.cohorte==request.vars.Cohorte)
        if request.vars.Estado:
            query = query & (db.estudiante.estatus==request.vars.Estado)
        if request.vars.Sexo:
            query = query & (db.estudiante.sexo==request.vars.Sexo)
        if request.vars.MenorPromedioEntero != "0" or request.vars.MenorPromedioDecimal != "0":
            query = query & (db.estudiante.promedio<=(int(request.vars.MenorPromedioEntero)+(float(request.vars.MenorPromedioDecimal))/100))
        if request.vars.MayorPromedioEntero != "0" or request.vars.MayorPromedioDecimal != "0":
            query = query & (db.estudiante.promedio>=int(request.vars.MayorPromedioEntero)+(float(request.vars.MayorPromedioDecimal)/100))

        # Orden
        orden = None
        if request.vars.tipoOrden == "cedula":
            orden = db.usuario.username
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
                                        orderby=orden)
        elif request.vars.tipoEstudiante == "No eximidos":
            session.consulta = db(query)(~db.estudiante.ci.belongs(
                                db(db.exime.ci_estudiante)._select(db.exime.ci_estudiante))
                                ).select(db.usuario.username,db.usuario.first_name,
                                    db.usuario.last_name,db.estudiante.cohorte,
                                    db.estudiante.promedio,db.estudiante.estatus,
                                    orderby=orden)
        elif request.vars.tipoEstudiante == "Eximidos":
            query = query & (db.estudiante.ci==db.exime.ci_estudiante)
            session.consulta = db(query).select(db.usuario.username,db.usuario.first_name,
                                        db.usuario.last_name,db.estudiante.cohorte,
                                        db.estudiante.promedio,db.estudiante.estatus,
                                        orderby=orden)
        redirect(URL('resultadosConsulta'))
    #######################
    # Para los desplegables
    #######################

    ordenAlfabeticoCohortes = db.cohorte.identificador.lower()

    cohortes = db(db.cohorte.id>0).select(orderby = ordenAlfabeticoCohortes)

    ##########################
    # Fin de los desplegables
    ##########################
    return dict(cohortes=cohortes)

@auth.requires_membership('Representante_liceo')
@auth.requires_login()
def resultadosConsulta():
    consulta = session.consulta
    session.consulta = None
    return dict(consulta=consulta)

@auth.requires_membership('Representante_liceo')
@auth.requires_login()
def perfil():

    formularioPerfil = FORM()
    user = db(db.usuario.username==auth.user.username).select()[0]
    if formularioPerfil.accepts(request.vars,formname="formularioPerfil"):    # Verificamos que se haya introducido una cedula

        if request.vars.cedula == auth.user.username:
            db(db.usuario.username==user.username).update(first_name=request.vars.nombre)
            db(db.usuario.username==user.username).update(last_name=request.vars.apellido)
            db(db.usuario.username==user.username).update(email=request.vars.email)
            user = db(db.usuario.username==auth.user.username).select()[0]
            response.flash = "Perfil Modificado exitosamente"
        else:
            response.flash = "Ya existe un usuario con la cédula de identidad"

    return dict(user=user)

@auth.requires_membership('Representante_liceo')
@auth.requires_login()
def noticias():
    return dict()

@auth.requires_membership('Representante_liceo')
@auth.requires_login()
def cambioContrasena():

    cambiarContrasena = FORM()
    username = auth.user.username

    if cambiarContrasena.accepts(request.vars, formname="cambiarContrasena"):
        if db.usuario.password.validate(request.vars.contrasenaRL) == (db(db.usuario.username==username).select().first().password, None):
            if request.vars.passwordRL == request.vars.confirm_passwordRL:
                if request.vars.contrasenaRL != request.vars.passwordRL:
                    db(db.usuario.username==username).update(password=db.usuario.password.validate(request.vars.passwordRL)[0])
                    response.flash = "Contraeña cambiado exitosamente"
                else:
                    response.flash = "La contraseña a cambiar no puede igual a la contraseña actual"
            else:
                response.flash = "Las constraseña nueva no coincide con la contraseña confirmada"
        else:
            response.flash = "La contraseña actual no es la perteneciente a la cuenta"

    return dict(cambiarContrasena=cambiarContrasena)

@auth.requires_membership('Representante_liceo')
@auth.requires_login()
def generarComprobante():
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
