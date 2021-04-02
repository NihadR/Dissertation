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

with open('dataset.csv', 'w', newline='') as f:
    thewriter = csv.writer(f)

    thewriter.writerow(['row_id','user_id', 'skill_name', 'correct',
                        'start_time', 'end_time'])
    count = 10000000

    for i in range(0, 300000):
        count += 1

        choice = random.randint(0, 1)
        schoice = random.randint(0, 1)
        xchoice = random.randint(0, 1)
        time = random.randint(30000, 500000)
        stime = random.randint(30000, 500000)
        xtime = random.randint(30000, 500000)
        endtime = random_date(d1, d2)
        thewriter.writerow([0, count, 'statement', choice, '1/1/2021 1:30 PM', endtime])
        thewriter.writerow([0,count, 'ifstatement', schoice, '1/1/2021 1:30 PM', endtime])
        thewriter.writerow([0,count, 'forloop', xchoice,  '1/1/2021 1:30 PM', endtime])


# TRAINED PARAMS                               value
# skill       param   class          
# statement   prior   default 0.74341
#             learns  default 1.00000
#             guesses default 0.13280
#             slips   default 0.37607
#             forgets default 0.00000
# ifstatement prior   default 0.67054
#             learns  default 1.00000
#             guesses default 0.22585
#             slips   default 0.36619
#             forgets default 0.00000
# forloop     prior   default 0.83905
#             learns  default 1.00000
#             guesses default 0.02186
#             slips   default 0.40736
#             forgets default 0.00000