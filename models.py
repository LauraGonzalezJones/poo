from datetime import datetime

class Persona:
    """Clase base que abstrae los datos fundamentales de una persona."""
    def __init__(self, nombre: str, rut: str):
        self._nombre = nombre
        self._rut = rut

    @property #metadato que indica que el método siguiente es un getter, lo que permite acceder al valor de un atributo de manera controlada.
    def nombre(self) -> str:
        """Devuelve el nombre de la persona."""
        return self._nombre
    @nombre.setter
    def nombre(self,nuevo_nombre:str):
        if not nuevo_nombre:
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = nuevo_nombre

    @property#metadato que indica que el método siguiente es un getter, lo que permite acceder al valor de un atributo de manera controlada.
    def rut(self) -> str:
        """Devuelve el RUT de la persona."""
        return self._rut
    
class Empleado(Persona):
    """Clase que representa a un empleado, heredando de Persona."""
    def __init__(self, id_empleado: int, nombre: str, rut: str,correo: str, fecha_ingreso: datetime, salario: float, cargo: str):
        super().__init__(nombre, rut)
        self.__id_empleado = id_empleado
        self.correo = correo
        self.fecha_ingreso = fecha_ingreso
        self.salario = salario
        self.cargo = cargo

class Proyecto:
    """Identifica un proyecto en curso con su fecha de inicio."""
    def __init__(self, id_proyecto: int, nombre_proyecto: str, fecha_inicio: str):
        self.id_proyecto = id_proyecto
        self.nombre_proyecto = nombre_proyecto
        self.fecha_inicio = fecha_inicio

    def asignar_empleado(self, empleado: Empleado) -> str:
        return f"Empleado {empleado.nombre} asignado al proyecto {self.nombre_proyecto}."

    def desasignar_empleado(self, empleado: Empleado) -> str:
        return f"Empleado {empleado.nombre} removido del proyecto {self.nombre_proyecto}."


class RegistroHoras:
    """Trazabilidad de horas trabajadas por empleado y proyecto asignado."""
    def __init__(self, id_registro: int, id_empleado: int, id_proyecto: int, horas_trabajadas: int, fecha: str = None, hora_entrada: str = "09:00", hora_salida: str = "18:00"):
        self.id_registro = id_registro
        self.id_empleado = id_empleado
        self.id_proyecto = id_proyecto
        self.horas_trabajadas = horas_trabajadas
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d")
        self.hora_entrada = hora_entrada
        self.hora_salida = hora_salida

    def registrar_horas(self) -> str:
        return f"Registradas {self.horas_trabajadas} hrs para empleado ID {self.id_empleado} en proyecto ID {self.id_proyecto}."

    def consultar_horas(self) -> int:
        return self.horas_trabajadas


class Informe:
    """Información consolidada generada a solicitud de las partes interesadas."""
    def __init__(self, id_informe: int, id_empleado: int, id_proyecto: int, id_departamento: int, reporte_horas: str = "", reporte_proyecto: str = "", reporte_empleado: str = ""):
        self.id_informe = id_informe
        self.id_empleado = id_empleado
        self.id_proyecto = id_proyecto
        self.id_departamento = id_departamento
        self.reporte_horas = reporte_horas
        self.reporte_proyecto = reporte_proyecto
        self.reporte_empleado = reporte_empleado

    def generar_reporte(self) -> str:
        return f"Informe #{self.id_informe} [Empleado: {self.id_empleado}, Proyecto: {self.id_proyecto}, Depto: {self.id_departamento}]"
