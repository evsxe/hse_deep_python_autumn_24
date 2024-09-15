from random import uniform


class SomeModel:
    def __init__(self):
        self.message = ''
        self.random_predict = uniform(0.0, 1.0)

    def get_message(self) -> str:
        """
        :return: message used for prediction
        """
        return self.message

    def predict(self, message: str) -> float:
        """
        :param message: any string
        :return: model prediction (random number provided by the uniform module)
        """
        self.message = message
        return self.random_predict


def predict_message_mood(
        message: str,
        bad_thresholds: float = 0.3,
        good_thresholds: float = 0.8,
) -> str:
    """
    :param message: any string
    :param bad_thresholds: threshold for a score of "неуд"
    :param good_thresholds: threshold for a score of "отл"
    :return: string estimate
    """

    if not isinstance(message, str):
        raise TypeError("message must be a string")

    predict = SomeModel().predict(
        message=message
    )

    if predict < bad_thresholds:
        return "неуд"

    if predict > good_thresholds:
        return "отл"

    return "норм"
