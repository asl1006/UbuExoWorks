

from datetime import datetime
import string
import secrets
import os
from time import timezone
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, ForeignKey, DateTime, Integer, Text, Float, Time, false
from sqlalchemy.orm import relationship
from database.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



class Usuario(UserMixin, db.Model):
    
    __tablename__ = 'USUARIO'
    
    idUsuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), nullable=False)
    apellidos = db.Column(db.String(45), nullable=False)
    nif = db.Column(db.String(45), nullable=False)
    login = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    estado = db.Column(db.Boolean, nullable=False)
    idEmpresa = db.Column(db.Integer, ForeignKey('EMPRESA.idEmpresa'))
    empresa = db.relationship('Empresa')
    idJornadaLaboral = db.Column(db.Integer, ForeignKey('JORNADA_LABORAL.idJornadaLAboral'))
    jornada = db.relationship('Jornada_Laboral')                                
    idRol = db.Column(db.Integer, nullable=False)
    
    """def __init__(self, idUsuario=None, nombre=None, apellidos=None, login=None, password=None, 
        estado=None, idEmpresa=None,idJornadaLaboral=None, idRol=None) -> None:
        self.idUsuario=idUsuario
        self.nombre=nombre
        self.apellidos=apellidos
        self.login=login
        self.password=generate_password_hash(password)
        self.estado=estado
        self.idEmpresa=idEmpresa
        self.idJornadaLaboral=idJornadaLaboral
        self.idRol=idRol """
    
    def get_id_empresa(self):
        return self.idEmpresa    
    
    def get_id(self):
        return self.idUsuario
    
    def get_login(self):
        return self.login
    
    def save(self):
        if not self.idUsuario:
            db.session.add(self)
            print('añadido en modif')
        else:
            print('actualizado en modif')
        db.session.commit()
        
    def get_by_empresa(idEmpresa):
        return Usuario.query.filter_by(idEmpresa=idEmpresa).all()
        
    @staticmethod
    def get_by_login(login):    
        return Usuario.query.filter_by(login=login).first()
    
    @staticmethod
    def get_by_id(user_id):    
        return Usuario.query.filter_by(idUsuario=user_id).first()

    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def check_habilitado(self):
        return self.estado
    
    @staticmethod
    def generate_password():
        alfabeto = string.ascii_letters + string.digits
        while True:
            password = ''.join(secrets.choice(alfabeto) for i in range(10))
            if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
                break
        print('password generada: ', password)
        return password
    
    
    
    #Metodo para poder serializarlo y enviarlo como un JSON
    def to_JSON(self):
        return {
            'idUsuario': self.idUsuario,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'login': self.login,
            'password': self.password,
            'estado': self.estado,
            'idEmpresa': self.idEmpresa,
            'idJornadaLaboral': self.idJornadaLaboral,
            'idRol': self.idRol
        }
        
class Empresa(db.Model):
    
    __tablename__ = 'EMPRESA'
    
    idEmpresa = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), nullable=False)
    cif = db.Column(db.String(20), nullable=False)
    planContratado = db.Column(db.Integer, nullable=False)
    numEmpleados = db.Column(db.Integer, nullable=False)
    
    """
    def __init__(self, idEmpresa, nombre=None, cif=None, planContratado=None, numEmpleados=1) -> None:
        self.idEmpresa = idEmpresa
        self.nombre = nombre
        self.cif = cif
        self.planContratado = planContratado
        self.numEmpleados = numEmpleados
    """        
                 
    @staticmethod
    def get_by_id(idEmpresa):    
        return Empresa.query.filter_by(idEmpresa=idEmpresa).first()
    
    @staticmethod
    def get_by_cif(cif):    
        return Empresa.query.filter_by(cif=cif).first()
    
    def get_id_empresa(self):
        return self.idEmpresa
     
    
    def save(self):
        if not self.idEmpresa:
            db.session.add(self)
        db.session.commit()

    def to_JSON(self):
        return {
            'idEmpresa': self.idEmpresa,
            'nombre': self.nombre,
            'cif': self.cif,
            'planContratado': self.planContratado,
            'numEmpleados': self.numEmpleados
        }  
    
class Jornada_Laboral(db.Model):
        
        __tablename__ = 'JORNADA_LABORAL'
    
        idJornadaLAboral = db.Column(db.Integer, primary_key=True)
        horaEntrada = db.Column(db.Time, nullable=False)
        horaSalida = db.Column(db.Time, nullable=False)
        horaEntrada2 = db.Column(db.Time, nullable=False)
        horaSalida2 = db.Column(db.Time, nullable=False)
        margenFichaje = db.Column(db.Time, nullable=False)
        horasJornada = db.Column(db.Time, nullable=False)
        idEmpresa = db.Column(db.Integer, ForeignKey('EMPRESA.idEmpresa'))
        empresa = db.relationship('Empresa')
                    
        def __init__(self, idJornadaLAboral, horaEntrada=None, horaSalida=None, horaEntrada2=None,
                    horaSalida2=None, margenFichaje=None, horasJornada=None, idEmpresa=None) -> None:
        
            self.idJornadaLAboral=idJornadaLAboral
            self.horaEntrada=horaEntrada
            self.horaSalida=horaSalida
            self.horaEntrada2=horaEntrada2
            self.horaSalida2=horaSalida2
            self.margenFichaje=margenFichaje
            self.horasJornada=horasJornada
            self.idEmpresa=idEmpresa

        @staticmethod
        def get_by_id(idJornadaLAboral):    
            return Jornada_Laboral.query.filter_by(idJornadaLAboral=idJornadaLAboral).first()
    
        def to_JSON(self):
            return {
                'idJornadaLAboral': self.idJornadaLAboral,
                'horaEntrada': self.horaEntrada,
                'horaSalida': self.horaSalida,
                'horaEntrada2': self.horaEntrada2,
                'horaSalida2': self.horaSalida2,
                'margenFichaje': self.margenFichaje,
                'horasJornada': self.horasJornada,
                'idEmpresa': self.idEmpresa
            }  
            
class Fichaje(db.Model):
    __tablename__ = "FICHAJE"
    
    idFichaje = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    hora_entrada = db.Column(db.Time(timezone=false), nullable=False)
    entrada_latitud = db.Column(db.Float, nullable=False)
    entrada_longitud = db.Column(db.Float, nullable=False)
    #hora_salida= db.Column(db.Time(timezone=false), nullable=False)
    #salida_latitud = db.Column(db.Float, nullable=False)
    #salida_longitud = db.Column(db.Float, nullable=False)
    incidencia = db.Column(db.String, nullable=False)
    idUsuario =  db.Column(db.Integer, ForeignKey('USUARIO.idUsuario'))
    usuario = db.relationship('Usuario')
   
    """ 
    def __init__(self, idFichaje, fecha=None, hora_entrada=None, entrada_latitud=None, entrada_longitud=None,
                 hora_salida=None, salida_latitud=None, salida_longitud=None, incidencia=None, idUsuario=None) -> None:
        
        self.idFichaje=idFichaje
        self.fecha=fecha
        self.hora_entrada=hora_entrada
        self.entrada_latitud=entrada_latitud
        self.entrada_longitud=entrada_longitud
        self.hora_salida=hora_salida
        self.salida_latitud=salida_latitud
        self.salida_longitud=salida_longitud
        self.incidencia=incidencia
        self.idUsuario=idUsuario 
    """
        
    def to_JSON(self):
        
        
        hora = str(self.hora_entrada)
        print(hora)
        return {
            'idFichaje': self.idFichaje,
            'fecha': self.fecha,
            #'hora_entrada':self.hora_entrada,
            'hora_entrada':hora,
            'entrada_latitud':self.entrada_latitud,
            'entrada_longitud':self.entrada_longitud,
            #'hora_salida':self.hora_salida,
            #'salida_latitud':self.entrada_latitud,
            #'salida_longitud':self.entrada_longitud,
            'incidencia':self.incidencia,
            'idUsuario':self.idUsuario
        }
        
    @staticmethod
    def get_by_idEmpleado(idEmpleado):    
        return Fichaje.query.filter_by(idUsuario=idEmpleado).all()
    
    @staticmethod
    def get_by_idEmpleadoFecha(idEmpleado,fecha):
        return Fichaje.query.filter_by(idUsuario=idEmpleado, fecha=fecha).all()       
    
    def save(self):
        if not self.idFichaje:
            db.session.add(self)
        db.session.commit()    