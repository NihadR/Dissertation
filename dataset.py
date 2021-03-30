import csv
import random
from datetime import timedelta, datetime


def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


d1 = datetime.strptime('1:30 PM', '%I:%M %p')
d2 = datetime.strptime('2:10 PM', '%I:%M %p')
print(random_date(d1, d2))

with open('dataset.csv', 'w', newline='') as f:
    thewriter = csv.writer(f)

    thewriter.writerow(['user_id', 'skill_name', 'correct',
                        'hints', 'attempts', 'steps', 'start_time', 'end_time'])
    count = 10000000

    for i in range(0, 300000):
        count += 1
        steps = random.randint(1, 2)

        choice = random.randint(0, 1)
        schoice = random.randint(0, 1)
        xchoice = random.randint(0, 1)
        time = random.randint(30000, 500000)
        stime = random.randint(30000, 500000)
        xtime = random.randint(30000, 500000)
        endtime = random_date(d1, d2)
        thewriter.writerow([count, 'statement', choice, 0,
                            1, steps, '1/1/2021 1:30 PM', endtime])
        thewriter.writerow([count, 'ifstatement', schoice,
                            0, 1,  steps, '1/1/2021 1:30 PM', endtime])
        thewriter.writerow([count, 'forloop', xchoice, 0,
                            1,  steps, '1/1/2021 1:30 PM', endtime])