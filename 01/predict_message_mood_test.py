import unittest

from unittest.mock import patch

from predict_message_mood import predict_message_mood, SomeModel


class TestPredictMessageMood(unittest.TestCase):

    def test_message_type_error(self):
        with self.assertRaises(TypeError):
            predict_message_mood(123)

    @patch('predict_message_mood.SomeModel')
    def test_predict_message_mood_bad(self, mock_some_model):
        test_message = "Плохое настроение"
        mock_some_model.return_value.predict.return_value = 0.2
        mock_some_model.return_value.get_message.return_value = test_message
        result = predict_message_mood(
            test_message,
            bad_thresholds=0.3,
            good_thresholds=0.8
        )
        self.assertEqual(result, "неуд")
        mock_some_model.return_value.predict.assert_called_once_with(
            message=test_message
        )

    @patch('predict_message_mood.SomeModel')
    def test_predict_message_mood_good(self, mock_some_model):
        test_message = "Отличное настроение"
        mock_some_model.return_value.predict.return_value = 0.9
        mock_some_model.return_value.get_message.return_value = test_message
        result = predict_message_mood(
            test_message,
            bad_thresholds=0.3,
            good_thresholds=0.8
        )
        self.assertEqual(result, "отл")
        mock_some_model.return_value.predict.assert_called_once_with(
            message=test_message
        )

    @patch('predict_message_mood.SomeModel')
    def test_predict_message_mood_normal(self, mock_some_model):
        test_message = "Нормальное настроение"
        mock_some_model.return_value.predict.return_value = 0.5
        mock_some_model.return_value.get_message.return_value = test_message
        result = predict_message_mood(
            test_message,
            bad_thresholds=0.3,
            good_thresholds=0.8
        )
        self.assertEqual(result, "норм")
        mock_some_model.return_value.predict.assert_called_once_with(
            message=test_message
        )

    @patch('predict_message_mood.SomeModel')
    def test_predict_message_mood_bad_thresholds_less_than_good_thresholds(
            self,
            mock_some_model
    ):
        test_message = "Плохое настроение"
        mock_some_model.return_value.predict.return_value = 0.2
        mock_some_model.return_value.get_message.return_value = test_message
        result = predict_message_mood(
            test_message,
            bad_thresholds=0.2,
            good_thresholds=0.3
        )
        self.assertEqual(result, "норм")
        mock_some_model.return_value.predict.assert_called_once_with(
            message=test_message
        )

    @patch('predict_message_mood.SomeModel')
    def test_predict_message_mood_bad_thresholds_equal_good_thresholds(
            self,
            mock_some_model
    ):
        test_message = "Нормальное настроение"
        mock_some_model.return_value.predict.return_value = 0.5
        mock_some_model.return_value.get_message.return_value = test_message
        result = predict_message_mood(
            test_message,
            bad_thresholds=0.5,
            good_thresholds=0.5
        )
        self.assertEqual(result, "норм")
        mock_some_model.return_value.predict.assert_called_once_with(
            message=test_message
        )

    @patch('predict_message_mood.SomeModel')
    def test_predict_message_mood_slightly_above_bad_threshold(self,
                                                               mock_some_model):
        test_message = "Slightly above bad mood"
        mock_some_model.return_value.predict.return_value = 0.31
        mock_some_model.return_value.get_message.return_value = test_message
        result = predict_message_mood(test_message,
                                      bad_thresholds=0.3,
                                      good_thresholds=0.8)

        self.assertEqual(result, "норм")

    @patch('predict_message_mood.SomeModel')
    def test_predict_message_mood_near_good_threshold(self, mock_some_model):
        test_message = "Почти отличное настроение"
        mock_some_model.return_value.predict.return_value = 0.79
        mock_some_model.return_value.get_message.return_value = test_message
        result = predict_message_mood(test_message,
                                      bad_thresholds=0.3,
                                      good_thresholds=0.8)

        self.assertEqual(result, "норм")

    @patch('predict_message_mood.SomeModel')
    def test_predict_message_mood_slightly_below_good_threshold(
            self,
            mock_some_model
    ):
        test_message = "Slightly below good mood"
        mock_some_model.return_value.predict.return_value = 0.81
        mock_some_model.return_value.get_message.return_value = test_message
        result = predict_message_mood(test_message,
                                      bad_thresholds=0.3,
                                      good_thresholds=0.8)

        self.assertEqual(result, "отл")

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
