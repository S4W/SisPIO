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

@auth.requires_membership('Estudiante')
@auth.requires_login()
def index():

    ########################
    ###Consula de datos
    ########################
    T.force('es')
    username = auth.user.username
    estudiante=db(db.estudiante.ci==username).select().first()
    usuario = db(db.usuario.username==username).select().first()
    #tipo=""
    #error = False

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

    if formDatosBasicos.process(session=None, formname='perfil basico del Estudiante', keepvalues=True).accepted:
        response.flash = 'El formulario fue aceptado exitosamente.'

    elif formDatosBasicos.errors:
        #error = True
        response.flash = 'Hay un error en un campo.'

    formEstudiante = SQLFORM.factory(
        Field('ci',
            type='string',
            notnull=True,
            default=estudiante.ci,
            requires=db.estudiante.ci.requires,
            label='ci'
            ),
        Field('first_name',
            type='string',
            default=usuario.first_name,
            requires=db.usuario.first_name.requires and db.usuario.last_name.requires,
            label='nombre'
            ),
        Field('last_name',
            type='string',
            default=usuario.last_name,
            requires=db.usuario.first_name.requires and db.usuario.last_name.requires,
            label='apellido'
            ),

        Field('sexo',
            type='string',
            default=estudiante.sexo,
            requires=db.estudiante.sexo.requires,
            label='sexo'
            ),
        Field('fecha_nacimiento',
            type='date',
            default=estudiante.fecha_nacimiento,
            requires=db.estudiante.fecha_nacimiento.requires,
            label='fecha_de_nacimiento'
            ),
        Field('promedio',
            type='string',
            default= estudiante.promedio,
            requires=db.estudiante.promedio.requires,
            label='promedio'
            ),
        Field('nombre_liceo',
            type='string',
            default="            "+estudiante.nombre_liceo,
            requires=db.estudiante.nombre_liceo.requires,
            label='nombre_liceo'
            ),
        Field('email',
            type='string',
            default=usuario.email,
            requires=db.usuario.email.requires,
            label='email',
            ),
        Field('telefono_habitacion',
            type='integer',
            default=estudiante.telefono_habitacion,
            requires=db.estudiante.telefono_habitacion.requires,
            label='telefono_habitacion',
            ),
        Field('direccion',
            type='string',
            default= estudiante.direccion,
            requires=db.estudiante.direccion.requires,
            label='direccion'),
        readonly = True
        )

    if formEstudiante.process(session=None, formname='perfil del Estudiante', keepvalues=True).accepted:
        response.flash = 'El formulario fue aceptado exitosamente.'

    elif formEstudiante.errors:
        #error = True
        response.flash = 'Hay un error en un campo.'

    ############################
    ###fin de Consula de datos
    ############################

    return dict(formDatosBasicos = formDatosBasicos, formEstudiante = formEstudiante)

def testVocacional():
    periodoActivo = db(db.periodo.nombre=="Test Vocacional").select()[0].Activo
    userId = db(db.usuario.username==auth.user.username).select()[0].id

    testVocacional = FORM()
    if testVocacional.accepts(request.vars,formname='testVocacional'):
        if ((request.vars.primeraCarrera!=request.vars.segundaCarrera) and
            (request.vars.primeraCarrera!=request.vars.terceraCarrera) and
            (request.vars.terceraCarrera!=request.vars.segundaCarrera)):

            if (db((db.carrera.nombre==request.vars.primeraCarrera)&(db.carrera.dictada_en_la_USB==True)).select() or
                    db((db.carrera.nombre==request.vars.segundaCarrera)&(db.carrera.dictada_en_la_USB==True)).select() or
                    db((db.carrera.nombre==request.vars.terceraCarrera)&(db.carrera.dictada_en_la_USB==True)).select()):
                        db(db.estudiante.ci==auth.user.username).update(estatus="Seleccionado")
                        db.auth_membership.insert(user_id = userId, group_id= 1)                # Agregar permisos de estudiante (group_id=1)
                        session.flash = "Felicidades, usted es un alumno candidato para cursar el PIO. Por favor complete sus datos en \"Mi Perfil\""
                        redirect(URL('index'))
            else:
                db(db.estudiante.ci==auth.user.username).update(estatus="Inactivo")
                session.flash = "Lo sentimos, usted no es candidato para cursar el PIO"
                redirect(URL('falloTest'))
        else:
            response.flash = "Selecciona tres carreras distintas"
    # Desplegables
    ordenAlfabeticoCarreras = db.carrera.nombre
    carreras = db(db.carrera.id>0).select(orderby=ordenAlfabeticoCarreras)

    return dict(carreras=carreras,periodoActivo=periodoActivo)

def falloTest():
    return dict()
