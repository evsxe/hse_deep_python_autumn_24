from random import uniform


class SomeModel:
    def predict(self, message: str) -> float:
        return uniform(0.0, 1.0)



def predict_message_mood(
    message: str,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    
    predict = SomeModel().predict(
        message=message
    )

    if predict < bad_thresholds:
        return "неуд"

    if predict > good_thresholds:
        return "отл"

    return "норм"


assert predict_message_mood("Чапаев и пустота") == "отл"
assert predict_message_mood("Чапаев и пустота", 0.8, 0.99) == "норм"
assert predict_message_mood("Вулкан") == "неуд"