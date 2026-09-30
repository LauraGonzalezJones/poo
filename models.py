# models.py
# Este archivo contiene las clases y modelos de datos del sistema.


from datetime import datetime
# Importamos datetime para poder trabajar con fechas y horas.


class Persona:
    # Creamos la clase Persona.
    # Esta será la clase general o "padre".

    def __init__(self, nombre: str, rut: str, correo: str):
        # __init__ es el constructor.
        # Se ejecuta automáticamente cuando creamos una Persona.
        # self representa al objeto que estamos creando.
        # str significa que esperamos recibir texto.

        self.nombre = nombre
        # Guardamos el nombre de la persona.

        self._rut = rut
        # Guardamos el RUT.
        # El "_" indica que es un atributo interno/protegido.

        self.correo = correo
        # Guardamos el correo de la persona.


    # --------------------------------------------------
    # GETTERS Y SETTERS
    # Se utilizan para controlar el acceso a los atributos.
    # --------------------------------------------------

    @property
    # @property permite consultar un atributo mediante un método.

    def nombre(self) -> str:
        # Este método permite obtener el nombre.

        return self._nombre
        # Devuelve el nombre que está guardado.


    @nombre.setter
    # Permite modificar el nombre de forma controlada.

    def nombre(self, nuevo_nombre: str):
        # Recibe el nuevo nombre.

        if not nuevo_nombre or not nuevo_nombre.strip():
            # Comprueba si el nombre está vacío
            # o contiene solamente espacios.

            raise ValueError("El nombre no puede estar vacío.")
            # Si está vacío, genera un error.

        self._nombre = nuevo_nombre.strip()
        # Guarda el nuevo nombre.
        # strip() elimina espacios al principio y al final.


    @property
    # Permite consultar el RUT.

    def rut(self) -> str:

        return self._rut
        # Devuelve el RUT.


    @property
    # Permite consultar el correo.

    def correo(self) -> str:

        return self._correo
        # Devuelve el correo.


    @correo.setter
    # Permite modificar el correo.

    def correo(self, nuevo_correo: str):

        self._correo = nuevo_correo
        # Guarda el nuevo correo.



# ======================================================
# CLASE EMPLEADO
# ======================================================

class Empleado(Persona):
    # Empleado hereda de Persona.
    # Esto representa HERENCIA en POO.
    # Un Empleado es una Persona, pero tiene datos adicionales.

    def __init__(
        self,
        id_empleado: int,
        nombre: str,
        rut: str,
        correo: str,
        fecha_ingreso: str = None,
        salario: float = 0.0,
        cargo: str = None
    ):
        # Constructor de Empleado.
        # Recibe los datos personales y laborales.
        # int = número entero.
        # float = número decimal.
        # None = no se ha entregado un valor.


        # --------------------------------------------------
        # Inicializamos los atributos heredados de Persona.
        # --------------------------------------------------

        super().__init__(
            nombre=nombre,
            rut=rut,
            correo=correo
        )
        # super() permite llamar al constructor de la clase padre.
        # En este caso, Persona.
        # Así reutilizamos el código de Persona.


        # --------------------------------------------------
        # Atributos propios de Empleado.
        # --------------------------------------------------

        self._id_empleado = id_empleado
        # Guardamos el ID del empleado.

        self._fecha_ingreso = fecha_ingreso
        # Guardamos la fecha en que ingresó el empleado.

        self._salario = salario
        # Guardamos el salario.

        self._cargo = cargo
        # Guardamos el cargo del empleado.


    @property
    # Permite consultar el ID del empleado.

    def id_empleado(self) -> int:

        return self._id_empleado
        # Devuelve el ID del empleado.


    @property
    # Permite consultar la fecha de ingreso.

    def fecha_ingreso(self) -> str:

        return self._fecha_ingreso
        # Devuelve la fecha de ingreso.


    @fecha_ingreso.setter
    # Permite modificar la fecha de ingreso.

    def fecha_ingreso(self, nueva_fecha: str):

        self._fecha_ingreso = nueva_fecha
        # Guarda la nueva fecha.


    @property
    # Permite consultar el salario.

    def salario(self) -> float:

        return self._salario
        # Devuelve el salario.


    @salario.setter
    # Permite modificar el salario.

    def salario(self, nuevo_salario: float):

        self._salario = nuevo_salario
        # Guarda el nuevo salario.


    @property
    # Permite consultar el cargo.

    def cargo(self) -> str:

        return self._cargo
        # Devuelve el cargo.


    @cargo.setter
    # Permite modificar el cargo.

    def cargo(self, nuevo_cargo: str):

        self._cargo = nuevo_cargo
        # Guarda el nuevo cargo.



# ======================================================
# CLASE DEPARTAMENTO
# ======================================================

class Departamento:
    # Representa un departamento de la empresa.


    def __init__(self, id_departamento: int, nombre: str):
        # Constructor del departamento.
        # Recibe el ID y el nombre.

        self._id_departamento = id_departamento
        # Guarda el ID del departamento.

        self._nombre = nombre
        # Guarda el nombre del departamento.


    @property
    # Permite consultar el ID del departamento.

    def id_departamento(self):

        return self._id_departamento
        # Devuelve el ID.


    @property
    # Permite consultar el nombre.

    def nombre(self):

        return self._nombre
        # Devuelve el nombre del departamento.



# ======================================================
# CLASE PROYECTO
# ======================================================

class Proyecto:
    # Representa un proyecto de EcoTech Solutions.


    def __init__(
        self,
        id_proyecto: int,
        nombre_proyecto: str,
        fecha_inicio: str
    ):
        # Constructor del proyecto.
        # Recibe ID, nombre y fecha de inicio.

        self.id_proyecto = id_proyecto
        # Guarda el ID del proyecto.

        self.nombre_proyecto = nombre_proyecto
        # Guarda el nombre del proyecto.

        self.fecha_inicio = fecha_inicio
        # Guarda la fecha de inicio.


        self._empleados: list[Empleado] = []
        # Creamos una lista vacía.
        # Aquí se guardarán los empleados asignados al proyecto.
        # Al principio no hay ningún empleado.



    def asignar_empleado(self, empleado: Empleado) -> str:
        # Método que permite asignar un empleado al proyecto.
        # Recibe un objeto de tipo Empleado.


        if empleado not in self._empleados:
            # Comprobamos si el empleado NO está en la lista.


            self._empleados.append(empleado)
            # append() agrega el empleado a la lista.


            return (
                f"Empleado {empleado.nombre} asignado al proyecto "
                f"{self.nombre_proyecto}."
            )
            # Devuelve un mensaje confirmando la asignación.


        return (
            f"El empleado {empleado.nombre} ya está asignado al proyecto "
            f"{self.nombre_proyecto}."
        )
        # Si el empleado ya estaba asignado,
        # devuelve un mensaje informándolo.



    def desasignar_empleado(self, empleado: Empleado) -> str:
        # Método que permite quitar un empleado del proyecto.


        if empleado in self._empleados:
            # Comprobamos si el empleado está en la lista.


            self._empleados.remove(empleado)
            # remove() elimina al empleado de la lista.


            return (
                f"Empleado {empleado.nombre} removido del proyecto "
                f"{self.nombre_proyecto}."
            )
            # Devuelve un mensaje confirmando que fue removido.


        return (
            f"El empleado {empleado.nombre} no está asignado al proyecto "
            f"{self.nombre_proyecto}."
        )
        # Si el empleado no estaba asignado,
        # informa que no se puede quitar.



    @property
    # Permite consultar los empleados del proyecto.

    def empleados(self) -> list[Empleado]:

        return self._empleados.copy()
        # Devuelve una copia de la lista.
        # Esto ayuda a proteger la lista original.
        # Es parte del ENCAPSULAMIENTO.



# ======================================================
# CLASE REGISTROHORAS
# ======================================================

class RegistroHoras:
    # Representa el registro de horas trabajadas
    # por un empleado en un proyecto.


    def __init__(
        self,
        id_registro: int,
        id_empleado: int,
        id_proyecto: int,
        horas_trabajadas: int,
        fecha: str = None,
        hora_entrada: str = "09:00",
        hora_salida: str = "18:00"
    ):
        # Constructor de RegistroHoras.


        self._id_registro = id_registro
        # Guarda el ID del registro.


        self._id_empleado = id_empleado
        # Guarda el ID del empleado.


        self._id_proyecto = id_proyecto
        # Guarda el ID del proyecto.


        self._horas_trabajadas = horas_trabajadas
        # Guarda la cantidad de horas trabajadas.


        self._fecha = fecha or datetime.now().strftime("%Y-%m-%d")
        # Si recibimos una fecha, usamos esa fecha.
        # Si no recibimos fecha, usamos la fecha actual.
        # datetime.now() obtiene la fecha y hora actual.
        # strftime() permite darle formato a la fecha.


        self._hora_entrada = hora_entrada
        # Guarda la hora de entrada.
        # Por defecto es 09:00.


        self._hora_salida = hora_salida
        # Guarda la hora de salida.
        # Por defecto es 18:00.



    @property
    # Permite consultar el ID del registro.

    def id_registro(self) -> int:

        return self._id_registro
        # Devuelve el ID del registro.



    @property
    # Permite consultar el ID del empleado.

    def id_empleado(self) -> int:

        return self._id_empleado
        # Devuelve el ID del empleado.



    @property
    # Permite consultar el ID del proyecto.

    def id_proyecto(self) -> int:

        return self._id_proyecto
        # Devuelve el ID del proyecto.



    @property
    # Permite consultar las horas trabajadas.

    def horas_trabajadas(self) -> int:

        return self._horas_trabajadas
        # Devuelve las horas trabajadas.



    @horas_trabajadas.setter
    # Permite modificar las horas trabajadas.

    def horas_trabajadas(self, nuevas_horas: int):

        self._horas_trabajadas = nuevas_horas
        # Guarda la nueva cantidad de horas.



    @property
    # Permite consultar la fecha.

    def fecha(self) -> str:

        return self._fecha
        # Devuelve la fecha del registro.



    @property
    # Permite consultar la hora de entrada.

    def hora_entrada(self) -> str:

        return self._hora_entrada
        # Devuelve la hora de entrada.



    @property
    # Permite consultar la hora de salida.

    def hora_salida(self) -> str:

        return self._hora_salida
        # Devuelve la hora de salida.



    def registrar_horas(self) -> str:
        # Método que confirma el registro de horas.


        return (
            f"Registradas {self.horas_trabajadas} hrs "
            f"para empleado ID {self.id_empleado} "
            f"en proyecto ID {self.id_proyecto}."
        )
        # Devuelve un mensaje con las horas registradas,
        # el empleado y el proyecto.



    def consultar_horas(self) -> int:
        # Método que permite consultar las horas trabajadas.

        return self.horas_trabajadas
        # Devuelve la cantidad de horas.



# ======================================================
# CLASE INFORME
# ======================================================

class Informe:
    # Representa información consolidada del sistema.


    def __init__(
        self,
        id_informe: int,
        id_empleado: int,
        id_proyecto: int,
        id_departamento: int,
        reporte_horas: str = "",
        reporte_proyecto: str = "",
        reporte_empleado: str = ""
    ):
        # Constructor del informe.


        self._id_informe = id_informe
        # Guarda el ID del informe.


        self._id_empleado = id_empleado
        # Guarda el ID del empleado asociado.


        self._id_proyecto = id_proyecto
        # Guarda el ID del proyecto asociado.


        self._id_departamento = id_departamento
        # Guarda el ID del departamento asociado.


        self._reporte_horas = reporte_horas
        # Guarda el reporte de horas.


        self._reporte_proyecto = reporte_proyecto
        # Guarda el reporte del proyecto.


        self._reporte_empleado = reporte_empleado
        # Guarda el reporte del empleado.



    @property
    # Permite consultar el ID del informe.

    def id_informe(self) -> int:

        return self._id_informe
        # Devuelve el ID del informe.



    @property
    # Permite consultar el ID del empleado.

    def id_empleado(self) -> int:

        return self._id_empleado
        # Devuelve el ID del empleado.



    @property
    # Permite consultar el ID del proyecto.

    def id_proyecto(self) -> int:

        return self._id_proyecto
        # Devuelve el ID del proyecto.



    @property
    # Permite consultar el ID del departamento.

    def id_departamento(self) -> int:

        return self._id_departamento
        # Devuelve el ID del departamento.



    @property
    # Permite consultar el reporte de horas.

    def reporte_horas(self) -> str:

        return self._reporte_horas
        # Devuelve el reporte de horas.


    @reporte_horas.setter
    # Permite modificar el reporte de horas.

    def reporte_horas(self, nuevo_reporte: str):

        self._reporte_horas = nuevo_reporte
        # Guarda el nuevo reporte.



    @property
    # Permite consultar el reporte del proyecto.

    def reporte_proyecto(self) -> str:

        return self._reporte_proyecto
        # Devuelve el reporte del proyecto.


    @reporte_proyecto.setter
    # Permite modificar el reporte del proyecto.

    def reporte_proyecto(self, nuevo_reporte: str):

        self._reporte_proyecto = nuevo_reporte
        # Guarda el nuevo reporte.



    @property
    # Permite consultar el reporte del empleado.

    def reporte_empleado(self) -> str:

        return self._reporte_empleado
        # Devuelve el reporte del empleado.


    @reporte_empleado.setter
    # Permite modificar el reporte del empleado.

    def reporte_empleado(self, nuevo_reporte: str):

        self._reporte_empleado = nuevo_reporte
        # Guarda el nuevo reporte.



    def generar_reporte(self) -> str:
        # Método que genera un resumen del informe.


        return (
            f"Informe #{self.id_informe} "
            f"[Empleado: {self.id_empleado}, "
            f"Proyecto: {self.id_proyecto}, "
            f"Depto: {self.id_departamento}]"
        )
        # Devuelve un texto con la información principal
        # del informe.