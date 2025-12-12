import random


def generate_otp(begin, end):
    return f"{random.randint(begin, end)}"