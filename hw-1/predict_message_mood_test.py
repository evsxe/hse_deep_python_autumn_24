import unittest
from unittest import mock

from predict_message_mood import predict_message_mood, SomeModel


class TestPredictMessageMood(unittest.TestCase):
    def setUp(self):
        self.model = SomeModel()
        self.text = 'test'
