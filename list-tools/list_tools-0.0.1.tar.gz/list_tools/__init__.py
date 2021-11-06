def chunk(seq, size):
	def is_iterable(obj):
		try:
			iter(obj)
		except Exception:
			return False
		else:
			return True

	if not is_iterable(seq):
		raise TypeError("Passed sequence is not iterable")
	return (seq[pos:pos + size] for pos in range(0, len(seq), size))
