"""
Woaw what an awesome module. I wonder who's that good...!
"""


def send_batman(person, model):
    """Returns whether or not the person Batman should be called on this
    person based on a statistical model

    Args:
        person (str): the target's name
        model (code.Model): model to perform inference with

    Returns:
        bool: blabla
    """

    print(person, model)
    return person in model
