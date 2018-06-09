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
	db = DAL('postgres://SisPIO:SisPIO@localhost/SisPIO', migrate=True)
	# db = DAL('sqlite://storage.sqlite')
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

auth.define_tables(username = True, signature = False, migrate='db.usuario')

db.usuario.username.length = 8
db.usuario.password.requires = CRYPT()
db.usuario.username.requires = IS_MATCH('^[0-9]*$|^admin$', error_message='Numero de Cedula Invalido.')
db.usuario.first_name.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]([a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+[\s-]?[a-zA-ZñÑáéíóúÁÉÍÓÚ\s][a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+)*$', error_message='Nombre No Valido. Debe ser no vacío y contener sólo letras, guiones o espacios.')
db.usuario.last_name.requires = IS_MATCH('^[a-zA-ZñÑáéíóúÁÉÍÓÚ]([a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+[\s-]?[a-zA-ZñÑáéíóúÁÉÍÓÚ\s][a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+)*$', error_message='Apellido No Valido. Debe ser no vacío y contener sólo letras, guiones o espacios.')

auth.settings.create_user_groups = None

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------

from gluon.tools import Mail

# mail = Mail()
mail = auth.settings.mailer
mail.settings.server = "smtp.gmail.com:587"
mail.settings.sender = "piosistema@gmail.com"
mail.settings.login =  "piosistema@gmail.com:rokgwdmpmoxocpgc"
# mail.settings.server = "mail.latinux.com:587"
# mail.settings.sender = "non-reply@latinux.org"
# mail.settings.login =  "mleandro:L3@ndr0L@t1nux"
mail.settings.tls = True
mail.settings.ssl = False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True

auth.settings.login_url = URL('index')
auth.settings.login_next = URL('redireccionando')

# -------------------------------------------------------------------------
# Tipos de ingreso de estudiantes
# -------------------------------------------------------------------------
# Lista de tipos de ingresos.
TIPOS_INGRESO = myconf.take('tipos_estudiante')

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
	'sede',
	Field('zona', type='string', notnull=True, unique=True, default=''),

#	migrate=False
	)


db.define_table(
	'liceo',
	Field('nombre', type='string', notnull=True, unique=True),
	Field('tipo', type='string', notnull=True, requires=IS_IN_SET(['Publico', 'Subsidiado', 'Otro'])),
	Field('sede', type='string', notnull=True, requires=IS_IN_DB(db, db.sede.zona)),
	Field('telefono', type ='string', length=12, requires=IS_MATCH('^((0)?2[0-9]{2}(-)?)?[0-9]{7}$', error_message='Telefono Invalido.')),
	Field('direccion', type='text', default=''),

#	migrate=False
	)


db.define_table(
	'cohorte',
	Field('identificador', type='string', unique=True, requires=IS_MATCH('^[0-9]{4}/[0-9]{4}$', error_message='Formato de Cohorte Invalido.')),
	Field('status', type='string', default='Inactiva', requires=IS_IN_SET(['Activa', 'Inactiva', 'Proxima'])),

#	migrate=False
	)

db.define_table(
	'estudiante',
	Field('ci', type='string', notnull=True, unique=True, requires=[IS_IN_DB(db, db.usuario.username), IS_MATCH('^[0-9]*$', error_message='Numero de Cedula Invalido.')]),
	Field('promedio', type='double', notnull=True, requires=IS_FLOAT_IN_RANGE(minimum=0.01,maximum=20, error_message='Promedio no valido.')),
	Field('direccion', type='text', default=''),
	Field('telefono_habitacion', type ='string', length=12, requires=IS_EMPTY_OR(IS_MATCH('^((0)?2[0-9]{2}(-)?)?[0-9]{7}$', error_message='Telefono Habitación Invalido.'))),
	Field('telefono_otro', type ='string', length=12, requires=IS_EMPTY_OR(IS_MATCH('^((0)?[0-9]{3}(-)?)?[0-9]{7}$', error_message='Telefono Invalido.'))),
	Field('fecha_nacimiento', type='date', requires=IS_EMPTY_OR(IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy'))),
	Field('sexo', type='string', default= 'Masculino', requires=IS_IN_SET(['Masculino', 'Femenino'])),
	Field('nombre_liceo', type='string', required=True, requires=IS_IN_DB(db, db.liceo.nombre)),
	Field('estatus', type='string', default='Pre-inscrito', requires=IS_IN_SET(['Pre-inscrito', 'Seleccionado', 'Activo', 'Inactivo', 'Finalizado'])),
	Field('cohorte', type='string', default='', requires=IS_IN_DB(db, db.cohorte.identificador)),

	Field('ci_representante', type='string', length=8, default='', requires=IS_EMPTY_OR(IS_MATCH('^[0-9]*$', error_message='Numero de Cedula Invalido.'))),
	Field('nombre_representante', type='string', default=''),
	Field('apellido_representante', type='string', default=''),
	Field('sexo_representante', type='string', default='Masculino', requires=IS_IN_SET(['Masculino', 'Femenino'])),
	Field('correo_representante', type='string', length=128, required=True, default='', requires=IS_EMPTY_OR(IS_EMAIL(error_message='Debe tener un formato válido. EJ: example@org.com'))),
	Field('direccion_representante', type='text', default=''),
	Field('telefono_representante_oficina', type ='string', length=12, requires=IS_EMPTY_OR(IS_MATCH('^((0)?2[0-9]{2}(-)?)?[0-9]{7}$', error_message='Telefono Oficina Invalido.'))),
	Field('telefono_representante_otro', type ='string', length=12, requires=IS_EMPTY_OR(IS_MATCH('^((0)?[0-9]{3}(-)?)?[0-9]{7}$', error_message='Telefono Invalido.'))),

	Field('sufre_enfermedad', type='boolean', default=False),
	Field('enfermedad', type='string'),
	Field('indicaciones_enfermedad', type='text'),

	Field('tipo_ingreso', type='string'),

	Field('validado', type='boolean', default=False),

#	migrate=False
	)

db.define_table(
	'representante_sede',
	Field('ci', type='string', notnull=True, unique=True, requires=[IS_IN_DB(db, db.usuario.username), IS_MATCH('^[0-9]*$', error_message='Numero de Cedula Invalido.')]),
	Field('sede', type='string', requires=IS_IN_DB(db, db.sede.zona)),
	Field('telefono', type ='string', length=12, requires=IS_MATCH('^((0)?[0-9]{3}(-)?)?[0-9]{7}$', error_message='Telefono Invalido.')),

#	migrate=False
	)

db.define_table(
	'representante_liceo',
	Field('ci', type='string', notnull=True, unique=True, requires=[IS_IN_DB(db, db.usuario.username), IS_MATCH('^[0-9]*$', error_message='Numero de Cedula Invalido.')]),
	Field('nombre_liceo', type='string', required=True,  requires=IS_IN_DB(db, db.liceo.nombre)),
	Field('telefono', type='string', length=12, requires=IS_MATCH('^((0)?[0-9]{3}(-)?)?[0-9]{7}$', error_message='Telefono Invalido.')),

#	migrate=False
	)

db.define_table(
	'materia',
	Field('nombre', type='string', notnull=True, unique=True),

#	migrate=False
	)

db.define_table(
	'profesor',
	Field('ci', type='string', notnull=True, unique=True, requires=[IS_IN_DB(db, db.usuario.username), IS_MATCH('^[0-9]*$', error_message='Numero de Cedula Invalido.')]),
	Field('materia', type='string', notnull=True, requires=IS_IN_DB(db, db.materia.nombre)),
	Field('telefono', type ='string', length=12, requires=IS_MATCH('^((0)?[0-9]{3}(-)?)?[0-9]{7}$', error_message='Telefono Invalido.')),

#	migrate=False
	)

db.define_table(
	'cursa',
	Field('ci_estudiante', type='string', requires=IS_IN_DB(db, db.estudiante.ci)),
	Field('nombre_materia', type='string', requires=IS_IN_DB(db, db.materia.nombre)),
	Field('notas', type='list:integer'),

#	migrate=False
)

db.define_table(
	'inasistencia',
	Field('ci_estudiante', type='string', requires=IS_IN_DB(db, db.estudiante.ci)),
	Field('nombre_materia', type='string', requires=IS_IN_DB(db, db.materia.nombre)),
	Field('fecha_clase', type='date', requires=IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')),

#	migrate=False
)

db.define_table(
	'carrera',
	Field('nombre', type='string'),
	Field('dictada_en_la_USB', type='boolean', notnull=True, default=True),

#	migrate=False
)

db.define_table(
	'exime',
	Field('ci_estudiante', type='string', length=8, notnull=True, requires=IS_IN_DB(db, db.estudiante.ci)),
	Field('liceo', type='string', requires=IS_IN_DB(db, db.liceo.nombre)),
	Field('cohorte', type='string', notnull=True, requires=IS_IN_DB(db, db.cohorte.identificador)),

#	migrate=False
)

db.define_table(
	'periodo',
	Field('nombre', type='string', unique=True),
	# Field('fecha_inicio', type='date', requires=IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')),
	# Field('fecha_fin', type='date', requires=IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')),
	Field('Activo', type='boolean', notnull=True, default=True),

#	migrate=False
)

db.define_table(
	'noticias',
	Field('titulo', type='string'),
	Field('contenido', type='text'),
	Field('fecha_publicacion', type='date', requires=IS_DATE(format=T('%d/%m/%Y'), error_message='Debe ser del siguiente formato: dd/mm/yyyy')),

#	migrate=False
)

db.define_table(
	'promedio_ingreso',
	Field('promedio', type='double', notnull=True),

#	migrate=False
)

db.define_table(
	'tokens_enviados',
	Field('ci_estudiante', type='string', length=8, notnull=True, requires=IS_IN_DB(db, db.estudiante.ci)),
	Field('token', type='string', length=30, notnull=True),

#	migrate='db.tokens_enviados'
	)

db.define_table(
	'resultados_prueba',
	Field('ci_estudiante', type='string', length=8, notnull=True, requires=IS_IN_DB(db, db.estudiante.ci)),
	Field('id_examen', type='string', requires=IS_IN_SET(['-1', 'Test Vocacional', 'Test de Inteligencia', 'Habilidad Matematica', 'Habilidad Verbal'])),
	Field('resultado', type='double'),

#	migrate='db.resultados_prueba'
)


# Agregamos el Periodo 'Prueba PIO' en caso de que no exista.
if not db(db.periodo.nombre=="Prueba PIO").select():
	db.periodo.insert(nombre="Prueba PIO", fecha_inicio="01/01/2017",
					  fecha_fin="01/01/2017", Activo=False)

if not db(db.auth_membership.group_id == 5).select():
	# Primer Usuario del Sistema
	id_usuario = db.usuario.insert(username='admin', password=CRYPT()('admin')[0], first_name='SisPIO',
								   last_name='Admin', email='admin@usb.ve')

	# Roles
	estudiante = auth.add_group(role='Estudiante', description='description')
	profesor = auth.add_group(role='Profesor', description='description')
	representante_liceo = auth.add_group(role='Representante_liceo', description='description')
	representante_sede = auth.add_group(role='Representante_sede', description='description')
	admin = auth.add_group(role='Administrador', description='description')

	# Permisos para cada rol
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

	# Dar privilegios de Administrador al usario creado
	auth.add_membership(admin, id_usuario)

	# Cohorte
	db.cohorte.insert(identificador='2018/2019',status='Proxima')

	# Sedes
	db.sede.insert(zona='Sartenejas')
	db.sede.insert(zona='Litoral')
	db.sede.insert(zona='Guarenas')
	db.sede.insert(zona='Higuerote')

	# Materias PIO
	db.materia.insert(nombre = "Matematicas")
	db.materia.insert(nombre = "Lenguaje")
	db.materia.insert(nombre = "Psicoafectivo")

	# Liceo para Estudiantes independientes
	db.liceo.insert(nombre='Otros', tipo='Otro', sede='Sartenejas', telefono='02127654321')

	# Carreras USB
	db.carrera.insert(nombre="Ingeniería Eléctrica", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Ingeniería Mecánica", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Ingeniería Química", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Ingeniería Electrónica", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Ingeniería de Materiales", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Ingeniería de la Computación", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Ingeniería Geofísica", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Ingeniería de Producción", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Ingeniería de Mantenimiento", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Ingeniería de Telecomunicaciones", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Arquitectura", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Urbanismo", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Licenciatura en Química", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Licenciatura en Matemáticas", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Licenciatura en Física", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Licenciatura en Biología", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Licenciatura en Comercio Internacional", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Licenciatura en Gestión de la Hospitalidad", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Tecnología Eléctrica", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Tecnología Electrónica", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Tecnología Mecánica", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Mantenimiento Aeronáutico", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Administración del Turismo", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Administración Hotelera", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Administración del Transporte", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Organización Empresarial", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Comercio Exterior", dictada_en_la_USB=True)
	db.carrera.insert(nombre="Administración Aduanera", dictada_en_la_USB=True)
	# Carrera No USB
	db.carrera.insert(nombre="Psicologia", dictada_en_la_USB=False)
	db.carrera.insert(nombre="Odontologia", dictada_en_la_USB=False)
	db.carrera.insert(nombre="Filosofia", dictada_en_la_USB=False)

	# Procesos
	db.periodo.insert(nombre="Test Vocacional",
					  # fecha_inicio= "01/01/2017",
					  # fecha_fin= "01/01/2017",
					  Activo=True)
	db.periodo.insert(nombre="Carga Estudiantes",
					  # fecha_inicio= "01/01/2017",
					  # fecha_fin= "01/01/2017",
					  Activo=True)

	# Promedio ingreso
	db.promedio_ingreso.insert(promedio=13.00)
