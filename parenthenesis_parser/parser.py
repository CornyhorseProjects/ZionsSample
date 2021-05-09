import re


def sanitize_string(string):
    """
    As the goal of this is to determine only if the parenthesis are balanced, we remove any
    characters that are not specifically related to this goal.

    :return: Returns a sanitized string with only the opening "(" and closing ")" parenthesis.
    :rtype: str
    """
    return re.sub(r"[^)(]", "", string)


class ParenthesisParser:
    """
    This parenthesis parser contains a method, parse, which accepts a string.  From a user
    perspective, this is really the only method that is likely to be called. It ties together the
    balance of the functionality of the parser.  The class itself only exists to maintain
    attributes, which are easier to pass around in this instance as class attributes rather than
    using globals or similar with a functional programming approach.
    """

    def __init__(self):
        self.string = ""
        self.stack = list()
        self.reject_based_on_length = False
        self.reject_based_on_incorrect_closing_or_opening = False
        self.reject_based_on_number_of_open_and_closed = False
        self.total_open = 0
        self.total_close = 0

    def parse(self, string):
        """
        Calling this method resets all of the class attributes and then checks to see if the
        string meets any of the immediate rejection criteria. If the rejection criteria are met,
        it returns "False" and doesn't parse. If the rejection criteria are not met, it invokes
        the check_for_balance method, which itself generates a stack and verifies that the
        parenthesis are balanced in the string.

        :param string: str
        :return: A boolean indicating whether or not the string is balanced or not.
        :rtype: bool
        """
        self.reset_varaibles(string)

        if self.check_for_rejection_criteria():
            return False
        else:
            return self.check_for_balance()

    def reset_varaibles(self, string):
        """
        When we invoke the "parse" command, we need to wipe the class attributes to reflect the
        new string.  This is essentially a "setter" method in the jargon of other pure
        object-oriented languages.

        :param string: The string that is to be parsed.
        :return: None
        """
        self.string = sanitize_string(string)
        self.stack = list()
        self.reject_based_on_length = False
        self.reject_based_on_incorrect_closing_or_opening = False
        self.reject_based_on_number_of_open_and_closed = False
        self.total_open = 0
        self.total_close = 0

    def check_for_rejection_criteria(self):
        """
        There are some "low-hanging-fruit" criteria that we can use to reject a string. These
        include:

        * Strings with odd number of characters after removing all of the
        non-parenthetical characters; by definition, these strings cannot be balanced.

        * Strings that have a diverging number of open and closing parenthesis

        * Strings that start with a closing or end with an opening.


        :return: Boolean (true) indicating if we can immediately reject the string as being
        unbalanced
        :rtype: bool
        """
        self.check_if_can_reject_based_on_string_length()
        self.check_if_can_reject_based_on_start_or_end_position()
        self.check_if_can_reject_based_on_number_of_open_and_close()

        if (
            self.reject_based_on_incorrect_closing_or_opening
            or self.reject_based_on_length
            or self.reject_based_on_number_of_open_and_closed
        ):
            return True

    def check_for_balance(self):
        """
        For any string that has not yet been rejected, we simply add the parentheticals to a
        stack to see if they are balanced.  Note that we've removed things like starting with a
        closing bracket; therefore, this specific method makes no attempt to remove them because at
        this stage, they've already been rejected.

        By simply popping the opening character from the list, by the time we're done,
        if any element in th elist remais, it means it is unbalanced.

        :return: Boolean value indicating if the string has balanced parenthesis.
        :rtype: bool
        """

        # For any even length string, check to see if the inverse position matches:
        for i, character in enumerate(self.string):
            if character == "(":
                self.stack.append(character)
            elif character == ")":
                self.stack.pop()

        if len(self.stack) == 0:
            return True
        else:
            return False

    def check_if_can_reject_based_on_number_of_open_and_close(self):
        """
        For instances where there might be additional opens/closes, there's no point in parsing
        because we can immediately rule out that they will be unbalanced.

        :return: None
        """
        self.total_open = self.string.count("(")
        self.total_close = self.string.count(")")
        if self.total_close != self.total_open:
            self.reject_based_on_number_of_open_and_closed = True

    def check_if_can_reject_based_on_start_or_end_position(self):
        """
        If the string starts with a closing or ends with an opening, it is by definition not
        balanced, so we can reject it immediately. Updates the class attribute
        reject_based_on_incorrect_closing_or_opening, which is checked before parsing.

        :return: None
        """
        if self.string[0] == ")" or self.string[-1] == "(":
            self.reject_based_on_incorrect_closing_or_opening = True

    def check_if_can_reject_based_on_string_length(self):
        """
        If there is an odd number, there's no sense in checking to see if all of the elements
        match; by definition, they cannot match if there is an odd number of parenthesis.  This
        method updates the class attribute "reject_based_on_length" if it has an odd number,
        which is checked immediately before parsing.

        :return: None
        """
        if len(self.string) % 2 != 0:
            self.reject_based_on_length = True
