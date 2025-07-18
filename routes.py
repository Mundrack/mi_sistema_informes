# Archivo: routes.py

from flask import request, jsonify
from app import app, db, bcrypt
from models import Usuario, Rol, Grupo

# =========================================================
# RUTAS DE PRUEBA
# =========================================================

@app.route('/')
def home():
    return jsonify({"message": "API de Informes de Ciberseguridad activa."}), 200

# =========================================================
# RUTAS DE AUTENTICACIÓN
# =========================================================

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    nombre_usuario = data.get('nombre_usuario')
    contrasena = data.get('contrasena')

    if not nombre_usuario or not contrasena:
        return jsonify({"error": "Falta nombre de usuario o contraseña"}), 400

    usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()

    if not usuario or not usuario.check_password(contrasena):
        return jsonify({"error": "Credenciales inválidas"}), 401

    # Por ahora, solo devolvemos éxito. Más adelante, usaremos tokens JWT.
    return jsonify({"message": "Login exitoso", "rol": usuario.rol.nombre}), 200

# =========================================================
# RUTAS DE ADMINISTRACIÓN (EXCLUSIVAS PARA EL ROL 'admin')
# =========================================================

@app.route('/admin/crear_usuario', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    nombre_completo = data.get('nombre_completo')
    nombre_usuario = data.get('nombre_usuario')
    contrasena = data.get('contrasena')
    rol_nombre = data.get('rol_nombre')
    grupo_id = data.get('grupo_id')

    # Validación básica
    if not all([nombre_completo, nombre_usuario, contrasena, rol_nombre]):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    # Verificar que el usuario no exista ya
    if Usuario.query.filter_by(nombre_usuario=nombre_usuario).first():
        return jsonify({"error": "El nombre de usuario ya existe"}), 409

    # Buscar el rol y el grupo por nombre/id
    rol = Rol.query.filter_by(nombre=rol_nombre).first()
    grupo = Grupo.query.get(grupo_id) if grupo_id else None

    if not rol:
        return jsonify({"error": "El rol especificado no existe"}), 404

    # Crear el nuevo usuario
    nuevo_usuario = Usuario(
        nombre_completo=nombre_completo,
        nombre_usuario=nombre_usuario,
        rol_id=rol.id,
        grupo_id=grupo.id if grupo else None
    )
    nuevo_usuario.set_password(contrasena)

    try:
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({
            "message": "Usuario creado exitosamente",
            "id": nuevo_usuario.id,
            "nombre_usuario": nuevo_usuario.nombre_usuario
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Ocurrió un error al crear el usuario: {str(e)}"}), 500
    
# =========================================================
# RUTAS DE ADMINISTRACIÓN PARA GRUPOS
# =========================================================

@app.route('/admin/crear_grupo', methods=['POST'])
def crear_grupo():
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')

    # Validación básica
    if not nombre:
        return jsonify({"error": "El nombre del grupo es obligatorio"}), 400

    # Verificar que el grupo no exista ya
    if Grupo.query.filter_by(nombre=nombre).first():
        return jsonify({"error": "El nombre del grupo ya existe"}), 409

    # Crear el nuevo grupo
    nuevo_grupo = Grupo(nombre=nombre, descripcion=descripcion)

    try:
        db.session.add(nuevo_grupo)
        db.session.commit()
        return jsonify({
            "message": "Grupo creado exitosamente",
            "id": nuevo_grupo.id,
            "nombre": nuevo_grupo.nombre
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Ocurrió un error al crear el grupo: {str(e)}"}), 500

@app.route('/admin/listar_grupos', methods=['GET'])
def listar_grupos():
    grupos = Grupo.query.all()
    lista_grupos = []
    for grupo in grupos:
        lista_grupos.append({
            "id": grupo.id,
            "nombre": grupo.nombre,
            "descripcion": grupo.descripcion
        })
    return jsonify(lista_grupos), 200