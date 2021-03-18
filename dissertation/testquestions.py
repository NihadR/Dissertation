questions = [
    {'id': '1',
     'question': 'Create a statement price which is equal to 10 and another statement called money which is equal to 15. Using these two statements work out the money left after buying the product.',
     'answers': {'1': '''
    public class Main {
        public static void main(String[] args) {
            Int Price =10;
            Int Money =15;
            Int Money_After = money-price;
            System.out.println(Money_After);
         }
    }''',
                 '2':  '''
    public class Main {
        public static void main(String[] args) {
            String Price =10;
            String Money =15;
            String Money_After = money-price;
            System.out.println(Money_After);
        }
    }''',
                 '3':  '''
    public class Main {
        public static void main(String[] args) {
            Int Price =15;
            Int Money =10;
            String Money_After = price-money;
            System.out.println(Money_After);
        }
    }''',
                 '4':   '''  I don’t know'''},
     'correct': '1'},

    {"id": "2",
     "question": 'Using these variables, Wallet = 50, GoodA = 20, GoodB = 25, Using these variables check whether the total of GoodA and GoodB are greater than the value of Wallet and if so return the value of wallet after purchasing these goods',
     "answers": {'1': '''
    public class Main {
        public static void main(String[] args) {
            int wallet = 50;
            int goodA = 20;
            int goodB = 25;
            if (goodA + goodB < wallet){
                wallet = wallet - (goodA-goodB);
                System.out.println(wallet);}
                }
            }''',
                 '2': '''
    public class Main {
        public static void main(String[] args) {
            int wallet = 50;
            int goodA = 20;
            int goodB = 25;
            if (goodA & & goodB < wallet){
                wallet= wallet - (goodA+goodB);
                System.out.println(wallet); }
                }
            }''',
                 '3': '''
    public class Main {
        public static void main(String[] args) {
            int wallet= 50;
            int goodA= 20;
            int goodB= 25;
            if (goodA + goodB < wallet){
                wallet= wallet - (goodA+goodB);
                System.out.println(wallet); }
            }
            }''', '4': "  I don't know"},
     "correct": '3'

     }, {"id": "3",
         "question": 'Write a program to calculate the sum of the numbers 1 to 10',
         "answers": {'1': '''
    public class Main{
        public static void main(String[] args) {
            int num= 10;
            int sum= 0;
            for(int i=1; i < num; ++i){
                sum += i;
            }
            System.out.println(sum); }
    }''',
                     '2':   '''
     public class Main{
        public static void main(String[] args) {
            int num= 10;
            int sum= 0;
            for(int i=1; i <= num; ++i){
            sum += i;
            }
            System.out.println(sum); }
    }''',
                     '3':     '''
     public class Main{
        public static void main(String[] args) {
            int num= 10;
            int sum= 0;
            for(int i = 1; i < num;){
            sum += i;
            }
            System.out.println(sum); }
    }''',
                     '4':      "  I don't know"},
         "correct":  '3'
         },

    {"id": "4",
     "question": 'Transalate this statement into an if statement, if it is raining today then I will stay home ',
     "answers": {'1': '''
    public class Main {
        public static void main(String[] args) {
            Bool stayHome = False;
            Bool isRaining = True;
            if (isRaining == True);
                stayHome = True;
        }
    }''',
                 '2': '''
    public class Main {
        public static void main(String[] args) {
            Bool stayHome = False;
            Bool isRaining = True;
            if (isRaining.isequals(True));
                stayHome = True;
        }
    }''',
    '3': '''
    public class Main {
        public static void main(String[] args) {
            Bool stayHome = False;
            Bool isRaining = True;
            if (isRaining = True);
                stayHome = true;
        }
    }''',
     '4': "I don't know"},
     'correct': '1'},
    {"id": "5",
     "question": 'Which input would create an infinite for loop?',
     "answers": {'1': 'for(i=0, i++)', '2': 'for(;;)'},
     'correct': '2'},
    {"id": "6",
     "question": "A statement does not require the type to be declared?",
     "answers": {'1': 'True', '2': 'False'},
     'correct': '2'}

]


lsquestions = {
    'How do you best revise?': ['Through the use of diagrams', 'Through the use of videos and lectures',
                                'Through notes and reading material', 'Through participating in practicals'],
    "What's the best way for you to learn something new?": ['Through charts', 'Watching a video about it',
                                                            'Reading a book about it', 'Figuring it out on your own'],
    "In a new country how would you find your way around?": ['Using a map', 'Using the internet',
                                                             'Read an atlas', 'Walk around till you find your destination'],
    "What kind of book do you like to read": ["A book with images", "Audio book", "A novel", "Book with crosswords"],
    "What do you think about exams?": ['Would prefer if they have more diagram based questions', 'Would prefer more oral questions',
                                       'I like them', 'Would prefer more practical assessments'],
    "How do you solve problems": ["Visualising the problem", "Thinking out loud", "Through writing the problem down",
                                  "Thinking about while exercising"]
}
lsquestions3 = {
    "What do you like to do relax?": ['Read', 'Listen to music', 'Exercise'],
    "In what setting do you learn the best": ['Study group', 'Study session by yourself', 'Field Trips'],
    "Can you memorise song lyrics after listening to it a few times?": ['Yes, I can memorise it easily', 'No, I need to read the song lyrics',
                                                                        "No, but I prefer dancing to it"],
    "Do you find youself needing to take frequent breaks when studying or restless during a lecture": ['No, I like it', 'Yes, its too much reading for me ', 'Yes, I would like more practical based material']
}
