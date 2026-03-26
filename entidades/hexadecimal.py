class Hexadecimal:
    """Clase para validar y convertir números en base 16 (soporta parte fraccionaria)."""
    base = 16

    @staticmethod
    def validar(numero: str) -> bool:
        """
        Verifica que la cadena represente un número hexadecimal válido.
        Acepta dígitos 0-9, letras A-F (mayúsculas o minúsculas), un punto y signo.
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
                ch = ch.upper()
                if not (ch.isdigit() or ('A' <= ch <= 'F')):
                    return False
        return True

    @staticmethod
    def _valor_digito(ch: str) -> int:
        """Convierte un carácter hexadecimal a su valor entero (0-15)."""
        ch = ch.upper()
        if ch.isdigit():
            return int(ch)
        return ord(ch) - ord('A') + 10

    @staticmethod
    def to_decimal(numero: str) -> float:
        """Convierte un número hexadecimal (cadena) a su valor decimal (float)."""
        neg = False
        s = numero.strip()
        if s.startswith('-'):
            neg = True
            s = s[1:]
        if s == '' or s == '.':
            raise ValueError('Número inválido')

        partes = s.split('.')
        entero = partes[0] if partes[0] != '' else '0'

        # Parte entera
        valor = 0
        potencia = 1
        for ch in entero[::-1]:
            valor += Hexadecimal._valor_digito(ch) * potencia
            potencia *= 16

        # Parte fraccionaria
        if len(partes) > 1 and partes[1] != '':
            frac = partes[1]
            potencia = 16
            for ch in frac:
                valor += Hexadecimal._valor_digito(ch) / potencia
                potencia *= 16

        return -valor if neg else valor