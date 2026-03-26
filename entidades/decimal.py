class DecimalSystem:
    """Clase para validar y convertir números en base 10 (soporta parte fraccionaria)."""
    base = 10

    @staticmethod
    def validar(numero: str) -> bool:
        """
        Verifica que la cadena represente un número decimal válido.
        Solo dígitos, un punto opcional y signo al inicio.
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
            if not all(ch.isdigit() for ch in parte):
                return False
        return True

    @staticmethod
    def to_decimal(numero: str) -> float:
        """Convierte la cadena decimal a float. Lanza ValueError si no es válida."""
        if not DecimalSystem.validar(numero):
            raise ValueError('Número decimal inválido')
        return float(numero)

    @staticmethod
    def from_decimal(valor_decimal: float, precision: int = 12) -> str:
        """
        Devuelve la representación decimal como cadena.
        Se recortan ceros innecesarios en la parte fraccionaria.
        """
        if not isinstance(valor_decimal, (int, float)):
            raise ValueError('Se requiere un número')
        s = f"{round(valor_decimal, precision)}"
        if '.' in s:
            s = s.rstrip('0').rstrip('.')
        return s