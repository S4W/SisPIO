@service.xmlrpc
def check_periodo():
	estado = db(db.periodo.nombre == "Prueba PIO").select()[0].Activo

	return estado
