def list_items(item):
	"""
	Creates a gramatically correct string from an item.

	Parameters:
	item -- the item that provides the element(s) for string construction

	Examples:
	>>> list_items(["apples", "oranges", "bananas"])
	"'apples', 'oranges', or 'bananas'"
	"""
	if isinstance(item, (list, tuple)):
		if len(item) == 1:
			return f"'{item[0]}'"
		elif len(item) == 2:
			return f"'{item[0]}' or '{item[1]}'"
		else:
			listed = ", ".join(f"'{e}'" for e in item[0:-1])
			return f"{listed}, or '{item[-1]}'"
	else:
		return f"'{item}'"
