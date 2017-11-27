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
            redirect(URL('admin', 'index'))
        elif 'Estudiante' in auth.user_groups.values():
            username = auth.user.username
            estadoEstudiante=db(db.estudiante.ci==username).select()[0].estatus
            if estadoEstudiante == "Pre-inscrito":
                redirect(URL('estudiante','testVocacional'))
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
