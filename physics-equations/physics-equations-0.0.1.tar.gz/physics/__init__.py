import math


def functionOne(initialVelocity: float, finalVelocity: float, acceleration: float, time: float):
    if initialVelocity is None:
        return round(finalVelocity - acceleration * time, 2)
    elif finalVelocity is None:
        return round(initialVelocity + acceleration * time, 2)
    elif acceleration is None:
        return round((finalVelocity - initialVelocity) / time, 2)
    elif time is None:
        return round((finalVelocity - initialVelocity) / acceleration, 2)


def functionTwo(distance: float, initialVelocity: float, finalVelocity: float, acceleration: float):
    if distance is None:
        return ((finalVelocity ** 2) - (initialVelocity ** 2)) / (2 * acceleration)
    elif initialVelocity is None:
        return math.sqrt((finalVelocity ** 2) - (2 * acceleration * distance))
    elif finalVelocity is None:
        return math.sqrt((initialVelocity ** 2) + (2 * acceleration * distance))
    elif acceleration is None:
        return ((finalVelocity ** 2) - (initialVelocity ** 2)) / (2 * distance)


def functionThree(distance: float, initialVelocity: float, acceleration: float, time: float):
    if distance is None:
        return (initialVelocity * time) + (.5 * acceleration * (time ** 2))
    elif initialVelocity is None:
        return (distance - .5 * acceleration * time ** 2) / time
    elif acceleration is None:
        return 2 * (distance - initialVelocity * time) / (time ** 2)
    elif time is None:
        temp = math.sqrt(initialVelocity ** 2 + 2 * acceleration * distance)
        valueOne = (-initialVelocity + temp) / acceleration
        valueTwo = (-initialVelocity - temp) / acceleration
        if abs(valueOne) != valueOne:
            return valueTwo
        elif abs(valueTwo) != valueTwo:
            return valueOne
        else:
            return [
                (-initialVelocity + temp) / acceleration,
                (-initialVelocity - temp) / acceleration
            ]
