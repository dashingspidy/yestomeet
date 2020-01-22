from datetime import datetime


def age(birthday):
    b_date = datetime.strptime(str(birthday), '%Y-%m-%d')
    return int((datetime.today() - b_date).days / 365)
