from parenthenesis_parser import parser, prettify_report


if __name__ == "__main__":
    prompt = """Prompt:
    
    The parenthesis parsingInput: A string of open and closed parenthesis.
    Output: True or False based on if the string is a valid expression.
    Example:
        (()) returns True
        )()( returns False
        ()() returns True
        ((()) returns False
    Describe the algorithm or pseudo code to solve this challenge."""

    explanation = """Explanation: 
    
    The algorithm you would use to solve this is a stack.  There are a few conditions that are 
    easy to check for that would render the input False that can be checked for outside of the 
    stack. These are:
    
    * When the string is odd
    * When the string starts with a closing or ends with an open
    * When the string contains a different number of opens and closes
    
    These can be checked for in the context of a stack, but it's very easy to check for them 
    initially with basic things like regex or counting; I therefore elected to do these outside 
    of the algorithm itself.  
    
    For any string that doesn't fail with the obvious rejection criteria, we append the opening 
    to a list.  When we see the closing, we likewise "pop" from the list, which in Python removes an 
    element from the list; in this case, the default is index [0].  After looping through the 
    entire string, if we are left with no elements, it means that the stack was balanced properly 
    and we return True.
    
    Details on what each of the methods do can be found in the docstrings in 
    parenthesis_parser.parser.
    
    Note that I also added a sanitization function to eliminate any non-parentheticals. This is 
    technically unnecessary for these strings but I like to sanitize my inputs so that it is 
    explicit that my code wouldn't handle something it isn't designed for, which in this case is 
    essentially any string that contains characters other than opening "(" and closing ")" 
    parenthesis."""



    p1 = parser.ParenthesisParser()
    result1 = p1.parse("(())")  # True
    result_status1 = prettify_report.evaluate_if_correct(result1, True)

    result2 = p1.parse(")()(")  # False
    result_status2 = prettify_report.evaluate_if_correct(result2, False)

    result3 = p1.parse("()()")  # True
    result_status3 = prettify_report.evaluate_if_correct(result3, True)

    result4 = p1.parse("((())")  # False
    result_status4 = prettify_report.evaluate_if_correct(result4, False)

    result = f'''Results: 
    
    "(())" Correct value: True   | Evaluated value: {result1}  ({result_status1})  
    ")()(" Correct value: False  | Evaluated Value: {result2} ({result_status2})
    "()()" Correct value: True   | Evaluated Value: {result3}  ({result_status3})
    "((())" Correct value: False | Evaluated Value: {result4} ({result_status4})
    '''

    for string_to_print in [prompt, explanation, result]:
        print(string_to_print + "\n\n")


