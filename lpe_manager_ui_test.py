import unittest
import os
import pymel.core as pm
from lpe_manager_ui import LPEManagerUI
from lpe_manager import LPEManager

# Test scene has 2 lights:
# warmLightShape
# coldLightShape
TEST_SCENE_PATH = "General\\scripts\\lpe_manager\\test_scene.mb"


def openMayaFile(sceneName):
	pm.system.openFile(sceneName, force=True)


class LPEManagerUITest(unittest.TestCase):
	"""LPEManagerUI Test class"""
	pass
	# def setUp(self):
	# 	dirPath = os.getcwd()
	# 	filePath = os.path.join(dirPath, TEST_SCENE_PATH)
	# 	openMayaFile(filePath)

	# 	self.ui = LPEManagerUI()

	# def test_creates_itself(self):
	# 	self.assertTrue(type(self.ui) is LPEManagerUI)

	# def test_composes_a_manager(self):
	# 	self.assertTrue(type(self.ui._manager) is LPEManager)
