from builtins import range
from django import template
from website.models import Question, Answer

register = template.Library()


def category_question_count(category):
    """Return the number of active and non-spam questions in the category."""
    category_question_count = Question.objects.filter(category=category, is_active=True, is_spam=False).count()
    return category_question_count

register.simple_tag(category_question_count)


def answer_count(question):
    """Return the number of active and non-spam answers to a question."""
    return question.answer_set.filter(is_active=True, is_spam=False).count()

register.simple_tag(answer_count)


def total_question_count():
    """Return total number of active and non-spam questions on forum."""
    count = Question.objects.filter(is_active=True, is_spam=False).count()
    return count

register.simple_tag(total_question_count)


def total_answer_count():
    """Return total number of active and non-spam answers on forum."""
    count = Answer.objects.filter(is_active=True, is_spam=False).count()
    return count

register.simple_tag(total_answer_count)


# Implementing range(x) function in templates

def get_range(value, arg=''):
    args = arg.split(', ')
    n = len(args)

    if n == 0 or arg == '':
        # if no arguments set value as limit
        start = 0
        limit = value
        step = 1
    elif n == 1:
        start = int(args[0])
        limit = value
        step = 1
    elif n == 2:
        start = int(args[0])
        limit = value
        step = int(args[1])
    else:
        raise TypeError(
            'get_range() takes maximum 2 arguments, {} given'.format(n))
    return list(range(start, limit, step))


register.filter('get_range', get_range)


# Implementing increment and decrement functions

def inc(value, arg=1):
    return value + int(arg)

register.filter('inc', inc)


def dec(value, arg=1):
    return value - int(arg)

register.filter('dec', dec)


# Implementing calculator for templates

def add(value, arg=0):
    return value + int(arg)

register.filter('add', add)


def sub(value, arg=0):
    return value - int(arg)

register.filter('sub', sub)


def mul(value, arg=1):
    return value * int(arg)

register.filter('mul', mul)


def div(value, arg=1):
    return value / arg

register.filter('div', div)


# Get length of array

def length(array):
    return len(array)

register.simple_tag(length)
