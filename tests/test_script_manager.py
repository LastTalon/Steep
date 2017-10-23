import unittest
from Steep import steep

class TestScriptManager(unittest.TestCase):
	def setUp(self):
		self.scriptManager = steep.ScriptManager()
		self.scriptManager.set(0, "a", "Script 0", "script value")
		self.scriptManager.set(1, "b", "Script 1", "script value")
		self.scriptManager.set(200, "c", "Script 2", "script value")
		self.scriptManager.set(4, "abcd", "", "script value")
		self.scriptManager.set(2, "qwert", "12345", "script value")
		self.scriptManager.set(-3, "", "", "script value")
		self.scriptManager.set(111111, "0", "n", "script value")

	def test_set(self):
		self.scriptManager.set(1, "abcdef", "Script", "script value")
		self.assertIn(1, self.scriptManager)
		self.assertEquals(self.scriptManager[1], ("abcdef", "Script", "script value"))
	
	def test_length(self):
		self.assertEquals(len(self.scriptManager), 7)
		self.scriptManager.set(10, "abcdef", "Script", "script value")
		self.assertEquals(len(self.scriptManager), 8)
		self.scriptManager.set(10, "t", "t", "t")
		self.assertEquals(len(self.scriptManager), 8)
	
	def test_get(self):
		self.assertEquals(self.scriptManager[0], ("a", "Script 0", "script value"))
		self.assertEquals(self.scriptManager[1], ("b", "Script 1", "script value"))
		self.assertEquals(self.scriptManager[200], ("c", "Script 2", "script value"))
		self.assertEquals(self.scriptManager[4], ("abcd", "", "script value"))
		self.assertEquals(self.scriptManager[2], ("qwert", "12345", "script value"))
		self.assertEquals(self.scriptManager[-3], ("", "", "script value"))
		self.assertEquals(self.scriptManager[111111], ("0", "n", "script value"))
		self.scriptManager.set(1, "a", "a", "a")
		self.assertEquals(self.scriptManager[0], ("a", "Script 0", "script value"))
		self.assertEquals(self.scriptManager[1], ("a", "a", "a"))
		self.assertEquals(self.scriptManager[200], ("c", "Script 2", "script value"))
		self.assertEquals(self.scriptManager[4], ("abcd", "", "script value"))
		self.assertEquals(self.scriptManager[2], ("qwert", "12345", "script value"))
		self.assertEquals(self.scriptManager[-3], ("", "", "script value"))
		self.assertEquals(self.scriptManager[111111], ("0", "n", "script value"))
		self.scriptManager.set(11, "b", "b", "b")
		self.assertEquals(self.scriptManager[0], ("a", "Script 0", "script value"))
		self.assertEquals(self.scriptManager[1], ("a", "a", "a"))
		self.assertEquals(self.scriptManager[200], ("c", "Script 2", "script value"))
		self.assertEquals(self.scriptManager[4], ("abcd", "", "script value"))
		self.assertEquals(self.scriptManager[2], ("qwert", "12345", "script value"))
		self.assertEquals(self.scriptManager[-3], ("", "", "script value"))
		self.assertEquals(self.scriptManager[111111], ("0", "n", "script value"))
		self.assertEquals(self.scriptManager[11], ("b", "b", "b"))
	
	def test_iterate(self):
		n = 0
		for i in self.scriptManager:
			self.assertIn(i, self.scriptManager)
			n += 1
		self.assertEquals(n, len(self.scriptManager))
	
	def test_contains(self):
		self.assertIn(0, self.scriptManager)
		self.assertIn(1, self.scriptManager)
		self.assertIn(200, self.scriptManager)
		self.assertIn(4, self.scriptManager)
		self.assertIn(2, self.scriptManager)
		self.assertIn(-3, self.scriptManager)
		self.assertIn(111111, self.scriptManager)
		self.assertNotIn(10, self.scriptManager)
		self.scriptManager.set(1, "a", "a", "a")
		self.scriptManager.set(10, "b", "b", "b")
		self.assertIn(1, self.scriptManager)
		self.assertIn(10, self.scriptManager)
	
	def test_delete(self):
		self.assertIn(0, self.scriptManager)
		self.assertIn(1, self.scriptManager)
		self.assertIn(200, self.scriptManager)
		self.assertIn(4, self.scriptManager)
		self.assertIn(2, self.scriptManager)
		self.assertIn(-3, self.scriptManager)
		self.assertIn(111111, self.scriptManager)
		del(self.scriptManager[0])
		del(self.scriptManager[111111])
		self.assertNotIn(0, self.scriptManager)
		self.assertNotIn(111111, self.scriptManager)
	
	def test_clear(self):
		self.assertIn(0, self.scriptManager)
		self.assertIn(1, self.scriptManager)
		self.assertIn(200, self.scriptManager)
		self.assertIn(4, self.scriptManager)
		self.assertIn(2, self.scriptManager)
		self.assertIn(-3, self.scriptManager)
		self.assertIn(111111, self.scriptManager)
		self.scriptManager.clear()
		self.assertNotIn(0, self.scriptManager)
		self.assertNotIn(1, self.scriptManager)
		self.assertNotIn(200, self.scriptManager)
		self.assertNotIn(4, self.scriptManager)
		self.assertNotIn(2, self.scriptManager)
		self.assertNotIn(-3, self.scriptManager)
		self.assertNotIn(111111, self.scriptManager)
	
	def test_tid(self):
		self.assertTrue(self.scriptManager.contains_tid("a"))
		self.assertTrue(self.scriptManager.contains_tid("b"))
		self.assertTrue(self.scriptManager.contains_tid("abcd"))
		self.assertTrue(self.scriptManager.contains_tid("qwert"))
		self.assertFalse(self.scriptManager.contains_tid("foo"))
		self.assertFalse(self.scriptManager.contains_tid("bar"))
		self.assertEquals(self.scriptManager.get_tid("a"), 0)
		self.assertEquals(self.scriptManager.get_tid("b"), 1)
		self.assertEquals(self.scriptManager.get_tid("abcd"), 4)
		self.assertEquals(self.scriptManager.get_tid("qwert"), 2)
		self.assertIsNone(self.scriptManager.get_tid("foo"))
		self.assertIsNone(self.scriptManager.get_tid("bar"))
		del(self.scriptManager[self.scriptManager.get_tid("c")])
		self.scriptManager.set(300, "bar", "script", "script")
		self.assertFalse(self.scriptManager.contains_tid("c"))
		self.assertTrue(self.scriptManager.contains_tid("bar"))
	
	def test_iterator(self):
		iterator = iter(self.scriptManager)
		self.assertIs(iterator, iter(iterator))
		for i in iterator:
			self.assertIn(i, self.scriptManager)
