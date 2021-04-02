infor = [{

    'type': 'Statement',
    'info': '''A statement defines an action in a java program. It can be used to add to variables together, or define a variable,
    as shown in the example below. When creating a statement, the type has to be declared. Looking at the example below
    you can see that random_number is of type integer and has been assigned a value of 10. For example, a variable with 
    type str (string) would have a value 'hi' assigned to it. ''',
    'example': '''public class Main {
        public static void main(String[] args) {
            int random_number =10;
            System.out.println(random_number);
         }
    }'''

},
{
    'type': 'If Statement',
    'info': '''An if statement is used to execute a condition when true, this can best be shown in an example. Looking at the code below we can see the code checks to see if 5 is greater than 10, if so it will print out the line 'Hello World' 
    If statements are very powerful and do not only have to be used for evaluating simple conditions such as these.  ''',
    'example': '''
       public class Main {
        public static void main(String[] args) {
            if(5>10);
            System.out.println('Hello World');
         }
    }
    '''
},
{
    'type': 'For Loop',
    'info': '''For loops are a control flow that iterate over a certain part of a program multiple times.
     The syntax involves 3 parts, first "int i = 1", this initialises the variable in the loop and is executed once before the rest of the block,
      the next part specifies the condition that will be executed, so in this example it will continue looping while the condition that i is less than 10 is true, the last part increments the value of i, so with each loop i increases, this can be set to decrease as well. ''',
    'example': '''   public class Main{
        public static void main(String[] args) {
            for(int i = 1; i < 10; i++){
                System.out.println(i);
            }
         }
    }'''
}
]