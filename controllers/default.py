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
    return dict(form=auth.login())

def redireccionando():
    if auth.is_logged_in():
        if 5 in auth.user_groups:
            redirect(URL('admin'))
        elif 1 in auth.user_groups:
            redirect(URL('welcome'))
        elif 2 in auth.user_groups:
            redirect(URL('profesor'))
        elif 3 in auth.user_groups:
            redirect(URL('coordinadorLiceo'))
        elif 4 in auth.user_groups:
            redirect(URL('coordinadorPio'))
        else:
            redirect(URL('default', 'user', args='logout'))
    else:
        redirect(URL('index'))
    return dict()

@auth.requires_membership('Administrador')
@auth.requires_login()
def admin():
    return dict()


@auth.requires_membership('Profesor')
@auth.requires_login()
def profesor():
    return dict()

@auth.requires_membership('Representante_liceo')
@auth.requires_login()
def coordinadorLiceo():
    return dict()

@auth.requires_membership('Representante_sede')
@auth.requires_login()
def coordinadorPio():
    return dict()

@auth.requires_membership('Estudiante')
@auth.requires_login()
def welcome():
    if auth.is_logged_in():
        usuario = auth.user.id
    else:
        usuario = "nadie"
    return dict(usuario=usuario)
