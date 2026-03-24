class Binario:
	"""Clase para validar y convertir números en base 2 (soporta parte fraccionaria)."""
	base = 2

	@staticmethod
	def validar(numero: str) -> bool:
		"""Verifica que la cadena represente un número binario válido (puede tener un solo punto decimal)."""
		if not isinstance(numero, str):
			return False
		if numero.count('.') > 1:
			return False
		if numero.startswith('-'):
			numero = numero[1:]
		partes = numero.split('.')
		for parte in partes:
			if parte == '':
				continue
			for ch in parte:
				if ch not in ('0', '1'):
					return False
		return True

	@staticmethod
	def to_decimal(numero: str) -> float:
		"""Convierte un número binario (como cadena) a su valor decimal (float)."""
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
			potencia *= 2
		if len(partes) > 1 and partes[1] != '':
			frac = partes[1]
			potencia = 2
			for ch in frac:
				valor += int(ch) / potencia
				potencia *= 2
		return -valor if neg else valor

	@staticmethod
	def from_decimal(valor_decimal: float, precision: int = 12) -> str:
		"""Convierte un número decimal (float) a su representación binaria con la precisión dada para la fracción."""
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
			partes_ent = []
			n = entero
			while n > 0:
				partes_ent.append(str(n % 2))
				n //= 2
			entero_str = ''.join(reversed(partes_ent))
		# parte fraccionaria
		if frac == 0:
			resultado = entero_str
		else:
			partes_frac = []
			f = frac
			for _ in range(max(1, precision)):
				f *= 2
				d = int(f)
				partes_frac.append(str(d))
				f -= d
				if f == 0:
					break
			resultado = entero_str + '.' + ''.join(partes_frac)
		return ('-' + resultado) if neg else resultado

