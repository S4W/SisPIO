# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    if not(request.args):
        if auth.is_logged_in():
            redirect(URL('redireccionando'))
        else:
            redirect(URL('index'))
    else:
        if request.args[0] == 'login':
            if auth.is_logged_in():
                redirect(URL('redireccionando'))
            else:
                redirect(URL('index'))
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

@auth.requires_login()
def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def index():
    if auth.is_logged_in():
        redirect(URL('default', 'user', args='logout')) # Si ya hay un usuario conectado, desconectarlo
    return dict(form=auth.login())

def redireccionando():
    if auth.is_logged_in():
        if 'Administrador' in auth.user_groups.values():
            redirect(URL('admin'))
        elif 'Estudiante' in auth.user_groups.values():
            redirect(URL('welcome'))
        elif 'Profesor' in auth.user_groups.values():
            redirect(URL('profesor'))
        elif 'Representante_liceo' in auth.user_groups.values():
            redirect(URL('coordinadorLiceo'))
        elif 'Representante_sede' in auth.user_groups.values():
            redirect(URL('coordinadorPio'))
        else:
            redirect(URL('default', 'user', args='logout'))
    else:
        redirect(URL('index'))
    return dict()

@auth.requires_membership('Administrador')
@auth.requires_login()
def admin():

    ##################
    # Carga de archivo
    ##################
    aceptado = "hola"

    formularioArchivo = FORM(
                            INPUT(_name='tituloArchivo', _type='text'),
                            INPUT(_name='archivo', _type='file')
                            )
    if formularioArchivo.accepts(request.vars,formname='formularioArchivo'):
        aceptado = True
    else:
        aceptado= False


    ########################
    ###Consula de datos
    ########################
    T.force('es')
    username = auth.user.username
    usuario = db(db.usuario.username==username).select().first()
    #tipo=""
    #error = False

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

    return dict(formAdministrador=formAdministrador, aceptado = aceptado)

@auth.requires_membership('Profesor')
@auth.requires_login()
def profesor():
    return dict()

@auth.requires_membership('Representante_liceo')
@auth.requires_login()
def coordinadorLiceo():

    ########################
    ###Consula de datos
    ########################
    T.force('es')
    username = auth.user.username
    representante_liceo=db(db.representante_liceo.ci==username).select().first()
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

    if formDatosBasicos.process(session=None, formname='perfil basico del Representante liceo de sede', keepvalues=True).accepted:
        response.flash = 'El formulario fue aceptado exitosamente.'

    elif formDatosBasicos.errors:
        #error = True
        response.flash = 'Hay un error en un campo.'

    formCoordinadorLiceo = SQLFORM.factory(
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

    if formCoordinadorLiceo.process(session=None, formname='perfil del Representante Liceo de sede', keepvalues=True).accepted:
        response.flash = 'El formulario fue aceptado exitosamente.'

    elif formCoordinadorLiceo.errors:
        #error = True
        response.flash = 'Hay un error en un campo.'
    ############################
    ###fin de Consula de datos
    ############################

    return dict(formCoordinadorLiceo=formCoordinadorLiceo, formDatosBasicos=formDatosBasicos)

@auth.requires_membership('Representante_sede')
@auth.requires_login()
def coordinadorPio():

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

@auth.requires_membership('Estudiante')
@auth.requires_login()
def welcome():

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
