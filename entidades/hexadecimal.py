class Hexadecimal:
	"""Clase para validar y convertir números en base 16 (soporta parte fraccionaria)."""
	base = 16

	@staticmethod
	def validar(numero: str) -> bool:
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
		ch = ch.upper()
		if ch.isdigit():
			return int(ch)
		return ord(ch) - ord('A') + 10

	@staticmethod
	def to_decimal(numero: str) -> float:
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
			valor += Hexadecimal._valor_digito(ch) * potencia
			potencia *= 16
		if len(partes) > 1 and partes[1] != '':
			frac = partes[1]
			potencia = 16
			for ch in frac:
				valor += Hexadecimal._valor_digito(ch) / potencia
				potencia *= 16
		return -valor if neg else valor

	@staticmethod
	def from_decimal(valor_decimal: float, precision: int = 12) -> str:
		if not isinstance(valor_decimal, (int, float)):
			raise ValueError('Se requiere un número')
		neg = valor_decimal < 0
		if neg:
			valor_decimal = -valor_decimal
		entero = int(valor_decimal)
		frac = valor_decimal - entero
		# parte entera
		if entero == 0:
			entero_str = '0'
		else:
			digs = []
			n = entero
			while n > 0:
				d = n % 16
				if d < 10:
					digs.append(str(d))
				else:
					digs.append(chr(ord('A') + d - 10))
				n //= 16
			entero_str = ''.join(reversed(digs))
		# parte fraccionaria
		if frac == 0:
			res = entero_str
		else:
			digs = []
			f = frac
			for _ in range(precision):
				f *= 16
				d = int(f)
				if d < 10:
					digs.append(str(d))
				else:
					digs.append(chr(ord('A') + d - 10))
				f -= d
				if f == 0:
					break
			res = entero_str + '.' + ''.join(digs)
		return ('-' + res) if neg else res

