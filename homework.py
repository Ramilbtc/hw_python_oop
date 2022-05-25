from typing import Dict
class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,  # Тип тренировки
                 duration: float,  # Длительность тренировки (время)
                 distance: float,  # Дистанция (км)
                 speed: float,  # Средняя скорость на дистанции (км/ч)
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Вернуть информационное сообщение о  тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65  # расстояние (за один шаг)
    M_IN_KM: float = 1000  # конвертер из км в метры
    MIN_IN_H_CONST: float = 60  # минуты в часах

    def __init__(self,
                 action: int,  # количество действий
                 duration: float,  # длительность тренировки
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight  # вес спортсмена

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Определить get_spent_calories в %s.' %
            (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    RUNNING_1_CONST: float = 18  # const 1 running (каллории)
    RUNNING_2_CONST: float = 20  # const 2 running (каллории)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.RUNNING_1_CONST * self.get_mean_speed()
                - self.RUNNING_2_CONST) * self.weight
                / self.M_IN_KM
                * self.duration * self.MIN_IN_H_CONST)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WALKING_1_CONST: float = 0.035
    WALKING_2_CONST: float = 0.029
    WALKING_3_CONST: float = 2

    def __init__(self,
                 action: int,  # количество действий
                 duration: float,  # длительность тренировки
                 weight: float,  # вес спортсмена
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height  # рост спортсмена

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.WALKING_1_CONST
                * self.weight
                + ((self.get_mean_speed()
                    ** self.WALKING_3_CONST)
                    // self.height)
                * self.WALKING_2_CONST
                * self.weight)
                * self.duration
                * self.MIN_IN_H_CONST)


class Swimming(Training):
    """Тренировка: плавание."""

    SWIMMING_1_CONST: float = 1.1  # const 1 swimming (каллории)
    SWIMMING_2_CONST: float = 2  # const 2 swimming (каллории)
    LEN_STEP: float = 1.38  # расстояние (за один гребок)

    def __init__(self,
                 action: int,  # количество действий
                 duration: float,  # длительность тренировки
                 weight: float,  # вес спортсмена
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool  # длина бассейна
        self.count_pool = count_pool  # сколько раз переплыл бассейн

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.lenght_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.SWIMMING_1_CONST)
                * self.SWIMMING_2_CONST * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    parameters_training: Dict[str, list] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return parameters_training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    return print(info.get_message())

if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
