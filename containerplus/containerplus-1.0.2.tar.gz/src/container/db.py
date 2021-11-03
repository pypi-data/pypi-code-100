import pickle

class KeyValueDB:
  def __init__(self, name: str, autoload=False, autosave=True):
    self.name = name
    self.load()
    self.autoload = autoload
    self.autosave = autosave

  def load(self):
    try:
      self.data = pickle.load(open(self.name + ".db", "rb"))
    except:
      self.data = {}
      pickle.dump(self.data, open(self.name + ".db", "wb"))

  def save(self, sort=True):
    if sort and isinstance(self.data, dict):
      self.data = {item:self.data[item] for item in sorted(self.data, key=str.lower)}
    pickle.dump(self.data, open(self.name + ".db", "wb"))

  def __repr__(self):
    if self.autoload:
      self.load()
    return str(self.data)

  def __getitem__(self, key):
    if self.autoload:
      self.load()
    return self.data[key]

  def __setitem__(self, key, value):
    self.data[key] = value
    if self.autosave:
      self.save()

  def __delitem__(self, key):
    del self.data[key]
    if self.autosave:
      self.save()

  