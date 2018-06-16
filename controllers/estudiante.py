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

	return dict(formDatosBasicos = formDatosBasicos, formEstudiante = formEstudiante, estado = estado, prueba=prueba)

"""
Generador automatico de claves aleatorias
"""
def generadorClave():
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
			nuevaClave = generadorClave()
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

	return dict(user=user, estudiante = estudiante, prueba=prueba, prueba_activa=prueba_activa)

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

	return dict(cambiarContrasena=cambiarContrasena, prueba=prueba)

@auth.requires_membership('Estudiante')
@auth.requires_login()
def presentarPrueba():

	user = db(db.usuario.username==auth.user.username).select()[0]

	token = generadorToken()
	db.tokens_enviados.update_or_insert(db.tokens_enviados.ci_estudiante == user.username, ci_estudiante = user.username, token = token)

	redirect("http://127.0.0.1:8000/examspio3/default/index?ci="+user.username+"&nombre="+user.first_name+"&apellido="+user.last_name+"&correo=migcanedo96@hotmail.com"+"&token="+token)
	# redirect("http://desearte1.dex.usb.ve/examspio3/default/index?ci="+user.username+"&nombre="+user.first_name+"&apellido="+user.last_name+"&correo="+user.email+"&token="+token)
	# redirect("http://seleccion.pio.dex.usb.ve/examspio3/default/index?ci="+user.username+"&nombre="+user.first_name+"&apellido="+user.last_name+"&correo="+user.email+"&token="+token)


	return dict()

"""
Generador aleatorio de tokens.
"""
def generadorToken():
	import string, random

	lst = [random.choice(string.ascii_letters + string.digits) for _ in range(30)]
	tokenNuevo = "".join(lst)


	return tokenNuevo
