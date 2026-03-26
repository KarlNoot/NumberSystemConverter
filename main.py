from fractions import Fraction

DIGITOS = "0123456789ABCDEF"
NOMBRES = {
    2: "Binario",
    8: "Octal",
    10: "Decimal",
    16: "Hexadecimal",
}


def valor_digito(caracter):
    return DIGITOS.index(caracter)


def digito_valor(valor):
    return DIGITOS[valor]


def solicitar_base(texto="Ingrese la base (2, 8, 10, 16): "):
    while True:
        try:
            base = int(input(texto))
            if base in NOMBRES:
                return base
            print("Base no válida. Use 2, 8, 10 o 16.")
        except ValueError:
            print("Entrada no numérica. Intente de nuevo.")


def validar_numero(numero, base):
    numero = numero.strip().upper()

    if not numero:
        return False

    if numero[0] in "+-":
        numero = numero[1:]

    if not numero or numero.count(".") > 1:
        return False

    partes = numero.split(".")
    if len(partes) == 2 and partes[0] == "" and partes[1] == "":
        return False

    permitidos = set(DIGITOS[:base])

    for parte in partes:
        if parte and any(ch not in permitidos for ch in parte):
            return False

    return any(parte != "" for parte in partes)


def numero_a_fraccion(numero, base):
    numero = numero.strip().upper()
    signo = -1 if numero.startswith("-") else 1

    if numero[0] in "+-":
        numero = numero[1:]

    if "." in numero:
        parte_entera, parte_fraccionaria = numero.split(".")
    else:
        parte_entera, parte_fraccionaria = numero, ""

    total = Fraction(0, 1)

    for posicion, digito in enumerate(reversed(parte_entera)):
        if digito:
            total += Fraction(valor_digito(digito) * (base ** posicion), 1)

    for posicion, digito in enumerate(parte_fraccionaria, start=1):
        total += Fraction(valor_digito(digito), base ** posicion)

    return signo * total


def fraccion_a_decimal_str(valor):
    if valor == 0:
        return "0"

    signo = "-" if valor < 0 else ""
    valor = abs(valor)

    entero = valor.numerator // valor.denominator
    resto = valor.numerator % valor.denominator

    if resto == 0:
        return signo + str(entero)

    decimales = []
    vistos = set()

    while resto != 0 and resto not in vistos:
        vistos.add(resto)
        resto *= 10
        decimales.append(str(resto // valor.denominator))
        resto %= valor.denominator

    resultado = "".join(decimales).rstrip("0")
    if not resultado:
        return signo + str(entero)

    return signo + f"{entero}.{resultado}"


def fraccion_a_base(valor, base_destino, max_decimales=12):
    if base_destino == 10:
        return fraccion_a_decimal_str(valor)

    if valor == 0:
        return "0"

    signo = "-" if valor < 0 else ""
    valor = abs(valor)

    parte_entera = valor.numerator // valor.denominator
    parte_fraccionaria = valor - parte_entera

    if parte_entera == 0:
        enteros = ["0"]
    else:
        enteros = []
        while parte_entera > 0:
            parte_entera, residuo = divmod(parte_entera, base_destino)
            enteros.append(digito_valor(residuo))
        enteros.reverse()

    fraccionarios = []
    contador = 0
    while parte_fraccionaria != 0 and contador < max_decimales:
        parte_fraccionaria *= base_destino
        digito = parte_fraccionaria.numerator // parte_fraccionaria.denominator
        fraccionarios.append(digito_valor(digito))
        parte_fraccionaria -= digito
        contador += 1

    if fraccionarios:
        return signo + "".join(enteros) + "." + "".join(fraccionarios)

    return signo + "".join(enteros)


def mostrar_descomposicion_numero(numero, base):
    numero_original = numero.strip().upper()
    negativo = numero_original.startswith("-")

    if numero_original and numero_original[0] in "+-":
        numero_limpio = numero_original[1:]
    else:
        numero_limpio = numero_original

    if "." in numero_limpio:
        parte_entera, parte_fraccionaria = numero_limpio.split(".")
    else:
        parte_entera, parte_fraccionaria = numero_limpio, ""

    total = Fraction(0, 1)

    print(f"\nDESCOMPOSICIÓN DE {numero_original} EN BASE {base} HACIA DECIMAL")
    print("-" * 95)
    print(f"{'Posición':<12}{'Dígito':<10}{'Potencia':<15}{'Ponderación':<18}{'Cálculo':<20}{'Aporte':<15}")
    print("-" * 95)

    for posicion, digito in enumerate(reversed(parte_entera)):
        valor = valor_digito(digito)
        ponderacion = Fraction(base ** posicion, 1)
        aporte = valor * ponderacion
        total += aporte

        print(
            f"{posicion:<12}{digito:<10}{(str(base) + '^' + str(posicion)):<15}"
            f"{fraccion_a_decimal_str(ponderacion):<18}"
            f"{(str(valor) + ' x ' + fraccion_a_decimal_str(ponderacion)):<20}"
            f"{fraccion_a_decimal_str(aporte):<15}"
        )

    for i, digito in enumerate(parte_fraccionaria, start=1):
        valor = valor_digito(digito)
        ponderacion = Fraction(1, base ** i)
        aporte = valor * ponderacion
        total += aporte

        print(
            f"{-i:<12}{digito:<10}{(str(base) + '^-' + str(i)):<15}"
            f"{fraccion_a_decimal_str(ponderacion):<18}"
            f"{(str(valor) + ' x ' + fraccion_a_decimal_str(ponderacion)):<20}"
            f"{fraccion_a_decimal_str(aporte):<15}"
        )

    if negativo:
        total = -total
        print("-" * 95)
        print("Signo negativo aplicado al resultado total.")

    print("-" * 95)
    print(f"TOTAL DECIMAL: {fraccion_a_decimal_str(total)}")
    print("-" * 95)


def mostrar_menu_principal():
    print("""
Seleccione la acción que desea realizar:
1.- Realizar conversión entre sistemas
2.- Salir
""")
    try:
        return int(input("Opción: "))
    except ValueError:
        return 0


def realizar_conversion():
    print("\nSistemas disponibles:")
    print("2  -> Binario")
    print("8  -> Octal")
    print("10 -> Decimal")
    print("16 -> Hexadecimal")

    base_origen = solicitar_base("\nSeleccione la base de origen: ")
    base_destino = solicitar_base("Seleccione la base de destino: ")

    while base_destino == base_origen:
        print("La base de destino debe ser diferente a la base de origen.")
        base_destino = solicitar_base("Seleccione la base de destino: ")

    numero = input(f"Ingrese el número en {NOMBRES[base_origen]}: ").strip()

    if not validar_numero(numero, base_origen):
        print("Número inválido para la base seleccionada.")
        return

    valor_decimal_fraccion = numero_a_fraccion(numero, base_origen)
    resultado = fraccion_a_base(valor_decimal_fraccion, base_destino, max_decimales=12)

    print("\n" + "=" * 70)
    print(f"Conversión: {numero} (base {base_origen}) -> {resultado} (base {base_destino})")
    print(f"Valor decimal: {fraccion_a_decimal_str(valor_decimal_fraccion)}")
    print("=" * 70)

    if base_origen in (2, 8, 16):
        mostrar_descomposicion_numero(numero, base_origen)


if __name__ == "__main__":
    while True:
        opcion = mostrar_menu_principal()

        if opcion == 1:
            realizar_conversion()
        elif opcion == 2:
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
