"""main.py - Interfaz de Consola e Integración."""
# Este es el archivo principal del programa.
# Se encarga de mostrar el menú, recibir los datos del usuario
# y conectar los demás archivos del proyecto.


from getpass import getpass
# getpass permite pedir una contraseña sin mostrarla
# directamente en la pantalla mientras el usuario escribe.


''' '''
# Esto es una cadena de texto vacía.
# No cumple una función importante en este programa.
# Se podría eliminar sin afectar el funcionamiento.


from models import Empleado
# Importamos la clase Empleado desde models.py.
# La utilizaremos para crear objetos Empleado
# cuando mostremos los empleados registrados.


from database import (
    inicializar_bd, crear_empleado, obtener_empleados,
    actualizar_empleado, eliminar_empleado
)
# Importamos las funciones que trabajan con la base de datos.
#
# inicializar_bd()      -> crea las tablas y datos iniciales.
# crear_empleado()      -> guarda un empleado.
# obtener_empleados()   -> consulta empleados.
# actualizar_empleado() -> modifica un empleado.
# eliminar_empleado()   -> elimina un empleado.


from auth import autenticar_usuario
# Importamos la función que comprueba
# el usuario y contraseña.


from services import (
    obtener_indicador_economico,
    obtener_clima_santiago,
    validar_moneda
)
# Importamos las funciones que trabajan con APIs externas.
#
# obtener_indicador_economico() -> consulta dólar, euro o UF.
# obtener_clima_santiago()      -> consulta el clima.
# validar_moneda()              -> comprueba la moneda ingresada.


from validaciones import (
    validar_nombre,
    validar_correo,
    validar_fecha,
    validar_salario,
    validar_cargo
)
# Importamos las funciones que validan los datos
# ingresados por el usuario.
#
# validar_nombre()  -> comprueba el nombre.
# validar_correo()  -> comprueba el correo.
# validar_fecha()   -> comprueba la fecha.
# validar_salario() -> comprueba el salario.
# validar_cargo()   -> comprueba el cargo.


def login():
    # Esta función se encarga del inicio de sesión.

    """Solicita credenciales al usuario y verifica autenticación."""

    print("=== SISTEMA DE GESTIÓN DE EMPLEADOS - ECOTECH SOLUTIONS ===")
    # Muestra el título del sistema.


    intentos = 0
    # Contador que comienza en cero.
    # Se utilizará para controlar los intentos de inicio de sesión.


    while intentos < 3:
        # Mientras los intentos sean menores que 3,
        # el usuario puede intentar iniciar sesión.


        user = input("Usuario: ").strip()
        # Solicita el nombre de usuario.
        # strip() elimina espacios innecesarios.


        pwd = getpass("Contraseña: ").strip()
        # Solicita la contraseña.
        #
        # getpass() hace que la contraseña no se muestre
        # directamente mientras se escribe.


        if autenticar_usuario(user, pwd):
            # Enviamos usuario y contraseña a auth.py.
            #
            # Si son correctos, devuelve True.


            print(
                f"\n[OK] Autenticación exitosa. "
                f"Bienvenido, {user.capitalize()}.\n"
            )
            # Mostramos un mensaje de bienvenida.
            #
            # capitalize() coloca la primera letra en mayúscula.


            return True
            # True significa que el inicio de sesión
            # fue exitoso.


        else:
            # Si usuario o contraseña son incorrectos...

            intentos += 1
            # Aumentamos el contador de intentos en 1.


            print(
                f"[ACCESO DENEGADO] "
                f"Intentos restantes: {3 - intentos}\n"
            )
            # Informamos cuántos intentos quedan.


    return False
    # Si llega aquí significa que se utilizaron
    # los 3 intentos sin éxito.


def menu_principal():
    # Esta función muestra y controla el menú principal.

    """Muestra el menu principal y gestiona las opciones del usuario."""


    while True:
        # El menú se mantiene funcionando
        # hasta que el usuario seleccione "Salir".


        print("=== MENÚ PRINCIPAL ===")
        print("1. Registrar Empleado (CREATE)")
        print("2. Listar Empleados (READ)")
        print("3. Actualizar Empleado (UPDATE)")
        print("4. Eliminar Empleado (DELETE)")
        print("5. Consultar Clima para Proyectos (API)")
        print("6. Consultar Indicador Económico / Salarios (API)")
        print("7. Salir")
        # Estas líneas muestran las opciones disponibles.


        opcion = input("Seleccione una opción: ").strip()
        # El usuario escribe el número de la opción.


        if opcion == "1":
            # Si el usuario selecciona 1,
            # comienza el registro de un empleado.


            print("\n--- REGISTRO DE EMPLEADO ---")


            nombre = input(
                "Nombre completo (ej. Carmen Lopez): "
            ).strip()
            # Pedimos el nombre.


            rut = input("RUT: ").strip()
            # Pedimos el RUT.


            correo = input("Correo electrónico: ").strip()
            # Pedimos el correo.


            fecha_ing = input(
                "Fecha de ingreso (YYYY-MM-DD): "
            ).strip()
            # Pedimos la fecha de ingreso.


            cargo = input("Cargo: ").strip()
            # Pedimos el cargo.


            if not validar_nombre(nombre):
                # Comprobamos si el nombre es válido.

                print(
                    "[ERROR] El nombre no puede estar vacío.\n"
                )

                continue
                # continue vuelve al comienzo del menú.
                # No continúa con el resto del registro.


            if not rut:
                # Comprueba si el RUT está vacío.

                print(
                    "[ERROR] El RUT no puede estar vacío.\n"
                )

                continue


            if not validar_correo(correo):
                # Comprueba que el correo tenga un formato válido.

                print(
                    "[ERROR] El correo electrónico "
                    "no tiene un formato válido.\n"
                )

                continue


            if not validar_fecha(fecha_ing):
                # Comprueba que la fecha sea válida.

                print(
                    "[ERROR] La fecha debe ser válida "
                    "y usar el formato YYYY-MM-DD.\n"
                )

                continue


            if not validar_cargo(cargo):
                # Comprueba que el cargo no esté vacío.

                print(
                    "[ERROR] El cargo no puede estar vacío.\n"
                )

                continue


            try:
                # Intentamos convertir los datos numéricos.


                salario = float(input("Salario ($): "))
                # float() convierte el texto ingresado
                # en un número decimal.
                #
                # Ejemplo:
                # "1200000" -> 1200000.0


                id_depto = int(
                    input(
                        "ID Departamento "
                        "(ej. 13 - Dev. Sostenible): "
                    )
                )
                # int() convierte el texto en un número entero.
                #
                # Ejemplo:
                # "13" -> 13


                if not validar_salario(salario):
                    # Comprueba que el salario sea mayor que cero.

                    print(
                        "[ERROR] El salario debe ser mayor que cero.\n"
                    )

                    continue


                if crear_empleado(
                    nombre,
                    rut,
                    correo,
                    fecha_ing,
                    salario,
                    cargo,
                    id_depto
                ):
                    # Llama a database.py para guardar
                    # el empleado en SQLite.

                    print(
                        "[ÉXITO] Empleado guardado en BD.\n"
                    )


            except ValueError:
                # Si el usuario escribe algo que no puede
                # convertirse a número, aparece este error.

                print(
                    "[ERROR] El salario y el ID de departamento "
                    "deben ser numéricos.\n"
                )


        elif opcion == "2":
            # Opción 2: consultar y mostrar empleados.


            print(
                "\n--- LISTA DE EMPLEADOS (INSTANCIAS POO) ---"
            )


            registros = obtener_empleados()
            # Pedimos a database.py todos los empleados
            # almacenados en SQLite.


            if not registros:
                # Si la lista está vacía...

                print(
                    "No hay empleados registrados."
                )


            for r in registros:
                # Recorremos cada empleado obtenido
                # desde la base de datos.


                # Aquí volvemos a convertir los datos
                # de la BD en un objeto de la clase Empleado.
                #
                # Esto permite aplicar el enfoque POO.

                emp = Empleado(
                    id_empleado=r[0],
                    nombre=r[1],
                    rut=r[2],
                    correo=r[3],
                    fecha_ingreso=r[4],
                    salario=r[5],
                    cargo=r[6]
                )


                print(
                    f"ID:{emp.id_empleado} | "
                    f"Nombre: {emp.nombre} | "
                    f"RUT: {emp.rut} | "
                    f"Cargo: {emp.cargo} | "
                    f"Salario: ${emp.salario}"
                )
                # Mostramos los datos del objeto Empleado.


            print()


        elif opcion == "3":
            # Opción 3: actualizar un empleado.


            print("\n--- ACTUALIZAR EMPLEADO ---")


            try:
                # Intentamos convertir el ID y salario
                # a números.


                emp_id = int(
                    input("ID de empleado a actualizar: ")
                )
                # Solicitamos el ID del empleado.


                nom = input("Nuevo nombre: ").strip()
                # Nuevo nombre.


                correo = input("Nuevo correo: ").strip()
                # Nuevo correo.


                cargo = input("Nuevo cargo: ").strip()
                # Nuevo cargo.


                salario = float(
                    input("Nuevo salario: ")
                )
                # Nuevo salario.


                if not validar_nombre(nom):
                    # Validamos el nuevo nombre.

                    print(
                        "[ERROR] El nombre no puede estar vacío.\n"
                    )

                    continue


                if not validar_correo(correo):
                    # Validamos el nuevo correo.

                    print(
                        "[ERROR] El correo electrónico "
                        "no tiene un formato válido.\n"
                    )

                    continue


                if not validar_cargo(cargo):
                    # Validamos el nuevo cargo.

                    print(
                        "[ERROR] El cargo no puede estar vacío.\n"
                    )

                    continue


                if not validar_salario(salario):
                    # Validamos el nuevo salario.

                    print(
                        "[ERROR] El salario debe ser mayor que cero.\n"
                    )

                    continue


                if actualizar_empleado(
                    emp_id,
                    nom,
                    correo,
                    salario,
                    cargo
                ):
                    # Llamamos a database.py para modificar
                    # el registro en SQLite.

                    print(
                        "[ÉXITO] Empleado actualizado.\n"
                    )


                else:
                    # Si no se encontró ese ID...

                    print(
                        "[ERROR] ID no encontrado.\n"
                    )


            except ValueError:
                # Si el usuario ingresa un valor que no puede
                # convertirse en número...

                print(
                    "[ERROR] El ID y el salario deben contener "
                    "valores numéricos válidos.\n"
                )


        elif opcion == "4":
            # Opción 4: eliminar un empleado.


            try:
                # Intentamos obtener el ID.


                emp_id = int(
                    input("ID de empleado a eliminar: ")
                )
                # Convertimos el ID ingresado a entero.


                if eliminar_empleado(emp_id):
                    # Llamamos a database.py para eliminar
                    # el empleado de la base de datos.

                    print(
                        "[ÉXITO] Registro eliminado de la BD.\n"
                    )


                else:
                    # Si el ID no existe...

                    print(
                        "[ERROR] ID no existente.\n"
                    )


            except ValueError:
                # Si el usuario no escribe un número entero...

                print(
                    "[ERROR] Ingrese un ID de tipo entero.\n"
                )


        elif opcion == "5":
            # Opción 5: consultar el clima.


            print(
                "\n[API] Consultando servicio meteorológico..."
            )


            clima = obtener_clima_santiago()
            # Llamamos a services.py para obtener
            # los datos actuales del clima.


            if clima["exito"]:
                # Si la API respondió correctamente...

                print(
                    "\n--- CLIMA ACTUAL EN SANTIAGO ---"
                )


                print(
                    f"Temperatura: "
                    f"{clima['temperatura']} °C"
                )
                # Mostramos la temperatura.


                print(
                    f"Humedad: "
                    f"{clima['humedad']} %"
                )
                # Mostramos la humedad.


                print(
                    f"Estado del tiempo: "
                    f"{clima['estado']}"
                )
                # Mostramos el estado del clima.


                if clima["viento"] is not None:
                    # Comprobamos si existe información
                    # sobre el viento.

                    print(
                        f"Viento: "
                        f"{clima['viento']} km/h"
                    )


                print()


            else:
                # Si ocurrió un error con la API...

                print(
                    f"[API ERROR] "
                    f"{clima['mensaje']}\n"
                )


        elif opcion == "6":
            # Opción 6: consultar un indicador económico.


            print(
                "\n--- CONSULTA DE INDICADOR ECONÓMICO ---"
            )


            ind = input(
                "Moneda a consultar (dolar, euro, uf): "
            ).strip().lower()
            # Solicitamos la moneda.
            #
            # strip() elimina espacios.
            # lower() convierte a minúsculas.


            if not validar_moneda(ind):
                # Comprobamos si la moneda está permitida.

                print(
                    "[ERROR] Moneda no válida. "
                    "Ingrese dolar, euro o uf.\n"
                )

                continue


            res = obtener_indicador_economico(ind)
            # Llamamos a services.py para consultar
            # el valor de la moneda.


            if res["exito"]:
                # Si la consulta fue exitosa...

                print(
                    f"[API] 1 {res['moneda'].upper()} "
                    f"= ${res['valor']} "
                    f"({res['unidad']})\n"
                )
                # Mostramos el resultado.


            else:
                # Si hubo un problema...

                print(
                    f"[API ERROR] "
                    f"{res['mensaje']}\n"
                )


        elif opcion == "7":
            # Opción 7: salir del programa.


            print(
                "\nCerrando sesión en EcoTech Solutions. "
                "Hasta pronto."
            )


            break
            # break termina el while True
            # y por lo tanto cierra el menú.


        else:
            # Si el usuario escribe una opción
            # que no existe...

            print(
                "\n[OPCIÓN INVÁLIDA] "
                "Intente nuevamente.\n"
            )


if __name__ == "__main__":
    # Esta condición pregunta:
    # "¿Este archivo se está ejecutando directamente?"
    #
    # Si ejecutamos:
    # python main.py
    #
    # esta condición será True.


    inicializar_bd()
    # Primero se crea/inicializa la base de datos.


    if login():
        # Después se solicita iniciar sesión.
        #
        # Si el login devuelve True...

        menu_principal()
        # ...se muestra el menú principal.


    else:
        # Si login() devuelve False...

        print(
            "[ACCESO BLOQUEADO] "
            "Máximo de intentos alcanzado."
        )
        # Se bloquea el acceso porque se agotaron
        # los 3 intentos.