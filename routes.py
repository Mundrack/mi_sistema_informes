# Archivo: routes.py

# Archivo: routes.py
from flask import request, jsonify
from app import app, db, bcrypt
from models import Usuario, Rol, Grupo, Informe, SeccionInforme, Monitoreo, DetalleCorreoAtacante, Vulnerabilidad, Incidente, CadenaLlamada 
from datetime import datetime # <--- ¡AÑADE ESTA LÍNEA!

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

# =========================================================
# RUTAS DE ADMINISTRACIÓN PARA USUARIOS
# =========================================================

@app.route('/admin/listar_usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    lista_usuarios = []
    for usuario in usuarios:
        lista_usuarios.append({
            "id": usuario.id,
            "nombre_completo": usuario.nombre_completo,
            "nombre_usuario": usuario.nombre_usuario,
            "rol": usuario.rol.nombre,
            "grupo": usuario.grupo.nombre if usuario.grupo else None,
            "activo": usuario.activo
        })
    return jsonify(lista_usuarios), 200

@app.route('/admin/cambiar_estado_usuario/<int:usuario_id>', methods=['PUT'])
def cambiar_estado_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Cambia el estado (activo a inactivo, o viceversa)
    usuario.activo = not usuario.activo
    
    try:
        db.session.commit()
        estado = "activo" if usuario.activo else "inactivo"
        return jsonify({"message": f"Estado del usuario '{usuario.nombre_usuario}' cambiado a '{estado}'"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Ocurrió un error al actualizar el estado: {str(e)}"}), 500
    
# =========================================================
# RUTAS PARA LA GESTIÓN DE INFORMES
# (Ruta de creación para el rol 'employer')
# =========================================================
@app.route('/informes/crear', methods=['POST'])
def crear_informe():
    data = request.get_json()
    
    # Asumimos que el usuario 'admin' es el que crea el informe.
    # Más adelante, implementaremos la autenticación real.
    usuario = Usuario.query.filter_by(nombre_usuario='admin').first()
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    titulo = data.get('titulo')
    tipo_informe = data.get('tipo_informe')
    if not all([titulo, tipo_informe]):
        return jsonify({"error": "Faltan datos básicos del informe"}), 400

    # Creamos la entrada principal en la tabla 'informes'
    nuevo_informe = Informe(
        titulo=titulo,
        tipo_informe=tipo_informe,
        autor_id=usuario.id
    )

    try:
        db.session.add(nuevo_informe)
        db.session.flush() # Guardamos para obtener el ID, pero no comiteamos

        # Guardar los datos específicos según el tipo de informe
        if tipo_informe == 'monitoreo':
            detalles_monitoreo = data.get('detalles', [])
            for item in detalles_monitoreo:
                nuevo_detalle = Monitoreo(
                    informe_id=nuevo_informe.id,
                    tipo_amenaza=item.get('tipo_amenaza'),
                    valor=item.get('valor')
                )
                db.session.add(nuevo_detalle)
        
        elif tipo_informe == 'boletin':
            contenido = data.get('contenido')
            if contenido:
                seccion = SeccionInforme(
                    informe_id=nuevo_informe.id,
                    contenido_html=contenido
                )
                db.session.add(seccion)
        
        elif tipo_informe == 'vulnerabilidad':
            vulnerabilidades_list = data.get('vulnerabilidades', [])
            for item in vulnerabilidades_list:
                nueva_vulnerabilidad = Vulnerabilidad(
                    informe_id=nuevo_informe.id,
                    nombre_vulnerabilidad=item.get('nombre_vulnerabilidad'),
                    nivel_criticidad=item.get('nivel_criticidad'),
                    sitio_web=item.get('sitio_web'),
                    descripcion=item.get('descripcion'),
                    impacto=item.get('impacto'),
                    mitigacion=item.get('mitigacion')
                )
                db.session.add(nueva_vulnerabilidad)
        
        elif tipo_informe == 'incidente':
            incidente_data = data.get('incidente', {})
            nuevo_incidente = Incidente(
                informe_id=nuevo_informe.id,
                fecha_apertura=datetime.strptime(incidente_data.get('fecha_apertura'), '%Y-%m-%d %H:%M:%S'),
                fecha_cierre=datetime.strptime(incidente_data.get('fecha_cierre'), '%Y-%m-%d %H:%M:%S'),
                asunto=incidente_data.get('asunto'),
                origen=incidente_data.get('origen'),
                detalles=incidente_data.get('detalles'),
                acciones_tomadas=incidente_data.get('acciones_tomadas'),
                estado=incidente_data.get('estado'),
                criticidad=incidente_data.get('criticidad'),
                prioridad=incidente_data.get('prioridad'),
                sitio_afectado=incidente_data.get('sitio_afectado'),
                ip_origen=incidente_data.get('ip_origen'),
                usuario_responsable_id=incidente_data.get('usuario_responsable_id'),
                analista_responsable_id=incidente_data.get('analista_responsable_id')
            )
            db.session.add(nuevo_incidente)
            db.session.flush() # Aquí se asigna el ID para la cadena de llamadas

            cadena_llamadas = incidente_data.get('cadena_llamadas', [])
            for llamada in cadena_llamadas:
                nueva_llamada = CadenaLlamada(
                    incidente_id=nuevo_incidente.id,
                    fecha=datetime.strptime(llamada.get('fecha'), '%Y-%m-%d %H:%M:%S'),
                    persona_contacto=llamada.get('persona_contacto'),
                    area_contacto=llamada.get('area_contacto'),
                    accion_comunicacion=llamada.get('accion_comunicacion'),
                    detalles_comunicacion=llamada.get('detalles_comunicacion')
                )
                db.session.add(nueva_llamada)

        # Si todo va bien, comiteamos todos los cambios al final
        db.session.commit()
        
        return jsonify({
            "message": f"Informe de tipo '{tipo_informe}' creado exitosamente",
            "informe_id": nuevo_informe.id,
            "titulo": nuevo_informe.titulo
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Ocurrió un error al crear el informe: {str(e)}"}), 500
    
    
    