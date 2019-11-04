import unittest
import os
import pymel.core as pm

if __name__ == '__main__':
	# Set the testing environment for Maya
	rootPath = os.getcwd()
	mayaEnvDir = os.path.join(rootPath, "__test_environment")
	os.environ["MAYA_APP_DIR"] = mayaEnvDir

	# Initialize Maya
	import maya.standalone
	maya.standalone.initialize('python')

	# Set current project to the test directory
	projectDir = os.path.join(mayaEnvDir, "projects\\default")
	pm.Workspace().open(projectDir)

	# Find all tests in and under current directory
	root = os.path.dirname(__file__)
	pattern = '*_test.py'

	loader = unittest.TestLoader().discover(root, pattern=pattern)
	suite = unittest.TestSuite()

	if loader.countTestCases():
		suite.addTests(loader)

	runner = unittest.TextTestRunner(verbosity=3)
	runner.run(suite)

	# Uninitialize Maya
	maya.standalone.uninitialize()
