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
