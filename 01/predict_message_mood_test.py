import unittest

from unittest.mock import patch

from predict_message_mood import predict_message_mood, SomeModel


class TestPredictMessageMood(unittest.TestCase):

    def setUp(self):
        self.model = SomeModel()
        self.text = 'test'

    def test_message_type_error(self):
        with self.assertRaises(TypeError):
            predict_message_mood(123)

    @patch('predict_message_mood.SomeModel')
    def test_predict_message_mood_bad(self, mock_some_model):
        mock_some_model.return_value.predict.return_value = 0.2
        self.assertEqual(
            predict_message_mood("Плохое настроение"),
            "неуд"
        )

    @patch('predict_message_mood.SomeModel')
    def test_predict_message_mood_good(self, mock_some_model):
        mock_some_model.return_value.predict.return_value = 0.9
        self.assertEqual(
            predict_message_mood("Отличное настроение"),
            "отл"
        )

    @patch('predict_message_mood.SomeModel')
    def test_predict_message_mood_normal(self, mock_some_model):
        mock_some_model.return_value.predict.return_value = 0.5
        self.assertEqual(
            predict_message_mood("Нормальное настроение"),
            "норм"
        )

    def test_message_assignment(self):
        model = SomeModel()
        test_message = "Тестовая строка"
        model.predict(message=test_message)
        self.assertEqual(model.get_message(), test_message)

    def test_get_message_returns_correct_message(self):
        model = SomeModel()
        test_message = "Тестовая строка"
        model.message = test_message
        self.assertEqual(model.get_message(), test_message)


if __name__ == '__main__':
    unittest.main()
