# ============================================================
# CONEXIÓN SQLITE Y OPERACIONES CRUD
# U2 - Paso 3 y 4
# ============================================================


import os
# Importamos os.
# Sirve para trabajar con carpetas y archivos del computador.


import sqlite3
# Importamos sqlite3.
# Permite conectar Python con una base de datos SQLite.



# ============================================================
# UBICACIÓN DE LA BASE DE DATOS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# __file__ representa este archivo Python.
# abspath() obtiene la ruta completa del archivo.
# dirname() obtiene solamente la carpeta donde está el archivo.
#
# En palabras simples:
# "Averigua en qué carpeta está este programa."


DB_NAME = os.path.join(BASE_DIR, "app_ecotech.db")
# os.path.join() une la carpeta con el nombre de la base de datos.
#
# Resultado aproximado:
# C:\MiProyecto\app_ecotech.db
#
# Aquí se define dónde estará guardada la base de datos.



# ============================================================
# FUNCIÓN PARA OBTENER UNA CONEXIÓN
# ============================================================

def obtener_conexion():
    # Esta función se encarga de conectar Python con SQLite.

    """Establece conexión con SQLite activando llaves foráneas
    para integridad referencial."""
    # Este texto explica qué hace la función.


    try:
        # try significa:
        # "Intenta ejecutar este código".
        # Si ocurre un error, pasamos al except.


        conn = sqlite3.connect(DB_NAME)
        # connect() crea una conexión con la base de datos.
        #
        # DB_NAME contiene la ubicación de app_ecotech.db.
        #
        # Si la base de datos no existe, SQLite puede crearla.


        conn.execute("PRAGMA foreign_keys = ON;")
        # Activa las claves foráneas de SQLite.
        #
        # Esto permite controlar las relaciones entre tablas.
        #
        # Por ejemplo:
        # un empleado puede estar relacionado con un departamento.


        return conn
        # Devuelve la conexión.
        # Las otras funciones podrán utilizarla.


    except sqlite3.Error as e:
        # Si ocurre un error relacionado con SQLite,
        # entra aquí.


        print(f"[ERROR CRÍTICO] Fallo al conectar a la BD: {e}")
        # Muestra el mensaje del error.


        return None
        # None significa que no se pudo obtener una conexión.



# ============================================================
# INICIALIZAR LA BASE DE DATOS
# ============================================================

def inicializar_bd():
    # Esta función crea las tablas de la base de datos
    # y agrega algunos datos iniciales.


    """Crea las tablas según el modelo relacional
    y la semántica de la empresa."""
    # Explicación de la función.



    script = """
    # Aquí guardamos varias instrucciones SQL
    # dentro de una cadena de texto.


    CREATE TABLE IF NOT EXISTS departamentos (
        # CREATE TABLE significa "crear una tabla".
        # IF NOT EXISTS significa:
        # "créala solamente si todavía no existe".


        id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
        # ID del departamento.
        # INTEGER = número entero.
        # PRIMARY KEY = identificador único.
        # AUTOINCREMENT = aumenta automáticamente.


        nombre_depto TEXT NOT NULL UNIQUE
        # TEXT = texto.
        # NOT NULL = este campo es obligatorio.
        # UNIQUE = no puede repetirse.
    );


    CREATE TABLE IF NOT EXISTS empleados (

        id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
        # Identificador único del empleado.


        nombre TEXT NOT NULL,
        # Nombre obligatorio.


        rut TEXT UNIQUE NOT NULL,
        # RUT obligatorio.
        # UNIQUE significa que no se puede repetir.


        correo TEXT NOT NULL,
        # Correo obligatorio.


        fecha_ingreso TEXT NOT NULL,
        # Fecha de ingreso.


        salario REAL NOT NULL,
        # REAL permite almacenar números decimales.
        # Aquí se utiliza para el salario.


        cargo TEXT NOT NULL,
        # Cargo del empleado.


        id_departamento INTEGER,
        # Guarda el ID del departamento
        # al que pertenece el empleado.


        FOREIGN KEY (id_departamento)
        REFERENCES departamentos(id_departamento)
        ON DELETE SET NULL
        # FOREIGN KEY = clave foránea.
        #
        # Relaciona empleados con departamentos.
        #
        # ON DELETE SET NULL significa:
        # si se elimina el departamento,
        # el empleado queda sin departamento,
        # pero no se elimina al empleado.
    );


    CREATE TABLE IF NOT EXISTS proyectos (

        id_proyecto INTEGER PRIMARY KEY AUTOINCREMENT,
        # Identificador único del proyecto.


        nombre_proyecto TEXT NOT NULL UNIQUE,
        # Nombre del proyecto.
        # Es obligatorio y no puede repetirse.


        fecha_inicio TEXT NOT NULL
        # Fecha en que comienza el proyecto.
    );


    CREATE TABLE IF NOT EXISTS registro_horas (

        id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
        # Identificador del registro de horas.


        fecha TEXT NOT NULL,
        # Fecha del registro.


        hora_entrada TEXT NOT NULL,
        # Hora en que comienza la jornada.


        hora_salida TEXT NOT NULL,
        # Hora en que termina.


        horas_trabajadas INTEGER NOT NULL,
        # Cantidad de horas trabajadas.


        id_proyecto INTEGER NOT NULL,
        # ID del proyecto relacionado.


        id_empleado INTEGER NOT NULL,
        # ID del empleado relacionado.


        FOREIGN KEY (id_proyecto)
        REFERENCES proyectos(id_proyecto)
        ON DELETE CASCADE,
        # Relaciona el registro con un proyecto.
        #
        # CASCADE significa que si se elimina el proyecto,
        # también se eliminan sus registros relacionados.


        FOREIGN KEY (id_empleado)
        REFERENCES empleados(id_empleado)
        ON DELETE CASCADE
        # Relaciona el registro con un empleado.
        #
        # Si se elimina el empleado,
        # también se eliminan sus registros de horas.
    );


    CREATE TABLE IF NOT EXISTS informes (

        id_informe INTEGER PRIMARY KEY AUTOINCREMENT,
        # Identificador del informe.


        id_empleado INTEGER NOT NULL,
        # Empleado relacionado con el informe.


        id_proyecto INTEGER NOT NULL,
        # Proyecto relacionado.


        id_departamento INTEGER NOT NULL,
        # Departamento relacionado.


        FOREIGN KEY (id_empleado)
        REFERENCES empleados(id_empleado),
        # Relación con la tabla empleados.


        FOREIGN KEY (id_proyecto)
        REFERENCES proyectos(id_proyecto),
        # Relación con la tabla proyectos.


        FOREIGN KEY (id_departamento)
        REFERENCES departamentos(id_departamento)
        # Relación con la tabla departamentos.
    );
    """
    # Aquí termina el script SQL.



    conn = obtener_conexion()
    # Intentamos obtener una conexión con SQLite.


    if conn is None:
        # Preguntamos si la conexión falló.


        return
        # Si no hay conexión, terminamos la función.



    try:
        # Intentamos ejecutar las instrucciones.


        with conn:
            # with ayuda a manejar la conexión
            # y las operaciones de forma segura.


            # Crear las tablas
            conn.executescript(script)
            # Ejecuta todo el script SQL.
            # Aquí se crean las tablas.


            # Poblar datos iniciales si la BD está vacía
            cursor = conn.cursor()
            # cursor permite ejecutar consultas SQL
            # y obtener resultados.



            cursor.execute(
                "SELECT COUNT(*) FROM departamentos;"
            )
            # SELECT = consultar información.
            # COUNT(*) = contar registros.
            #
            # Aquí preguntamos:
            # "¿Cuántos departamentos existen?"



            if cursor.fetchone()[0] == 0:
                # fetchone() obtiene la primera fila del resultado.
                # [0] obtiene el primer valor.
                #
                # Si el resultado es 0,
                # significa que no hay departamentos.


                conn.execute(
                    """
                    INSERT INTO departamentos
                    (id_departamento, nombre_depto)
                    VALUES
                    (13, 'Desarrollo Sostenible'),
                    (1, 'RRHH'),
                    (2, 'Ventas'),
                    (3, 'Investigación y Desarrollo');
                    """
                )
                # INSERT INTO sirve para agregar datos.
                #
                # Aquí agregamos 4 departamentos.



                conn.execute(
                    """
                    INSERT INTO empleados
                    (
                        id_empleado,
                        nombre,
                        rut,
                        correo,
                        fecha_ingreso,
                        salario,
                        cargo,
                        id_departamento
                    )
                    VALUES
                    (
                        1,
                        'Carmen Lopez',
                        '11.111.111-1',
                        'carmen@ecotech.cl',
                        '2022-01-15',
                        1200000,
                        'Analista',
                        13
                    ),
                    (
                        2,
                        'Juan Gomez',
                        '22.222.222-2',
                        'juan@ecotech.cl',
                        '2023-03-10',
                        1400000,
                        'Desarrollador',
                        13
                    );
                    """
                )
                # Agregamos dos empleados.
                #
                # Carmen pertenece al departamento 13.
                # Juan también pertenece al departamento 13.



                conn.execute(
                    """
                    INSERT INTO proyectos
                    (
                        id_proyecto,
                        nombre_proyecto,
                        fecha_inicio
                    )
                    VALUES
                    (
                        25,
                        'Campaña verde',
                        '2023-12-13'
                    ),
                    (
                        14,
                        'Evolución sostenible',
                        '2025-08-14'
                    );
                    """
                )
                # Agregamos dos proyectos iniciales.



    except sqlite3.Error as e:
        # Si ocurre algún error en SQLite,
        # llegamos aquí.


        print(f"[ERROR BD] Fallo en inicialización: {e}")
        # Mostramos el error.



    finally:
        # finally se ejecuta siempre,
        # haya error o no.


        conn.close()
        # Cerramos la conexión con la base de datos.



# ============================================================
# OPERACIONES CRUD DE EMPLEADOS
# ============================================================

# CRUD significa:
#
# C = CREATE  → Crear
# R = READ    → Leer / consultar
# U = UPDATE  → Actualizar
# D = DELETE  → Eliminar



# ============================================================
# CREATE → CREAR EMPLEADO
# ============================================================

def crear_empleado(
    nombre: str,
    rut: str,
    correo: str,
    fecha_ingreso: str,
    salario: float,
    cargo: str,
    id_depto: int
) -> bool:
    # Esta función crea un nuevo empleado.
    #
    # -> bool significa que devolverá:
    # True  → si funcionó
    # False → si ocurrió un problema.


    """Crea un nuevo empleado en la base de datos."""
    # Explica qué hace la función.


    conn = obtener_conexion()
    # Obtenemos una conexión con SQLite.


    if not conn:
        # Si no existe conexión...


        return False
        # Informamos que la operación falló.



    try:
        # Intentamos insertar al empleado.


        cursor = conn.cursor()
        # Creamos un cursor para ejecutar SQL.


        cursor.execute(
            """
            INSERT INTO empleados
            (nombre, rut, correo, fecha_ingreso, salario, cargo, id_departamento)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """,
            (
                nombre,
                rut,
                correo,
                fecha_ingreso,
                salario,
                cargo,
                id_depto
            )
        )
        # INSERT INTO agrega un nuevo empleado.
        #
        # Los signos ? son espacios reservados
        # para los valores que vienen después.
        #
        # Esto es importante porque evita colocar
        # directamente los datos dentro del SQL.


        conn.commit()
        # commit() confirma y guarda los cambios
        # realizados en la base de datos.


        return True
        # Informamos que el empleado fue creado correctamente.



    except sqlite3.IntegrityError as e:
        # Capturamos errores de integridad.
        #
        # Por ejemplo:
        # RUT repetido.
        # Departamento inexistente.


        msg = str(e).lower()
        # Convertimos el error a texto
        # y lo pasamos a minúsculas.



        if "foreign key" in msg:
            # Comprobamos si el problema fue
            # una clave foránea.


            print(
                f"[ERROR] El departamento {id_depto} no existe."
            )
            # Mostramos el error.



        elif "unique" in msg:
            # Comprobamos si el problema fue
            # un valor que debía ser único.


            print(
                f"[ERROR] El RUT '{rut}' ya se encuentra registrado."
            )
            # Avisamos que el RUT ya existe.



        else:
            # Si es otro error de integridad...


            print(f"[ERROR DE INTEGRIDAD]: {e}")
            # Mostramos el detalle.



        conn.rollback()
        # rollback() deshace los cambios
        # realizados si ocurrió un error.


        return False
        # Informamos que no se pudo crear.



    except sqlite3.Error as e:
        # Capturamos otros errores de SQLite.


        print(f"[ERROR BD]: {e}")
        # Mostramos el error.


        conn.rollback()
        # Deshacemos los cambios.


        return False
        # La operación falló.



    finally:
        # Se ejecuta siempre.


        conn.close()
        # Cerramos la conexión.



# ============================================================
# READ → OBTENER EMPLEADOS
# ============================================================

def obtener_empleados() -> list:
    # Esta función consulta todos los empleados.
    # Devuelve una lista.


    """Obtiene todos los empleados de la base de datos."""


    conn = obtener_conexion()
    # Conectamos con la base de datos.


    if not conn:
        # Si no hay conexión...


        return []
        # Devolvemos una lista vacía.



    try:
        # Intentamos realizar la consulta.


        cursor = conn.cursor()
        # Creamos un cursor.


        cursor.execute(
            """
            SELECT
                e.id_empleado,
                e.nombre,
                e.rut,
                e.correo,
                e.fecha_ingreso,
                e.salario,
                e.cargo,
                d.nombre_depto
            FROM empleados e
            LEFT JOIN departamentos d
                ON e.id_departamento = d.id_departamento;
            """
        )
        # SELECT sirve para consultar información.
        #
        # FROM empleados:
        # obtenemos los datos desde empleados.
        #
        # e es un alias para empleados.
        #
        # LEFT JOIN conecta empleados con departamentos.
        #
        # De esta manera podemos obtener también
        # el nombre del departamento.


        return cursor.fetchall()
        # fetchall() obtiene todos los resultados
        # de la consulta.
        #
        # Los devuelve como una lista.



    except sqlite3.Error as e:
        # Capturamos errores de SQLite.


        print(f"[ERROR BD]: {e}")
        # Mostramos el error.


        return []
        # Devolvemos una lista vacía si falló.



    finally:
        # Siempre se ejecuta.


        conn.close()
        # Cerramos la conexión.



# ============================================================
# UPDATE → ACTUALIZAR EMPLEADO
# ============================================================

def actualizar_empleado(
    id_emp: int,
    nombre: str,
    correo: str,
    salario: float,
    cargo: str
) -> bool:
    # Esta función modifica los datos de un empleado.
    #
    # Recibe el ID del empleado
    # y los nuevos datos.


    """Actualiza un empleado."""


    conn = obtener_conexion()
    # Obtenemos una conexión.


    if not conn:
        # Si no hay conexión...


        return False
        # Informamos que falló.



    try:
        # Intentamos actualizar.


        with conn:
            # Maneja automáticamente la operación
            # de la transacción.


            cursor = conn.execute(
                """
                UPDATE empleados
                SET nombre = ?,
                    correo = ?,
                    salario = ?,
                    cargo = ?
                WHERE id_empleado = ?;
                """,
                (
                    nombre,
                    correo,
                    salario,
                    cargo,
                    id_emp
                )
            )
            # UPDATE modifica información existente.
            #
            # SET indica qué campos vamos a cambiar.
            #
            # WHERE indica qué empleado modificaremos.
            #
            # MUY IMPORTANTE:
            # WHERE evita modificar a todos los empleados.
            #
            # Solo modifica al empleado cuyo ID coincida.


            return cursor.rowcount > 0
            # rowcount indica cuántas filas fueron modificadas.
            #
            # Si es mayor que 0:
            # True → se actualizó.
            #
            # Si es 0:
            # False → no encontró ese empleado.



    except sqlite3.Error as e:
        # Capturamos errores de SQLite.


        print(f"[ERROR BD]: {e}")
        # Mostramos el error.


        return False
        # Informamos que falló.



    finally:
        # Siempre se ejecuta.


        conn.close()
        # Cerramos la conexión.



# ============================================================
# DELETE → ELIMINAR EMPLEADO
# ============================================================

def eliminar_empleado(id_emp: int) -> bool:
    # Esta función elimina un empleado.
    #
    # Recibe el ID del empleado que queremos eliminar.


    """Elimina un empleado de la base de datos."""


    conn = obtener_conexion()
    # Obtenemos conexión con SQLite.


    if not conn:
        # Si no hay conexión...


        return False
        # La operación falla.



    try:
        # Intentamos eliminar al empleado.


        with conn:
            # Maneja la operación de forma segura.


            cursor = conn.execute(
                """
                DELETE FROM empleados
                WHERE id_empleado = ?;
                """,
                (id_emp,)
            )
            # DELETE FROM elimina registros.
            #
            # WHERE indica cuál empleado eliminar.
            #
            # El ? se reemplaza por id_emp.



            return cursor.rowcount > 0
            # Si se eliminó una fila:
            # True.
            #
            # Si no encontró al empleado:
            # False.



    except sqlite3.IntegrityError as e:
        # Capturamos errores de integridad.


        print(
            "[ERROR DE INTEGRIDAD] "
            "No se puede eliminar el empleado porque "
            "existen registros relacionados."
        )
        # Mostramos un mensaje indicando
        # que existen datos relacionados.


        print(f"Detalle técnico: {e}")
        # Mostramos el detalle técnico del error.


        return False
        # Informamos que no se pudo eliminar.



    except sqlite3.Error as e:
        # Capturamos cualquier otro error de SQLite.


        print(f"[ERROR BD] No se pudo eliminar el empleado: {e}")
        # Mostramos el error.


        return False
        # La operación falló.



    finally:
        # Se ejecuta siempre.


        conn.close()
        # Cerramos la conexión.