'''
Code lengthy due to implementaion of the following functionality:
If user enters (say) the username and the password fields too short, then 
the name field (and/or others) do not lose their data on page redirect.Instead,
ONLY the invalid fields lose their data and display a message about what went wrong.
'''

def validate(name='', uname='', pswd='', pswd_conf='x'):
    # Performs basic checks on user input,
    # and returns vars that are rendered to the signup page,
    # implementing the functionality of pre-filled valid fields,
    # and blank invalid fields.

    # Use regular expressions in production version.
    # Applying very basic checks just for testing sake.

    error_count = 0
    invalid_fields = valid_fields = invalid_field_names = []
    all_fields = [
                  {
                    'type': 'text',
                    'name': 'name',
                    'value': name
                  },
                  {
                    'type': 'text',
                    'name': 'username',
                    'value': uname
                  },
                  {
                    'type': 'password',
                    'name': 'passwd',
                    'value': pswd
                  },
                  {
                    'type': 'password',
                    'name': 'passwd-conf',
                    'value': pswd_conf
                  }
                 ]
    if len(name) < 3:
        error_count += 1
        invalid_fields.append({
                               'errmsg': 'Name looks too short.',
                               'name': 'name',
                               'type': 'text',
                               'plcdr': 'Enter name (4 characters minimum)'
                              })
    if len(uname) < 3:
        error_count += 1
        invalid_fields.append({
                               'errmsg': 'Username too short.',
                               'name': 'username',
                               'type': 'text',
                               'plcdr':
                                       '''Username (4 characters minimum.
                                       Alphanumerics, '.' or '_' only)
                                       '''
                              })
    if len(pswd) < 7:
        error_count += 1
        invalid_fields.append({
                               'errmsg': 'Set a longer password.',
                               'name': 'name',
                               'type': 'text',
                               'plcdr': 'Set password (8 characters minimum)'
                              })
    if pswd != pswd_conf:
        error_count += 1
        invalid_fields.append({
                               'errmsg': 'Passwords do not match.',
                               'name': 'name',
                               'type': 'text',
                               'plcdr': 'Your name (4 characters at least)'
                              })

    if error_count == 0:
        # If everything is good, or no error..
        return None, None, None
        # The two after first None are just for error prevention; could be anything,
        # as two vars await its return values.

    '''
    Below code executes if there is at least one invalid input.
    '''

    for i in range(len(invalid_fields)):
        # Make a list having names of all invalid inputs.
        field_name = invalid_fields[i]['name']
        invalid_field_names.append(field_name)

    # Now, checking which names are not in the list of invalid inputs,
    # (which was just created), and append it to valid fields' data.
    for i in range(len(all_fields)):
        field_name = all_fields[i]['name']
        if field_name not in invalid_field_names:
            valid_fields.append({
                                 'name': all_fields[i]['name'],
                                 'type': all_fields[i]['type'],
                                 'value': all_fields[i]['value']
                                })

    return error_count, valid_fields, invalid_fields
'''
EXAMPLE:
    invalid_fields = [
        {
            'errmsg': 'Name looks too short. Enter at least four characters',
            'name': 'name',
            'type': 'text',
            'value': ''
        },
        {
            'errmsg': 'Password too short, thus easily crackable',
            'name': 'username',
            'type': 'text',
            'value': ''
        },
    ]
'''


'''
FEATURES TO INCLUDE:
In future versions, validation features will include :-
    : presence of chars other that alphabets in `name` ;
    : `uname` is to be checked as :-
        :: first place should be an alphabet, not a number or a special char.
        :: composed of alphanumeric chars, underbars, periods only.
        :: max length to be set.
    : Email address validator (either built-in or custom)
    : Hash generator (custom hash being feeded to a standard encryption algo)

'''

'''
THINKING LOGIC USED:
First, in the signup page itself, it was assumed what type of data types we needed.
For example, it came out to be {{field.type}} etc.
So, the main route should deliver a var (list of dicts), which should first be returned 
by the validator function.
Hence, conditions were found, and implemented in code.

The main thing is: THINK REVERSE!
It can prove helpful in analysing how to start when a complicated functionality needs to be
implemented.
'''