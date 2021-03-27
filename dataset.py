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


# 0.49999778316146715   20000 users hints attempts version
#                               value
# skill       param   class
# statement   prior   default 0.51768
#             learns  default 1.00000
#             guesses default 0.08492
#             slips   default 0.11791
#             forgets default 0.00000
# ifstatement prior   default 0.46239
#             learns  default 1.00000
#             guesses default 0.10059
#             slips   default 0.03693
#             forgets default 0.00000
# forloop     prior   default 0.95682
#             learns  default 1.00000
#             guesses default 0.14763
#             slips   default 0.48335
#             forgets default 0.00000
# Training RMSE: 0.499998
# Training AUC: 0.501387

# 0.4999998507344081  300000 users hints attempts version
#                               value
# skill       param   class
# statement   prior   default 0.24823
#             learns  default 1.00000
#             guesses default 0.38390
#             slips   default 0.14629
#             forgets default 0.00000
# ifstatement prior   default 0.38854
#             learns  default 1.00000
#             guesses default 0.23484
#             slips   default 0.08192
#             forgets default 0.00000
# forloop     prior   default 0.72720
#             learns  default 1.00000
#             guesses default 0.06287
#             slips   default 0.33563
#             forgets default 0.00000
# Training RMSE: 0.500000
# Training AUC: 0.500107

# 0.49999999115324695  1000000 users hints attempts version
# value
# skill       param class
# statement   prior   default 0.60372
# learns  default 1.00000
# guesses default 0.04953
# slips   default 0.20446
# forgets default 0.00000
# ifstatement prior   default 0.91941
# learns  default 1.00000
# guesses default 0.13172
# slips   default 0.46757
# forgets default 0.00000
# forloop     prior   default 0.51214
# learns  default 1.00000
# guesses default 0.04452
# slips   default 0.06613
# forgets default 0.00000
# Training RMSE: 0.500000
# Training AUC: 0.500100
