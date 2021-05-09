TOTAL_LENGTH = 79


def make_line_exact_length(line):
    """
    For each line, add a '-' at the start and end based on the TOTAL_LENGTH global at the top of
    this file.

    :param line: The line that is to have the '-' added to ti.
    :return: A line with '-' added to the front and end
    :rtype: str
    """
    whitespace = TOTAL_LENGTH - len(line) - 3
    return f'\n- {line}{" " * (whitespace)}-'


def main(prompt):
    """
    Adds a box around the prompt.

    :param prompt: The string that is to have a box applied to it.
    :return: A string, identical to the first, but with a box placed around it.
    :rtype: str
    """
    output_string = "-" * TOTAL_LENGTH
    for line in prompt.split("\n"):
        output_string += make_line_exact_length(line)
    output_string += "\n" + "-" * TOTAL_LENGTH
    return output_string


def evaluate_if_correct(value, correct_value):
    """
    Simple helper function that basically does an assertion. This makes it easier to print to the report.

    :param value: The result of a report (boolean)
    :param correct_value: The correct result of a report (boolean)
    :return: A boolean indicating if the values match
    :rtype: bool
    """
    if value and correct_value:
        return 'Correct!'
    elif not value and not correct_value:
        return 'Correct!'
    else:
        return 'Not Correct...'