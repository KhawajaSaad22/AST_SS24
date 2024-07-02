# test_robot_logic.py

import unittest
from unittest.mock import MagicMock
from robot_logic import MonitorBatteryAndCollision, RotateBase, StopMotion

class TestMonitorBatteryAndCollision(unittest.TestCase):
    def setUp(self):
        self.node = MagicMock()
        self.state = MonitorBatteryAndCollision(self.node)

    def test_initialization(self):
        self.assertEqual(self.state.battery_level, None)
        self.assertFalse(self.state.collision_detected)

    def test_collision_callback(self):
        msg = MagicMock()
        msg.ranges = [0.6, 0.4, 0.8]
        self.state.collision_callback(msg)
        self.assertTrue(self.state.collision_detected)
        
        msg.ranges = [0.6, 0.7, 0.8]
        self.state.collision_callback(msg)
        self.assertFalse(self.state.collision_detected)
        
    def test_execute_low_battery(self):
        userdata = {'battery_level': 49}
        self.state.battery_level = userdata['battery_level']
        outcome = self.state.execute(userdata)
        self.assertEqual(outcome, 'low_battery')

    def test_execute_collision(self):
        userdata = {'collision_detected': True}
        self.state.collision_detected = userdata['collision_detected']
        outcome = self.state.execute(userdata)
        self.assertEqual(outcome, 'collision')

    def test_execute_safe(self):
        userdata = {'battery_level': 80, 'collision_detected': False}
        self.state.battery_level = userdata['battery_level']
        self.state.collision_detected = userdata['collision_detected']
        outcome = self.state.execute(userdata)
        self.assertEqual(outcome, 'safe')


class TestRotateBase(unittest.TestCase):
    def setUp(self):
        self.node = MagicMock()
        self.state = RotateBase(self.node)

    def test_initialization(self):
        self.assertEqual(self.state.battery_threshold, 99.0)

    def test_execute_battery_ok(self):
        userdata = {'battery_level': 80}
        self.node.create_publisher().publish = MagicMock()
        outcome = self.state.execute(userdata)
        self.assertEqual(outcome, 'battery_ok')
        self.assertGreaterEqual(userdata['battery_level'], 99.0)


class TestStopMotion(unittest.TestCase):
    def setUp(self):
        self.node = MagicMock()
        self.node.get_parameter.return_value.get_parameter_value.return_value.bool_value = False
        self.state = StopMotion(self.node)

    def test_initialization(self):
        self.assertEqual(self.state.battery_threshold, 50.0)

    def test_execute_manual_reset(self):
        userdata = {'battery_level': 80, 'collision_detected': True}
        self.node.get_parameter().get_parameter_value().bool_value = True
        outcome = self.state.execute(userdata)
        self.assertEqual(outcome, 'manual_reset')

    def test_execute_low_battery(self):
        userdata = {'battery_level': 45, 'collision_detected': True}
        outcome = self.state.execute(userdata)
        self.assertEqual(outcome, 'low_battery')

if __name__ == '__main__':
    unittest.main()
