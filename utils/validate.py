
def validate(name='', uname='', passwd=''):
    # Performs basic checks on user input.
    # Use regular expressions in production version.
    # Applying very basic checks just for testing sake. 
    if len(name) < 4 or len(uname) < 4 or len(passwd) < 8:
        return 0
    return 1

'''

In future versions, validation features will include :-
    : presence of chars other that alphabets in `name` ;
    : `uname` is to be checked as :-
        :: first place should be an alphabet, not a number or a special char.
        :: composed of alphanumeric chars, underbars, periods only.
        :: max length to be set.
    : Email address validator (either built-in or custom)
    : Hash generator (custom hash being feeded to a standard encryption algo)

'''