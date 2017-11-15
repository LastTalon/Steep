import sublime
import unittest
from Steep import steep

class TestApplicationCommands(unittest.TestCase):
	def setUp(self):
		self.view = sublime.active_window().new_file()
		settings = sublime.load_settings("Preferences.sublime-settings")
		settings.set("close_windows_when_empty", False)
	
	def tearDown(self):
		if self.view:
			self.view.set_scratch(True)
			self.view.window().focus_view(self.view)
			self.view.window().run_command("close_file")
	
	def test_connect(self):
		dummy = steep.SteepConnectCommand()
		
		self.assertIsNone(steep._connection)
		self.assertIsNotNone(steep._scripts)
		self.assertIsInstance(steep._scripts, steep.ScriptManager)
		self.assertIsNone(steep._disconnect)
		self.assertTrue(dummy.is_enabled())
		
		sublime.run_command("steep_connect")
		
		self.assertIsNotNone(steep._connection)
		self.assertIsInstance(steep._connection, tuple)
		self.assertEqual(len(steep._connection), 3)
		self.assertIsInstance(steep._connection[0], steep.Server)
		self.assertIsInstance(steep._connection[1], steep.Client)
		self.assertIsInstance(steep._connection[2], sublime.Window)
		self.assertIsNotNone(steep._scripts)
		self.assertIsInstance(steep._scripts, steep.ScriptManager)
		self.assertIsNone(steep._disconnect)
		self.assertFalse(dummy.is_enabled())
		
		steep._connection[0].exit_thread()
		steep._connection[1].exit_thread()
		steep._connection[2].run_command("close_window")
		steep._connection = None
		steep._scripts.clear()
		steep._disconnect = None
		
		self.assertTrue(dummy.is_enabled())
	
	def test_disconnect(self):
		pass
	
	def test_finalize_disconnect(self):
		pass
