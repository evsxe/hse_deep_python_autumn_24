import unittest
from predict_message_mood import predict_message_mood, SomeModel

class TestPredictMessageMood(unittest.TestCase):

    def setUp(self):
        self.model = SomeModel()
        self.text = 'test'

    def test_message_type_error(self):
        with self.assertRaises(TypeError):
            predict_message_mood(123)

    def test_predict_message_mood_bad(self):
        self.model.random_predict = 0.2
        self.assertEqual(
            predict_message_mood("Плохое настроение"),
            "неуд"
        )

    def test_predict_message_mood_good(self):
        self.model.random_predict = 0.9
        self.assertEqual(
            predict_message_mood("Отличное настроение"),
            "отл"
        )

    def test_predict_message_mood_normal(self):
        self.model.random_predict = 0.5
        self.assertEqual(
            predict_message_mood("Нормальное настроение"),
            "норм"
        )

    def test_predict_message_mood_custom_thresholds(self):
        self.model.random_predict = 0.7
        self.assertEqual(
            predict_message_mood(
                "Нормальное настроение",
                bad_thresholds=0.6,
                good_thresholds=0.9
            ),
            "неуд"
        )

    def test_predict_message_mood_custom_thresholds_2(self):
        self.model.random_predict = 0.85
        self.assertEqual(
            predict_message_mood(
                "Нормальное настроение",
                bad_thresholds=0.6,
                good_thresholds=0.9
            ),
            "отл"
        )


if __name__ == '__main__':
    unittest.main()