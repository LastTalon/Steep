import sublime
import unittest
import threading
import time
from Steep import steep

class TestApplicationCommands(unittest.TestCase):
	def setUp(self):
		settings = sublime.load_settings("Preferences.sublime-settings")
		settings.set("close_windows_when_empty", False)
	
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
		dummy_finalize = steep.SteepFinalizeDisconnectCommand()
		dummy_disconnect = steep.SteepDisconnectCommand()
		dummy_connect = steep.SteepConnectCommand()
		
		self.assertFalse(dummy_finalize.is_visible())
		
		sublime.run_command("steep_connect")
		
		steep._disconnect = 1
		steep._connection[0].exit_thread()
		steep._connection[1].exit_thread()
		steep._scripts.clear()
		sublime.run_command("steep_finalize_disconnect")
		
		self.assertIsNone(steep._connection)
		self.assertIsNone(steep._disconnect)
		self.assertFalse(dummy_disconnect.is_enabled())
		self.assertTrue(dummy_connect.is_enabled())
		self.assertIsNotNone(steep._scripts)
		self.assertIsInstance(steep._scripts, steep.ScriptManager)
		
		sublime.run_command("steep_connect")
		
		self.assertIsNotNone(steep._connection)
		self.assertIsNotNone(steep._scripts)
		self.assertIsNone(steep._disconnect)
		self.assertTrue(dummy_disconnect.is_enabled())
		self.assertFalse(dummy_connect.is_enabled())
		
		sublime.run_command("steep_disconnect")
		steep._disconnect.cancel_finalize()
		
		self.assertFalse(dummy_disconnect.is_enabled())
		self.assertFalse(dummy_connect.is_enabled())
		
		sublime.run_command("steep_finalize_disconnect")
		steep._scripts.clear()
