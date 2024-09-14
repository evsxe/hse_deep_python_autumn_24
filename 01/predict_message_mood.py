from random import uniform

"""Task Description:
    Реализовать функцию predict_message_mood, которая принимает
    на вход строку message и пороги хорошести. Функция возвращает:

    - "неуд", если предсказание модели меньше bad_threshold;
    - "отл", если предсказание модели больше good_threshold;
    - "норм" в остальных случаях.

    Функция predict_message_mood создает экземпляр класса SomeModel 
    и вызывает у этого экземпляра метод predict с аргументом message."""


class SomeModel:
    def __init__(self):
        self.message = ''
        self.random_predict = uniform(0.0, 1.0)

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


assert predict_message_mood("Чапаев и пустота") == "отл"
assert predict_message_mood("Чапаев и пустота",
                            0.8,
                            0.99) == "норм"
assert predict_message_mood("Вулкан") == "неуд"
