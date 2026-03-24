from entidades.binario import Binario
from entidades.octal import Octal
from entidades.decimal import DecimalSystem
from entidades.hexadecimal import Hexadecimal


SISTEMAS = {
    2: Binario,
    8: Octal,
    10: DecimalSystem,
    16: Hexadecimal,
}


def mostrar_menu_principal():
    print("""
Seleccione la acción que desea realizar:
1.- Realizar conversión entre sistemas (Binario/Octal/Decimal/Hexadecimal)
2.- Salir
""")
    try:
        return int(input("Opción: "))
    except ValueError:
        return 0


def solicitar_base(texto="Ingrese la base (2, 8, 10, 16): "):
    while True:
        try:
            b = int(input(texto))
            if b in (2, 8, 10, 16):
                return b
            print("Base no válida. Use 2, 8, 10 o 16.")
        except ValueError:
            print("Entrada no numérica. Intente de nuevo.")


def realizar_conversion():
    print("Seleccione la base de origen:")
    base_origen = solicitar_base()
    print("Seleccione la base de destino:")
    base_destino = solicitar_base()
    while base_destino == base_origen:
        print("La base de destino debe ser diferente a la de origen.")
        base_destino = solicitar_base()

    numero = input(f"Ingrese el número en base {base_origen}: ")
    ClaseOrigen = SISTEMAS[base_origen]
    ClaseDestino = SISTEMAS[base_destino]

    if not ClaseOrigen.validar(numero):
        print("Número inválido para la base seleccionada.")
        return

    valor_decimal = ClaseOrigen.to_decimal(numero)
    resultado = ClaseDestino.from_decimal(valor_decimal)

    print(f"\nResultado: {numero} (base {base_origen}) => {resultado} (base {base_destino})")
    print(f"Valor en decimal (aprox.): {valor_decimal}\n")


# Ejecución en nivel superior: bucle principal ejecutado "todo corrido"
while True:
    opcion = mostrar_menu_principal()
    if opcion == 1:
        realizar_conversion()
    elif opcion == 2:
        print("Saliendo...")
        break
    else:
        print("Opción no válida. Intente de nuevo.")
