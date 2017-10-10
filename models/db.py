# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL('postgres://SisPIO:SisPIO@localhost/SisPIO')
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.settings.table_user_name = 'usuario'

# db.define_table(
#     auth.settings.table_user_name,
#     Field('nombre', length=128, default=''),
#     Field('apellido', length=128, default=''),
#     Field('email', length=128, default=''),
#     Field('username', length=8, default='', unique=True, notnull=True),  # Requerido
#     Field('password', type='password', length=512,            # Requerido
#           readable=False, label='Clave'),
#     Field('registration_key', length=512,                # Requerido
#           writable=False, readable=False, default=''),
#     Field('reset_password_key', length=512,              # Requerido
#           writable=False, readable=False, default=''),
#     Field('registration_id', length=512,                 # Requerido
#           writable=False, readable=False, default=''),

#     primarykey=['username']
#     )

# ## Validadores
# nuevaTablaUsuario = db[auth.settings.table_user_name]
# nuevaTablaUsuario.nombre.requires =   IS_NOT_EMPTY(error_message="Falto nombre de usuario")
# nuevaTablaUsuario.apellido.requires =   IS_NOT_EMPTY(error_message="Falta apellido de usuario")
# nuevaTablaUsuario.password.requires = [CRYPT()]
# nuevaTablaUsuario.email.requires = [IS_EMAIL(error_message=auth.messages.invalid_email)]

# auth.settings.table_user = nuevaTablaUsuario

auth.define_tables(username = True, signature = False, migrate='db.usuario')

db.usuario.username.length = 8

auth.settings.create_user_groups = None

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = 'proppio@usb.ve'
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

db.define_table(
    'liceo',
    # Field('id', type='integer', unique=True, notnull=True),
    Field('nombre', type='string', notnull=True),
    Field('tipo', type='string', notnull=True, requires=[IS_IN_SET(['Publico', 'Subsidiado'])]),

    # primarykey=['id'],
    migrate='db.liceo'
    )

db.define_table(
    'estudiante',
    Field('ci', type='string', length=8, notnull=True, unique=True, requires=IS_IN_DB(db, db.usuario.username)),
    Field('promedio', type='integer', notnull=True),
    Field('direccion', type='string', default=''),
    Field('fecha_nacimiento', type='date', requires=IS_EMPTY_OR(IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy'))),
    Field('sexo', type='string', length=1, requires=IS_IN_SET(['Masculino', 'Femenino'])),
    Field('estatus', type='string', default='pre-inscrito', requires=IS_IN_SET(['Pre-inscrito', 'Seleccionado', 'Activo', 'Inactivo', 'Finalizado'])),
    Field('cohorte', type='string', default=''),
    Field('ci_representante', type='string', length=8, default=''),
    Field('nombre_representante', type='string', default=''),
    Field('apellido_representante', type='string', default=''),
    Field('correo_representante', type='string', length=128, required=True, default='', requires=IS_EMPTY_OR(IS_EMAIL(error_message='Debe tener un formato válido. EJ: example@org.com'))),
    Field('direccion_representante', type='string', default=''),
    Field('id_liceo', type='reference liceo', required=True),

    # primarykey=['ci'],
    migrate="db.estudiante"
    )

db.define_table(
    'profesor',
    Field('ci', type='string', length=8, notnull=True, unique=True, requires=IS_IN_DB(db, db.usuario.username)),

    # primarykey=['ci'],
    migrate="db.profesor"
    )

db.define_table(
    'representante_sede',
    Field('ci', type='string', length=8, notnull=True, unique=True, requires=IS_IN_DB(db, db.usuario.username)),
    Field('sede', 'string'),

    # primarykey=['ci'],
    migrate="db.representante_sede"
    )

db.define_table(
    'representante_liceo',
    Field('ci', type='string', length=8, notnull=True, unique=True, requires=IS_IN_DB(db, db.usuario.username)),
    Field('id_liceo', type='reference liceo', required=True),

    # primarykey=['ci'],
    migrate="db.representante_liceo"
    )


db.define_table(
    'materia',
    # Field('id', type='integer', length=128, unique=True, notnull=True),
    Field('nombre', type='string', notnull=True),
    Field('ci_profesor', type='string', requires=IS_IN_DB(db, db.profesor.ci)),

    # primarykey=['id'],
    migrate='db.materia'
    )

db.define_table(
    'cursa',
    Field('ci_estudiante', type='string', requires=IS_IN_DB(db, db.estudiante.ci)),
    Field('id_materia', type='reference materia'),
    Field('notas', type='list:integer'),

    # primarykey=['ci_estudiante','id_materia'],
    migrate='db.cursa'
    )

db.define_table(
    'asistencia',
    Field('ci_estudiante', type='string', requires=IS_IN_DB(db, db.estudiante.ci)),
    Field('id_materia', type='reference materia'),
    Field('fecha_clase', type='date'),

    # primarykey=['ci_estudiante','id_materia','fecha_clase'],
    migrate='db.asistencia'
    )

db.define_table(
    'carrera',
    Field('id', type='integer', unique=True, notnull=True),
    Field('nombre', type='string'),

    # primarykey=['id'],
    migrate='db.carrera'
    )

db.define_table(
    'exime',
    Field('ci_estudiante', type='string', length=8, notnull=True, requires=IS_IN_DB(db, db.estudiante.ci)),
    Field('ci_representante_liceo', type='string', length=8, notnull=True, requires=IS_IN_DB(db, db.representante_liceo.ci)),
    Field('cohorte', type='string', notnull=True),

    # primarykey=['ci_estudiante', 'ci_representante_liceo'],
    migrate='db.exime'
    )

db.define_table(
    'periodos',
    Field('nombre', type='string'),
    Field('fecha_inicio', type='date', requires=IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')),
    Field('fecha_fin', type='date', requires=IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')),

    # primarykey=['nombre'],
    migrate='db.periodos'
    )


# db.define_table(
#     'cohorte',
#     Field('id', type='string'),
#     Field('estado', type='boolean')

#     primarykey=['id'],
#     migrate='db.cohorte'
#     )


if not db(db.usuario.username == 'admin').select():
    id_usuario = db.usuario.insert(username='admin', password=CRYPT()('admin')[0], first_name='SisPIO', last_name='Admin', email='admin@usb.ve')

    estudiante = auth.add_group(role='Estudiante', description='description')
    profesor = auth.add_group(role='Profesor', description='description')
    representante_liceo = auth.add_group(role='Representante_liceo', description='description')
    representante_sede = auth.add_group(role='Representante_sede', description='description')
    admin = auth.add_group(role='Administrador', description='description')

    auth.add_permission(estudiante, 'Estudiante')

    auth.add_permission(profesor, 'Estudiante')
    auth.add_permission(profesor, 'Profesor')

    auth.add_permission(representante_liceo, 'Estudiante')
    auth.add_permission(representante_liceo, 'Representante_liceo')

    auth.add_permission(representante_sede, 'Estudiante')
    auth.add_permission(representante_sede, 'Representante_sede')

    auth.add_permission(admin, 'Estudiante')
    auth.add_permission(admin, 'Representante_liceo')
    auth.add_permission(admin, 'Profesor')
    auth.add_permission(admin, 'Representante_sede')
    auth.add_permission(admin, 'Administrador')
