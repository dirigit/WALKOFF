import importlib
import unittest

import walkoff.config.paths
import tests.config
from walkoff import initialize_databases
import walkoff.appgateway
from walkoff.appgateway import appinstance
from tests.config import test_apps_path


class TestInstance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        walkoff.config.paths.db_path = tests.config.test_db_path
        walkoff.config.paths.case_db_path = tests.config.test_case_db_path
        walkoff.config.paths.device_db_path = tests.config.test_device_db_path
        initialize_databases()
        walkoff.appgateway.cache_apps(test_apps_path)

    @classmethod
    def tearDownClass(cls):
        walkoff.appgateway.clear_cache()

    def test_create_instance(self):
        # extra janky way to import this because we still need a more predictable and consistent way to import modules
        hello_world_main = importlib.import_module('tests.testapps.HelloWorld.main')
        hello_world_main_class = getattr(hello_world_main, 'Main')
        inst = appinstance.AppInstance.create("HelloWorld", "testDevice")
        self.assertIsInstance(inst, appinstance.AppInstance)
        self.assertIsInstance(inst.instance, hello_world_main_class)
        self.assertEqual(inst.state, appinstance.OK)

    def test_create_invalid_app_name(self):
        instance = appinstance.AppInstance.create("InvalidAppName", "testDevice")
        self.assertIsNone(instance.instance)
        self.assertEqual(instance.state, appinstance.OK)

    def test_call(self):
        inst = appinstance.AppInstance.create("HelloWorld", "testDevice")
        created_app = inst()
        hello_world_main = importlib.import_module('tests.testapps.HelloWorld.main')
        hello_world_main_class = getattr(hello_world_main, 'Main')
        self.assertIsInstance(created_app, hello_world_main_class)

    def test_shutdown(self):
        inst = appinstance.AppInstance.create("HelloWorld", "testDevice")
        self.assertEqual(inst.state, appinstance.OK)
        inst.shutdown()
        self.assertEqual(inst.state, appinstance.SHUTDOWN)
