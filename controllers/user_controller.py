from flask import request, Blueprint, render_template, redirect, url_for, flash
from utils.database import db
from models import Usuario
from sqlalchemy.exc import IntegrityError
# Corregido: Declaración correcta del Blueprint
user_blueprint = Blueprint('user_controller', __name__)

# Obtener todos los usuarios
@user_blueprint.route('/users', methods=['GET'])
def get_users():
    users = Usuario.query.all()
    return render_template('users.html', users=users)

# Crear un nuevo usuario (GET para el formulario, POST para el envío del formulario)
@user_blueprint.route('/users/new', methods=['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        return render_template('add_user.html')  # Mostrar el formulario al usuario

    elif request.method == 'POST':
        # Obtener los datos del formulario
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            # Crear el nuevo usuario
            user = Usuario(
                username=username,
                email=email,
                password=password  # Almacenar la contraseña en texto plano por simplicidad; considera encriptarla para mayor seguridad
            )
            db.session.add(user)
            db.session.commit()
            flash('¡Usuario creado con éxito!', 'success')
            return redirect(url_for('user_controller.get_users'))  # Redirigir después de la creación exitosa
        except IntegrityError:
            db.session.rollback()
            flash('Error: El nombre de usuario o correo electrónico ya existe.', 'danger')
            return render_template('add_user.html'), 400

# Actualizar un usuario (GET para el formulario, POST para el envío del formulario)
@user_blueprint.route('/users/<int:id>/edit', methods=['GET', 'POST'])
def update_user(id):
    user = Usuario.query.get(id)

    if request.method == 'GET':
        return render_template('edit_user.html', user=user)  # Mostrar el formulario de edición con los datos del usuario

    elif request.method == 'POST':
        # Obtener los datos del formulario
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Solo actualizar la contraseña si se proporciona
        if password:
            user.password = password

        # Manejar campos vacíos manteniendo los datos anteriores
        user.username = username if username else user.username
        user.email = email if email else user.email
        
        db.session.commit()
        flash('¡Usuario actualizado con éxito!', 'success')
        return redirect(url_for('user_controller.get_users'))

# Eliminar un usuario
@user_blueprint.route('/users/<int:id>/delete', methods=['POST'])
def delete_user(id):
    user = Usuario.query.get(id)
    
    db.session.delete(user)
    db.session.commit()
    
    flash('¡Usuario eliminado con éxito!', 'success')
    return redirect(url_for('user_controller.get_users'))  # Redirigir después de la eliminación exitosa
