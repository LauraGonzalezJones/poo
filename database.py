import os
import sqlite3

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
    -- Aquí guardamos varias instrucciones SQL dentro de una cadena de texto.

    CREATE TABLE IF NOT EXISTS departamentos (
        -- CREATE TABLE significa "crear una tabla".
        -- IF NOT EXISTS significa: "créala solamente si todavía no existe".


        id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
        -- ID del departamento.
        -- INTEGER = número entero.
        -- PRIMARY KEY = identificador único.
        -- AUTOINCREMENT = aumenta automáticamente.


        nombre_depto TEXT NOT NULL UNIQUE
        -- TEXT = texto.
        -- NOT NULL = este campo es obligatorio.
        -- UNIQUE = no puede repetirse.
    );


    CREATE TABLE IF NOT EXISTS empleados (

        id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
        -- Identificador único del empleado.


        nombre TEXT NOT NULL,
        -- Nombre obligatorio.


        rut TEXT UNIQUE NOT NULL,
        -- RUT obligatorio.
        -- UNIQUE significa que no se puede repetir.


        correo TEXT NOT NULL,
        -- Correo obligatorio.


        fecha_ingreso TEXT NOT NULL,
        -- Fecha de ingreso.


        salario REAL NOT NULL,
        -- REAL permite almacenar números decimales.
        -- Aquí se utiliza para el salario.


        cargo TEXT NOT NULL,
        -- Cargo del empleado.


        id_departamento INTEGER,
        -- Guarda el ID del departamento al que pertenece el empleado.


        FOREIGN KEY (id_departamento)
        REFERENCES departamentos(id_departamento)
        ON DELETE SET NULL
        -- FOREIGN KEY = clave foránea.
        -- Relaciona empleados con departamentos.
        -- ON DELETE SET NULL significa: si se elimina el departamento,
        -- el empleado queda sin departamento, pero no se elimina al empleado.
    );


    CREATE TABLE IF NOT EXISTS proyectos (

        id_proyecto INTEGER PRIMARY KEY AUTOINCREMENT,
        -- Identificador único del proyecto.


        nombre_proyecto TEXT NOT NULL UNIQUE,
        -- Nombre del proyecto.
        -- Es obligatorio y no puede repetirse.


        fecha_inicio TEXT NOT NULL
        -- Fecha en que comienza el proyecto.
    );


    CREATE TABLE IF NOT EXISTS registro_horas (

        id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
        -- Identificador del registro de horas.


        fecha TEXT NOT NULL,
        -- Fecha del registro.


        hora_entrada TEXT NOT NULL,
        -- Hora en que comienza la jornada.


        hora_salida TEXT NOT NULL,
        -- Hora en que termina.


        horas_trabajadas INTEGER NOT NULL,
        -- Cantidad de horas trabajadas.


        id_proyecto INTEGER NOT NULL,
        -- ID del proyecto relacionado.


        id_empleado INTEGER NOT NULL,
        -- ID del empleado relacionado.


        FOREIGN KEY (id_proyecto)
        REFERENCES proyectos(id_proyecto)
        ON DELETE CASCADE,
        -- Relaciona el registro con un proyecto.
        -- CASCADE significa que si se elimina el proyecto,
        -- también se eliminan sus registros relacionados.


        FOREIGN KEY (id_empleado)
        REFERENCES empleados(id_empleado)
        ON DELETE CASCADE
        -- Relaciona el registro con un empleado.
        -- Si se elimina el empleado, también se eliminan sus registros de horas.
    );


    CREATE TABLE IF NOT EXISTS informes (

        id_informe INTEGER PRIMARY KEY AUTOINCREMENT,
        -- Identificador del informe.


        id_empleado INTEGER NOT NULL,
        -- Empleado relacionado con el informe.


        id_proyecto INTEGER NOT NULL,
        -- Proyecto relacionado.


        id_departamento INTEGER NOT NULL,
        -- Departamento relacionado.


        FOREIGN KEY (id_empleado)
        REFERENCES empleados(id_empleado),
        -- Relación con la tabla empleados.


        FOREIGN KEY (id_proyecto)
        REFERENCES proyectos(id_proyecto),
        -- Relación con la tabla proyectos.


        FOREIGN KEY (id_departamento)
        REFERENCES departamentos(id_departamento)
        -- Relación con la tabla departamentos.
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
                # Aquí agregamos 4 departamentos.


                # Agregamos los empleados iniciales correspondientes a los departamentos creados
                conn.execute(
                    """
                    INSERT INTO empleados
                    (nombre, rut, correo, fecha_ingreso, salario, cargo, id_departamento)
                    VALUES
                    ('Admin EcoTech', '11111111-1', 'admin@ecotech.cl', '2026-01-01', 1500000.0, 'Administrador', 1);
                    """
                )
                print("[BD] Base de datos inicializada y poblada con éxito.")

    except sqlite3.Error as error_sql:
        print(f"[ERROR BD] Fallo en inicialización: {error_sql}")
