#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#coding:utf-8

from google.appengine.api import users
from user import Usuario
from gimnasio import Gimnasio
from webapp2_extras import jinja2
from google.appengine.ext import ndb


import webapp2
class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
                email = user.email()
                name = user.nickname()
                login_logout_url = users.create_logout_url('/')

                datos = {
                    "login_logout_url": login_logout_url,
                    "user": user

                }
                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(jinja.render_template("formulario.html", **datos))

        else:

            email = "anonymous@anonymous.com"
            login_logout_url = users.create_login_url('/')
            name = 'ninguno'

            datos = {
                "login_logout_url": login_logout_url,
                "user":user

            }
            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("index.html", **datos))

        usuario = Usuario(email=email,name=name)
        usuario.put()


class ListarUsuarios(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        usuarios = Usuario.query()
        email=user.email()
        datos = {
            "usuarios": usuarios,
            "email":email

        }
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("usuarios.html", **datos))

class AddUser(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("add.html"))
    def post(self):
        email = self.request.get("email")
        name = self.request.get("name")

        usuario = Usuario(email=email,name=name)
        usuario.put()
        self.redirect("/listarUsuarios")

class ModificarUsuario(webapp2.RequestHandler):
    def get(self):
        usuario = self.request.get("id")
        usuario = ndb.Key(urlsafe=usuario).get()

        datos = {
            "usuario": usuario

        }
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("modificar.html", **datos))
    def post(self):
        usuario = self.request.get("id")
        name = self.request.get("name")
        usuario = ndb.Key(urlsafe=usuario).get()
        usuario.name = name
        usuario.put()

        self.redirect("/listarUsuarios")





class EliminarUsuario(webapp2.RequestHandler):

    def post(self):
        usuario = self.request.get("id")
        user = ndb.Key(urlsafe=usuario).get()
        user.key.delete()
        self.redirect("/listarUsuarios")#redirigir con jinja como con las actividades




class Horario(webapp2.RequestHandler):
    def get(self):
        actividades = Gimnasio.query()

        datos = {
            'actividades': actividades

            # 'gym':gym
            # "usr_name":nombre,
            # "usuarios":Usuario.query().order(-Usuario.momento),
            # "login_url":login_logout_url
            # "usr":usr

        }
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("horario.html", **datos))

    def post(self):
        actividades= self.request.get_all("actividades")
        cont = 0
        for i in actividades:
            cont = cont + 1
            gym = Gimnasio(actividades=str(i),id=cont,numInscritos=0)
            gym.put()


        actividades = Gimnasio.query()


        datos = {
            'actividades':actividades

            #'gym':gym
            #"usr_name":nombre,
            #"usuarios":Usuario.query().order(-Usuario.momento),
            #"login_url":login_logout_url
            #"usr":usr


        }
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("horario.html", **datos))
        #if usr:
         #   email = usr.email()
        #else:
         #   email = "anonymous@anonymous.com"

class Apuntar(webapp2.RequestHandler):

    def post(self):
        user = users.get_current_user()
        email = user.email()



        actividad_id= self.request.get("id")
        actividad = ndb.Key(urlsafe=actividad_id).get()
        if actividad.numInscritos < 20:
            actividad.numInscritos += 1


            actividad.usuarios.append(email)


            actividad.put()

        datos = {
            'usuarios':actividad.usuarios




            # 'gym':gym
            # "usr_name":nombre,
            # "usuarios":Usuario.query().order(-Usuario.momento),
            # "login_url":login_logout_url
            # "usr":usr

        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("listarApuntados.html", **datos))






app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/horario', Horario),
    ('/listarUsuarios', ListarUsuarios),
    ('/eliminar', EliminarUsuario),
    ('/apuntarse', Apuntar),
    ('/add', AddUser),
    ('/modificar', ModificarUsuario)

], debug=True)
