from threading import RLock

class ScriptManager:
	def __init__(self):
		self._scripts = dict()
		self._lock = RLock()
	
	def __len__(self):
		with self._lock:
			return len(self._scripts)
	
	def __getitem__(self, key):
		with self._lock:
			return self._scripts[key]
	
	def __delitem__(self, key):
		with self._lock:
			del self._scripts[key]
	
	def __iter__(self):
		with self._lock:
			return ScriptManagerIterator(self)
	
	def __contains__(self, item):
		with self._lock:
			return item in self._scripts
	
	def clear(self):
		with self._lock:
			self._scripts.clear()
	
	def set(self, id, tid, name, value):
		with self._lock:
			self._scripts[id] = (tid, name, value)
	
	def contains_tid(self, tid):
		return self.get_tid(tid) != None
	
	def get_tid(self, tid):
		with self._lock:
			for i, v in self._scripts.items():
				if v[0] == tid:
					return i
			return None

class ScriptManagerIterator:
	def __init__(self, manager):
		self._keys = list(manager._scripts.keys())
		self._index = 0
	
	def __iter__(self):
		return self
	
	def __next__(self):
		if self._index >= len(self._keys):
			raise StopIteration
		value = self._keys[self._index]
		self._index += 1
		return value
