import unittest
from Steep import steep

class TestScriptManager(unittest.TestCase):
	def setUp(self):
		self.scriptManager = steep.ScriptManager()

	def test_set(self):
		self.scriptManager.set(1, "abcdef", "Script", "script value")
		self.assertIn(1, self.scriptManager)
		self.assertEquals(self.scriptManager[1], ("abcdef", "Script", "script value"))
	
	def test_length(self):
		self.assertEquals(len(self.scriptManager), 0)
		self.scriptManager.set(0, "abcdef", "Script", "script value")
		self.assertEquals(len(self.scriptManager), 1)
		self.scriptManager.set(1, "t", "t", "t")
		self.assertEquals(len(self.scriptManager), 2)
		self.scriptManager.set(1, "bdafgd", "Name", "")
		self.assertEquals(len(self.scriptManager), 2)
	
	def test_iterate(self):
		self.scriptManager.set(0, "abcdef", "Script", "script value")
		self.scriptManager.set(1, "t", "t", "t")
		self.scriptManager.set(2, "bdafgd", "Name", "")
		n = 0
		iterator = iter(self.scriptManager)
		self.assertIs(iterator, iter(iterator))
		for i in iterator:
			self.assertIn(i, self.scriptManager)
			n += 1
		self.assertEquals(n, len(self.scriptManager))
	
	def test_delete(self):
		self.scriptManager.set(0, "abcdef", "Script", "script value")
		self.scriptManager.set(1, "t", "t", "t")
		self.scriptManager.set(2, "bdafgd", "Name", "")
		self.assertIn(0, self.scriptManager)
		self.assertIn(1, self.scriptManager)
		self.assertIn(2, self.scriptManager)
		del(self.scriptManager[0])
		del(self.scriptManager[2])
		self.assertNotIn(0, self.scriptManager)
		self.assertNotIn(2, self.scriptManager)
		self.assertIn(1, self.scriptManager)
	
	def test_clear(self):
		self.scriptManager.set(0, "abcdef", "Script", "script value")
		self.scriptManager.set(1, "t", "t", "t")
		self.scriptManager.set(2, "bdafgd", "Name", "")
		self.assertIn(0, self.scriptManager)
		self.assertIn(1, self.scriptManager)
		self.assertIn(2, self.scriptManager)
		self.scriptManager.clear()
		self.assertNotIn(0, self.scriptManager)
		self.assertNotIn(1, self.scriptManager)
		self.assertNotIn(2, self.scriptManager)
	
	def test_tid(self):
		self.scriptManager.set(0, "abcdef", "Script", "script value")
		self.scriptManager.set(1, "t", "t", "t")
		self.scriptManager.set(2, "bdafgd", "Name", "")
		self.assertTrue(self.scriptManager.contains_tid("abcdef"))
		self.assertTrue(self.scriptManager.contains_tid("t"))
		self.assertTrue(self.scriptManager.contains_tid("bdafgd"))
		self.assertEquals(self.scriptManager.get_tid("abcdef"), 0)
		self.assertEquals(self.scriptManager.get_tid("t"), 1)
		self.assertEquals(self.scriptManager.get_tid("bdafgd"), 2)
		self.assertIsNone(self.scriptManager.get_tid("foo"))
		del(self.scriptManager[self.scriptManager.get_tid("abcdef")])
		self.scriptManager.set(3, "bar", "script", "script")
		self.assertFalse(self.scriptManager.contains_tid("abcdef"))
		self.assertTrue(self.scriptManager.contains_tid("bar"))
