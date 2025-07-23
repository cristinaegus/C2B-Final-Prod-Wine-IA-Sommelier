from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from werkzeug.security import check_password_hash
from models import db, User

# Funciones auxiliares para gestión de usuarios
def get_all_users():
    return User.query.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def add_user(username, email, password):
    from datetime import date
    # Por simplicidad, se crean usuarios con datos mínimos y valores por defecto
    user = User(
        email=email,
        password=password,
        first_name=username,
        last_name='',
        birth_date=date(2000,1,1)
    )
    db.session.add(user)
    db.session.commit()

def edit_user(user_id, username, email, password):
    user = User.query.get(user_id)
    if user:
        user.email = email
        user.first_name = username
        if password:
            user.set_password(password)
        db.session.commit()

def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()

admin_bp = Blueprint('admin', __name__, template_folder='templates')

# Configuración del usuario administrador único
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD_HASH = 'scrypt:32768:8:1$fvefhX54pWKHOheC$b3cfc07e0f4727a1809d4ae8127460f44de0340972554ada31034ef674f767b6d703a3d36b4543c4b2e85b32a7b2e1daf83cbdcbd74a6b78e11c100684b61e79'  # Reemplaza por el hash real

@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['admin_logged_in'] = True
            return redirect(url_for('admin.admin_panel'))
        else:
            flash('Credenciales incorrectas', 'danger')
    return render_template('admin_login.html')

@admin_bp.route('/admin')
def admin_panel():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))
    users = get_all_users()
    return render_template('admin.html', users=users)

@admin_bp.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.admin_login'))

# Rutas para agregar, editar y eliminar usuarios
@admin_bp.route('/admin/add', methods=['GET', 'POST'])
def admin_add():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        add_user(username, email, password)
        return redirect(url_for('admin.admin_panel'))
    return render_template('admin_add.html')

@admin_bp.route('/admin/edit/<int:user_id>', methods=['GET', 'POST'])
def admin_edit(user_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))
    user = get_user_by_id(user_id)
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        edit_user(user_id, username, email, password)
        return redirect(url_for('admin.admin_panel'))
    return render_template('admin_edit.html', user=user)

@admin_bp.route('/admin/delete/<int:user_id>')
def admin_delete(user_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))
    delete_user(user_id)
    return redirect(url_for('admin.admin_panel'))
