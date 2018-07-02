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

	estado = db(db.estudiante.ci == auth.user.username).select().first().estatus
	prueba = db(db.periodo.nombre == "Prueba PIO").select()[0].Activo
	datosCompletos = _checkDatosFlatantes(auth.user.username)

	return dict(formDatosBasicos = formDatosBasicos, formEstudiante = formEstudiante, estado = estado, prueba=prueba, datosCompletos=datosCompletos)


def _checkDatosFlatantes(username):
	completo = True
	estudiante = db(db.estudiante.ci == username).select().first()
	completo = completo and estudiante.direccion
	completo = completo and estudiante.telefono_habitacion
	completo = completo and estudiante.telefono_otro
	completo = completo and estudiante.fecha_nacimiento
	completo = completo and estudiante.sexo
	completo = completo and estudiante.ci_representante
	completo = completo and estudiante.nombre_representante
	completo = completo and estudiante.apellido_representante
	completo = completo and estudiante.sexo_representante
	completo = completo and estudiante.correo_representante
	completo = completo and estudiante.direccion_representante
	completo = completo and estudiante.telefono_representante_oficina
	completo = completo and estudiante.telefono_representante_otro
	if estudiante.sufre_enfermedad:
		completo = completo and estudiante.enfermedad
		completo = completo and estudiante.indicaciones_enfermedad

	return completo

"""
Generador automatico de claves aleatorias
"""
def _generadorClave():
		import string
		import random
		psw = ''
		for i in range(0,3):
			psw += random.choice(string.ascii_lowercase)
			psw += random.choice(string.ascii_uppercase)
			psw += random.choice(string.digits)

		return ''.join(random.sample(psw,len(psw)))


def confirmarDatos():
	user = db(db.usuario.username == auth.user.username).select()[0]
	estudiante = db(db.estudiante.ci == auth.user.username).select().first()

	formularioConfirmacion = FORM()

	if formularioConfirmacion.accepts(request.vars, formname="formularioConfirmacion"):
		if user.email:
			nuevaClave = _generadorClave()
			db(db.usuario.username == auth.user.username).update(password=CRYPT()(nuevaClave)[0])

			# Enviamos al correo la nueva clave generada.

			print(mail.send(to=[user.email],
				  subject="Datos de Acceso SisPIO",
				  message="""
<html>
	<body>
		<br>
		<div>
			<center>
				<font size="10"><b>Bienvenido a SisPIO </b></font>
			</center>
			<br><br>
			<center>
				<font size="6">A continuación se presentan los datos que necesitará para ingresar al sistema.</font>
			</center>
		</div>
		<br><br><br>
		<div>
			<center> <font size="6"><b> Cédula: </b> </font> </center>
		</div>
		<div>
			<center><font size="5">"""+ auth.user.username +"""</font></center>
		</div>
		<br><br>
		<div>
			<center> <font size="6"> <b> Nueva contraseña: </b> </font> </center>
		</div>
		<div>
			<center><font size="5">"""+ nuevaClave +"""</font></center>
		</div>
	</body>
</html>
						"""))


			db(db.estudiante.ci == auth.user.username).update(validado = True)
			redirect(URL('default', 'index'))
		else:
			session.flash = "No tiene correo asignado, favor comuniquese con la coordinacion."


	return dict(user=user, estudiante=estudiante)


def testVocacional():
	periodoActivo = db(db.periodo.nombre=="Test Vocacional").select()[0].Activo
	userId = db(db.usuario.username==auth.user.username).select()[0].id
	correo = db(db.usuario.username==auth.user.username).select()[0].email
	tieneCorreo = correo != None


	testVocacional = FORM()
	if testVocacional.accepts(request.vars,formname='testVocacional'):
		if ((request.vars.primeraCarrera != request.vars.segundaCarrera) and
			(request.vars.primeraCarrera != request.vars.terceraCarrera) and
			(request.vars.terceraCarrera != request.vars.segundaCarrera)):

			if (db((db.carrera.nombre==request.vars.primeraCarrera)&(db.carrera.dictada_en_la_USB==True)).select() or
					db((db.carrera.nombre==request.vars.segundaCarrera)&(db.carrera.dictada_en_la_USB==True)).select() or
					db((db.carrera.nombre==request.vars.terceraCarrera)&(db.carrera.dictada_en_la_USB==True)).select()):
						db(db.estudiante.ci==auth.user.username).update(estatus="Seleccionado")
						db.auth_membership.insert(user_id = userId, group_id= 1)                # Agregar permisos de estudiante (group_id=1)
						session.flash = "Felicidades, usted es un alumno candidato para presentar la prueba del PIO."
						db(db.usuario.username == auth.user.username).update(email=request.vars.email)
						redirect(URL('confirmarDatos'))
			else:
				db(db.estudiante.ci == auth.user.username).update(estatus="Inactivo")
				session.flash = "Lo sentimos, usted no es candidato para cursar el PIO"
				redirect(URL('falloTest'))
		else:
			response.flash = "Selecciona tres carreras distintas"
	# Desplegables
	ordenAlfabeticoCarreras = db.carrera.nombre
	carreras = db(db.carrera.id>0).select(orderby=ordenAlfabeticoCarreras)

	# session.flash(correo)
	# prueba = db(db.periodo.nombre == "Prueba PIO").select()[0].Activo

	return dict(carreras=carreras,periodoActivo=periodoActivo, correo=correo, tieneCorreo=tieneCorreo)

def falloTest():
	return dict()

@auth.requires_membership('Estudiante')
@auth.requires_login()
def perfil():
	formularioPerfil = FORM()
	user = db(db.usuario.username==auth.user.username).select()[0]

	if formularioPerfil.accepts(request.vars,formname="formularioPerfil"):    # Verificamos que se haya introducido una cedula

		if (not(db(db.usuario.username == request.vars.cedula).select())) or user.username==request.vars.cedula:

			# db(db.usuario.username==user.username).update(first_name=request.vars.nombre)
			# db(db.usuario.username==user.username).update(last_name=request.vars.apellido)
			# db(db.usuario.username==user.username).update(username=request.vars.cedula)
			db(db.estudiante.ci==user.username).update(fecha_nacimiento=request.vars.fecha)
			db(db.estudiante.ci == user.username).update(sexo=request.vars.sexo)

			db(db.usuario.username == user.username).update(email=request.vars.email)
			db(db.estudiante.ci==user.username).update(telefono_habitacion=request.vars.telefonoHabitacion)
			db(db.estudiante.ci==user.username).update(telefono_otro=request.vars.telefonoOtro)
			db(db.estudiante.ci==user.username).update(direccion=request.vars.direccion)

			db(db.estudiante.ci==user.username).update(ci_representante=request.vars.cedulaRepresentante)
			db(db.estudiante.ci==user.username).update(nombre_representante=request.vars.nombresRepresentante)
			db(db.estudiante.ci==user.username).update(apellido_representante=request.vars.apellidosRepresentante)
			db(db.estudiante.ci==user.username).update(sexo_representante=request.vars.sexoRepresentante)
			db(db.estudiante.ci==user.username).update(correo_representante=request.vars.emailRepresentante)
			db(db.estudiante.ci==user.username).update(direccion_representante=request.vars.direccionRepresentante)
			db(db.estudiante.ci==user.username).update(telefono_representante_oficina=request.vars.telefonoOficinaRepresentante)
			db(db.estudiante.ci==user.username).update(telefono_representante_otro=request.vars.telefonoOtroRepresentante)

			db(db.estudiante.ci==user.username).update(trabajo_representante=request.vars.trabajoRepresentante)
			db(db.estudiante.ci==user.username).update(direccion_trabajo_representante=request.vars.direccionTrabajoRepresentante)

			db(db.estudiante.ci==user.username).update(sufre_enfermedad=request.vars.enfermedad)
			db(db.estudiante.ci==user.username).update(enfermedad=request.vars.informacionEnfermedad)
			db(db.estudiante.ci==user.username).update(indicaciones_enfermedad=request.vars.indicacionEnfermedad)



			auth.user.update(username=request.vars.cedula)
			user = db(db.usuario.username==auth.user.username).select()[0]
			response.flash = "Perfil Modificado exitosamente"
		else:
			response.flash = "Ya existe un usuario con la cédula de identidad introducida"

	estudiante = db(db.estudiante.ci == auth.user.username).select().first()
	prueba = db(db.periodo.nombre == "Prueba PIO").select()[0].Activo
	prueba_activa = db(db.periodo.nombre=="Prueba PIO").select().first().Activo
	datosCompletos = _checkDatosFlatantes(auth.user.username)
	estado = db(db.estudiante.ci == auth.user.username).select().first().estatus


	return dict(user=user, estudiante = estudiante, prueba=prueba, prueba_activa=prueba_activa, datosCompletos=datosCompletos, estado=estado)

@auth.requires_membership('Estudiante')
@auth.requires_login()
def cambioContrasena():

	cambiarContrasena = FORM()
	username = auth.user.username

	if cambiarContrasena.accepts(request.vars, formname="cambiarContrasena"):
		if db.usuario.password.validate(request.vars.contrasena) == (db(db.usuario.username==username).select().first().password, None):
			if request.vars.password == request.vars.confirm_password:
				if request.vars.contrasena != request.vars.password:
					db(db.usuario.username==username).update(password=db.usuario.password.validate(request.vars.password)[0])
					response.flash = "Contraseña cambiada exitosamente"
				else:
					response.flash = "La nueva contraseña no puede ser igual a la contraseña actual"
			else:
				response.flash = "El campo de la nueva contraseña no coincide con el campo de confirmación de la contraseña"
		else:
			response.flash = "La contraseña actual no es la misma de su cuenta"


	prueba = db(db.periodo.nombre == "Prueba PIO").select()[0].Activo
	datosCompletos = _checkDatosFlatantes(auth.user.username)
	estado = db(db.estudiante.ci == auth.user.username).select().first().estatus

	return dict(cambiarContrasena=cambiarContrasena, prueba=prueba, datosCompletos=datosCompletos, estado=estado)

@auth.requires_membership('Estudiante')
@auth.requires_login()
def presentarPrueba():

	user = db(db.usuario.username==auth.user.username).select()[0]

	token = _generadorToken()
	db.tokens_enviados.update_or_insert(db.tokens_enviados.ci_estudiante == user.username, ci_estudiante = user.username, token = token)

	# redirect("http://127.0.0.1:8000/examspio3/default/index?ci="+user.username+"&nombre="+user.first_name+"&apellido="+user.last_name+"&correo=migcanedo96@hotmail.com"+"&token="+token)
	# redirect("http://desearte1.dex.usb.ve/examspio3/default/index?ci="+user.username+"&nombre="+user.first_name+"&apellido="+user.last_name+"&correo="+user.email+"&token="+token)
	redirect("http://seleccion.pio.dex.usb.ve/examspio3/default/index?ci="+user.username+"&nombre="+user.first_name+"&apellido="+user.last_name+"&correo="+user.email+"&token="+token)


	return dict()

"""
Generador aleatorio de tokens.
"""
def _generadorToken():
	import string, random

	lst = [random.choice(string.ascii_letters + string.digits) for _ in range(30)]
	tokenNuevo = "".join(lst)


	return tokenNuevo

@auth.requires_membership('Estudiante')
@auth.requires_login()
def imprimirPlanilla():
	from fpdf import Template
	from pyPdf import PdfFileWriter, PdfFileReader
	from datetime import date
	import cStringIO
	import os.path

	user = db(db.usuario.username==auth.user.username).select().first()
	estudiante = db(db.estudiante.ci == auth.user.username).select().first()

	buffer = cStringIO.StringIO()

	#######################################
	# Primera Hoja
	#######################################
	elements = [
    { 'name': 'nombre', 'type': 'T', 'x1': 18.0, 'y1': 67.5, 'x2': 200, 'y2': 79, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'cedula', 'type': 'T', 'x1': 55.0, 'y1': 78, 'x2': 95, 'y2': 85, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'edad', 'type': 'T', 'x1': 110.0, 'y1': 78, 'x2': 140, 'y2': 85, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'sexo', 'type': 'T', 'x1': 155, 'y1': 78, 'x2': 200, 'y2': 85, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'fecha_nacimiento', 'type': 'T', 'x1': 56.0, 'y1': 87, 'x2': 69, 'y2': 94, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'correo', 'type': 'T', 'x1': 130.5, 'y1': 86.6, 'x2': 200, 'y2': 93.6, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'direccion', 'type': 'T', 'x1': 72, 'y1': 95, 'x2': 200, 'y2': 102, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'telefono_habitacion', 'type': 'T', 'x1': 60, 'y1': 113, 'x2': 110, 'y2': 120, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'telefono_otro', 'type': 'T', 'x1': 133, 'y1': 113, 'x2': 200, 'y2': 120, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'nombre_representante', 'type': 'T', 'x1': 51.0, 'y1': 130, 'x2': 69.0, 'y2': 137, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'ci_representante', 'type': 'T', 'x1': 145, 'y1': 130, 'x2': 200, 'y2': 137, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'direccion_representante', 'type': 'T', 'x1': 59, 'y1': 138, 'x2': 200, 'y2': 145, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'telefono_representante', 'type': 'T', 'x1': 36, 'y1': 156, 'x2': 69.0, 'y2': 163, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'correo_representante', 'type': 'T', 'x1': 128, 'y1': 156, 'x2': 200, 'y2': 163, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'lugar_trabajo_representante', 'type': 'T', 'x1': 50, 'y1': 164.5, 'x2': 200, 'y2': 171.5, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'direccion_trabajo_representante', 'type': 'T', 'x1': 54, 'y1':173.5, 'x2': 200, 'y2': 180.5, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'telefono_representante_oficina', 'type': 'T', 'x1': 48, 'y1': 183, 'x2': 69.0, 'y2': 190, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'si_sufre_enfermedad', 'type': 'T', 'x1': 76, 'y1': 200, 'x2': 80, 'y2': 207, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'no_sufre_enfermedad', 'type': 'T', 'x1': 97, 'y1': 200, 'x2': 107, 'y2': 207, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'enfermedad', 'type': 'T', 'x1': 119, 'y1': 200, 'x2': 200, 'y2': 207, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'indicaciones_enfermedad', 'type': 'T', 'x1': 18, 'y1': 215, 'x2': 200, 'y2': 224, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, }
	]

	# Inicializamos el Template
	f = Template(format="letter", elements=elements,
	             title="Sample Invoice")
	f.add_page()

	today = date.today()
	born = estudiante.fecha_nacimiento
	# Se llenan los campos como un "dict".
	f["nombre"] = user.last_name + ", " + user.first_name
	f["cedula"] = user.username
	f["edad"] = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
	f["sexo"] = estudiante.sexo
	f["fecha_nacimiento"] = born.strftime("%d/%m/%Y")
	f["correo"] = user.email
	f["direccion"] = estudiante.direccion
	f["telefono_habitacion"] = estudiante.telefono_habitacion
	f["telefono_otro"] = estudiante.telefono_otro
	f["nombre_representante"] = estudiante.apellido_representante + ", " + estudiante.nombre_representante
	f["ci_representante"] = estudiante.ci_representante
	f["direccion_representante"] = estudiante.direccion_representante
	f["telefono_representante"] = estudiante.telefono_representante_otro
	f["correo_representante"] = estudiante.correo_representante
	f["lugar_trabajo_representante"] = estudiante.trabajo_representante
	f["direccion_trabajo_representante"] = estudiante.direccion_trabajo_representante
	f["telefono_representante_oficina"] = estudiante.telefono_representante_oficina
	if estudiante.sufre_enfermedad:
		f["si_sufre_enfermedad"] = "X"
		f["enfermedad"] = estudiante.enfermedad
		f["indicaciones_enfermedad"] = estudiante.indicaciones_enfermedad
	else:
		f["no_sufre_enfermedad"] = "X"


	# Escribimos la hoja en el Buffer.
	buffer.write(f.render("template.pdf", dest='S'))

	buffer.seek(0)
	new_pdf = PdfFileReader(buffer)
	# Leemos la planilla original.
	existing_pdf = PdfFileReader(file(os.path.join(request.folder, "static", "pdfs", 'planillas.pdf'), "rb"))

	# Juntamos los datos junto con la planilla.
	output = PdfFileWriter()
	page = existing_pdf.getPage(0)
	page.mergePage(new_pdf.getPage(0))
	output.addPage(page)


	#######################################
	# Segunda Hoja
	#######################################
	elements = [
	{ 'name': 'nombre_representante', 'type': 'T', 'x1': 24, 'y1': 73, 'x2': 69.0, 'y2': 80, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'ci_representante', 'type': 'T', 'x1': 151.5, 'y1': 73, 'x2': 200, 'y2': 80, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
    { 'name': 'nombre', 'type': 'T', 'x1': 123, 'y1': 82, 'x2': 170, 'y2': 89, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'cedula', 'type': 'T', 'x1': 27, 'y1': 88, 'x2': 40, 'y2': 95, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'dia', 'type': 'T', 'x1': 65, 'y1': 159, 'x2': 90, 'y2': 166, 'font': 'Arial', 'size': 13.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'mes', 'type': 'T', 'x1': 135, 'y1': 159, 'x2': 130, 'y2': 166, 'font': 'Arial', 'size': 13.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	]

	# Inicializamos el Template
	f = Template(format="letter", elements=elements,
	             title="Sample Invoice")
	f.add_page()


	meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
	# Se llenan los campos como un "dict".
	f["nombre_representante"] = estudiante.apellido_representante + ", " + estudiante.nombre_representante
	f["ci_representante"] = estudiante.ci_representante
	f["nombre"] = user.last_name + ", " + user.first_name
	f["cedula"] = user.username
	f["dia"] = today.day
	f["mes"] = meses[today.month - 1]

	buffer = cStringIO.StringIO()
	# Escribimos la hoja en el Buffer.
	buffer.write(f.render("template1.pdf", dest='S'))

	buffer.seek(0)
	new_pdf2 = PdfFileReader(buffer)
	page = existing_pdf.getPage(1)
	page.mergePage(new_pdf2.getPage(0))
	output.addPage(page)




	#######################################
	# Tercera Hoja
	#######################################
	elements = [
	{ 'name': 'nombre', 'type': 'T', 'x1': 27, 'y1': 62.5, 'x2': 50, 'y2': 69.5, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'cedula', 'type': 'T', 'x1': 23, 'y1': 69, 'x2': 50, 'y2': 76, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	{ 'name': 'liceo', 'type': 'T', 'x1': 125, 'y1': 69, 'x2': 200, 'y2': 76, 'font': 'Arial', 'size': 11.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
	]

	# Inicializamos el Template
	f = Template(format="letter", elements=elements,
	             title="Sample Invoice")
	f.add_page()

	# Se llenan los campos como un "dict".
	f["nombre"] = user.last_name + ", " + user.first_name
	f["cedula"] = user.username
	f["liceo"] = estudiante.nombre_liceo

	buffer = cStringIO.StringIO()
	# Escribimos la hoja en el Buffer.
	buffer.write(f.render("template2.pdf", dest='S'))

	buffer.seek(0)
	new_pdf3 = PdfFileReader(buffer)
	page = existing_pdf.getPage(2)
	page.mergePage(new_pdf3.getPage(0))
	output.addPage(page)


	#######################################
	# Cuarta Hoja
	#######################################
	output.addPage(existing_pdf.getPage(3))

	# Guardamos el PDF final en forma de String y lo obtenemos para poderlo mostrar en pantalla.
	output.write(buffer)
	pdf = buffer.getvalue()
	buffer.close()

	header = {'Content-Type': 'application/pdf'}
	response.headers.update(header)

	return pdf
