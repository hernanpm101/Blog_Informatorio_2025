# Proyecto desarrollado en Python/Django

## Descripción
**Blog Mundial FIFA** es un espacio dedicado a recorrer la apasionante historia de los Mundiales de Fútbol, desde Uruguay 1930 hasta Qatar 2022.  
Aquí encontrarás análisis de cada torneo, posiciones de las selecciones, anécdotas, curiosidades y los momentos que marcaron época.  

Nuestro objetivo es mantener viva la memoria de cada Copa del Mundo, acercando estadísticas, historias y reflexiones tanto para fanáticos del fútbol como para quienes disfrutan de la historia detrás de este deporte.  

También contamos con un espacio para que los lectores comenten, compartan sus opiniones y formen parte de esta comunidad mundialista.  

👨‍💻 **Alumnos (Grupo 12)**:  
- Maria Cristina Roma  
- Jonathan Ariel Sotelo  
- Hernan Perez Melgar   

---

## Información adicional
Para poder ingresar como **superusuario** y poder editar, agregar un nuevo Post, eliminar comentarios, crear categorías, etc:  

- **Usuario**: `hernan`  
- **Contraseña**: `1234`  

---

## 🌐 Proyecto en producción
El blog se encuentra desplegado en **PythonAnywhere by Anaconda** y puede visitarse en el siguiente enlace:  

👉 [Blog Mundial FIFA - Producción](https://hernanpm101.pythonanywhere.com/)  

---

## Estructura del proyecto

```bash
blog_mundial/
├── manage.py
├── blog_mundial
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── mundial
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── templates
│   │   └── mundial
│   │       ├── acerca.html
│   │       ├── base.html
│   │       ├── contacto.html
│   │       ├── crear_post.html
│   │       ├── detalle_post.html
│   │       ├── inicio.html
│   │       ├── listar_posts.html
│   │       ├── login.html
│   │       ├── registro.html
│   │       └── ...
│   ├── urls.py
│   └── views.py
├── static
│   └── img
│       ├── fondo.jpg
│       └── favicon.png
└── requirements.txt






