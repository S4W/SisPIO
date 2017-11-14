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

@auth.requires_membership('Representante_sede')
@auth.requires_login()
def index():
    ########################
    ###Consula de datos
    ########################
    T.force('es')
    username = auth.user.username
    representante_sede=db(db.representante_sede.ci==username).select().first()
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

    if formDatosBasicos.process(session=None, formname='perfil basico del Representante PIO de sede', keepvalues=True).accepted:
        response.flash = 'El formulario fue aceptado exitosamente.'

    elif formDatosBasicos.errors:
        #error = True
        response.flash = 'Hay un error en un campo.'

    formCoordinadorPio = SQLFORM.factory(
        Field('ci',
            type='string',
            notnull=True,
            default=representante_sede.ci,
            requires=db.representante_sede.ci.requires,
            label='ci'
            ),
        Field('first_name' +  'last_name',
            type='string',
            default=usuario.first_name + " " + usuario.last_name,
            requires=db.usuario.first_name.requires and db.usuario.last_name.requires,
            label='nombre'
            ),
        Field('sede',
            type='string',
            default=representante_sede.sede,
            requires=db.representante_sede.sede.requires,
            label='sede'
            ),
        Field('email',
            type='date',
            default=usuario.email,
            requires=db.usuario.email.requires,
            label='email'),
        readonly = True
        )

    if formCoordinadorPio.process(session=None, formname='perfil del Representante PIO de sede', keepvalues=True).accepted:
        response.flash = 'El formulario fue aceptado exitosamente.'

    elif formCoordinadorPio.errors:
        #error = True
        response.flash = 'Hay un error en un campo.'
    ############################
    ###fin de Consula de datos
    ############################

    return dict(formDatosBasicos=formDatosBasicos, formCoordinadorPio=formCoordinadorPio)
