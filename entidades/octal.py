class Octal:
    """Clase para validar y convertir números en base 8 (soporta parte fraccionaria)."""
    base = 8

    @staticmethod
    def validar(numero: str) -> bool:
        """
        Verifica que la cadena represente un número octal válido.
        Solo dígitos 0-7, un punto y signo opcional.
        """
        if not isinstance(numero, str):
            return False
        s = numero.strip()
        if s == '':
            return False
        if s.count('.') > 1:
            return False
        if s.startswith('-'):
            s = s[1:]
        partes = s.split('.')
        for parte in partes:
            if parte == '':
                continue
            for ch in parte:
                if ch < '0' or ch > '7':
                    return False
        return True

    @staticmethod
    def to_decimal(numero: str) -> float:
        """Convierte un número octal (cadena) a su valor decimal (float)."""
        neg = False
        s = numero.strip()
        if s.startswith('-'):
            neg = True
            s = s[1:]
        if s == '' or s == '.':
            raise ValueError('Número inválido')

        partes = s.split('.')
        entero = partes[0] if partes[0] != '' else '0'

        valor = 0
        potencia = 1
        for ch in entero[::-1]:
            valor += int(ch) * potencia
            potencia *= 8

        if len(partes) > 1 and partes[1] != '':
            frac = partes[1]
            potencia = 8
            for ch in frac:
                valor += int(ch) / potencia
                potencia *= 8

        return -valor if neg else valor

    @staticmethod
    def from_decimal(valor_decimal: float, precision: int = 12) -> str:
        """Convierte un decimal a octal con la precisión dada para la parte fraccionaria."""
        if not isinstance(valor_decimal, (int, float)):
            raise ValueError('Se requiere un número')

        neg = valor_decimal < 0
        if neg:
            valor_decimal = -valor_decimal

        entero = int(valor_decimal)
        frac = valor_decimal - entero

        # Parte entera
        if entero == 0:
            entero_str = '0'
        else:
            digs = []
            n = entero
            while n > 0:
                digs.append(str(n % 8))
                n //= 8
            entero_str = ''.join(reversed(digs))

        # Parte fraccionaria
        if frac == 0:
            res = entero_str
        else:
            digs = []
            f = frac
            for _ in range(precision):
                f *= 8
                d = int(f)
                digs.append(str(d))
                f -= d
                if f == 0:
                    break
            res = entero_str + '.' + ''.join(digs)

        return ('-' + res) if neg else res
