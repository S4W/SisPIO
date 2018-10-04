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


def call():
	"""
	exposes services. for example:
	http://..../[app]/default/call/jsonrpc
	decorate with @service.jsonrpc the functions to expose
	supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
	"""
	session.forget()
	return service()

def index():
	if auth.is_logged_in():
		redirect(URL('default', 'user', args='logout')) # Si ya hay un usuario conectado, desconectarlo

	return dict(form=auth.login())

def redireccionando():
	if auth.is_logged_in():
		if 'Administrador' in auth.user_groups.values():
			redirect(URL('admin', 'index'))
		elif db(db.estudiante.ci==auth.user.username).select():
			estadoEstudiante=db(db.estudiante.ci==auth.user.username).select()[0].estatus
			if estadoEstudiante == "Pre-inscrito":
				redirect(URL('estudiante','testVocacional'))
			elif estadoEstudiante == "Seleccionado":
				if not db(db.estudiante.ci==auth.user.username).select()[0].validado:
					redirect(URL('estudiante', 'confirmarDatos'))
				else:
					redirect(URL('estudiante', 'index'))
			elif estadoEstudiante == "Inactivo":
				response.flash = "Lo sentimos, usted ya no tiene acceso al sistema"
				redirect(URL('estudiante', 'falloTest'))
			else:
				redirect(URL('estudiante','index'))

		elif 'Profesor' in auth.user_groups.values():
			redirect(URL('profesor','index'))
		elif 'Representante_liceo' in auth.user_groups.values():
			redirect(URL('representanteLiceo','index'))
		elif 'Representante_sede' in auth.user_groups.values():
			redirect(URL('representantePio','index'))
		else:
			redirect(URL('default', 'user', args='logout'))
	else:
		redirect(URL('default', 'index'))
	return dict()

def validacion_foto():
	acepto = request.args(0) == "aceptar"
	cedula = request.args(1)

	usuario = db(db.usuario.username == cedula).select().first()
	if acepto:
		db(db.estudiante.ci == cedula).update(foto_validada = True)

		msj = "La foto del estudiante con Cedula %s fue validada."%cedula

		print(mail.send(to=[usuario.email],
			  subject="Foto Aceptada para Carnet de PIO",
			  message="""
<html lang="en">
<body>
<center>
	<br>
	<h2>
		Su foto fue validada y aceptada por la Coordinación del Programa.
	</h2>
	<br><br><br>
	<font size="3">No responder este correo</font>
</center>
</body>
</html>
					"""))
	else:
		db(db.estudiante.ci == cedula).update(foto = None)

		msj = "La foto del estudiante con Cedula %s fue rechazada."%cedula

		print(mail.send(to=[usuario.email],
			  subject="Foto Rechazada para Carnet de PIO",
			  message="""
<html lang="en">
<body>
<center>
	<br>
	<h2>
		Su foto fue rechaza por la Coordinación del Programa por no cumplir con las reglas respectivas.
		<br><br><br>
		Favor cargue una foto en el sistema que cumpla con las indicaciones.
	</h2>
	<br><br><br>
	<font size="3">No responder este correo</font>
</center>
</body>
</html>
					"""))

	return dict(msj=msj)

@service.run
def check_periodo():
	estado = db(db.periodo.nombre == "Prueba PIO").select()[0].Activo

	return estado

@service.run
def check_token(ci, token):

	return db(db.tokens_enviados.ci_estudiante == ci).select().first().token == token

@service.run
def resultado(ci, id_exam, resultado):
	if id_exam == "PV":
		id_exam = "Test Vocacional"
	elif id_exam == "TI":
		id_exam = "Test de Inteligencia"
	elif id_exam == "HM":
		id_exam = "Habilidad Matematica"
	elif id_exam == "HV":
		id_exam = "Habilidad Verbal"

	if id_exam != "-1":
		db.resultados_prueba.update_or_insert((db.resultados_prueba.ci_estudiante == ci) & (db.resultados_prueba.id_examen == id_exam),
												ci_estudiante = ci, id_examen = id_exam, resultado = float(resultado))

def resultadoQR():
	if not request.vars:
		return "No Args"

	estudiante = db(db.estudiante.ci == request.vars.cedula).select().first()
	user = db(db.usuario.username == request.vars.cedula).select().first()
	return dict(estudiante=estudiante, user=user)
