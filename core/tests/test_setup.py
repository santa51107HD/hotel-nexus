from rest_framework.test import APITestCase
from django.urls import reverse
from dotenv import load_dotenv
import os

load_dotenv()

class TestSetUp(APITestCase):

    def setUp(self):
        self.login_url = reverse('login')
        self.create_url = reverse('create_user')
        self.admin_url = reverse('admin')
        self.client_url = reverse('client')
        self.recep_url = reverse('recep')
        self.clients_all_url = reverse('clients')
        self.clients_rooms_url = reverse('Crooms')
        self.free_rooms_url = reverse('rooms')
        
        self.admin_data ={

            "tipo": "Admin",
            "nombre": "prueba",
            "apellido": "prueba",
            "email": "test@test.com",
            "direccion": "calle test",
            "fecha_nacimiento": '2023-01-20',
            "salario": 100,
            "password": os.environ['TEST_PASSWORD']
        }

        self.login_admin_data = {
            'username':'test@test.com',
            'password': os.environ['TEST_PASSWORD']
        }

        self.client_data ={

            "tipo": "Cliente",
            "nombre": "clienteprueba",
            "apellido": "prueba",
            "email": "test1@test.com",
            "direccion": "calle test",
            "fecha_nacimiento": '2023-01-20',
            "salario": 0,
            "password": os.environ['TEST_PASSWORD']
        }

        self.login_client_data = {
            'username':'test1@test.com',
            'password': os.environ['TEST_PASSWORD']
        }

        self.recep_data ={

            "tipo": "Recepcionista",
            "nombre": "recepprueba",
            "apellido": "prueba",
            "email": "test2@test.com",
            "direccion": "calle test",
            "fecha_nacimiento": '2023-01-20',
            "salario": 100,
            "password": os.environ['TEST_PASSWORD']
        }
        self.login_recep_data = {
            'username':'test2@test.com',
            'password': os.environ['TEST_PASSWORD']
        }

        self.room1_data = {
            "disponible": True,
            "numero": 1
        }
        self.room2_data = {
            "disponible": False,
            "numero": 2
        }
        
        self.room1_bad_data ={
            "disponible": True,
            "numero": "camion"
        }

        self.room1_book_data = {
            
            "habitacion_id": 1
        }
        
        self.room1_book_bad_data = {
            
            "habitacion_id": "carro"

        }

        self.room1_book_bad_id_data = {
            
            "habitacion_id": 50
        }

        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()