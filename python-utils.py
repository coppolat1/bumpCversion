def ask_question(question):
    answer = input('{}: '.format(question))
    return answer.strip()


def ask_multiple_choice_question(question, choices):
    while True:
        print('{}?'.format(question))
        for i in range(len(choices)):
            print('{}. {}'.format(i, choices[i]))

        try:
            user_choice = int(ask_question('Enter Choice'))
        except ValueError:
            user_choice = None

        if user_choice in range(len(choices)):
            break
        else:
            print('Incorrect choice. Please choose a number between 0 and {}'.format(len(choices) - 1))
    return user_choice


def ask_yes_no_question(question):
    while True:
        answer = ask_question('{} (Y/N)'.format(question))
        if answer.lower() == 'y':
            answer = 'yes'
            break
        elif answer.lower() == 'n':
            answer = 'no'
            break
        else:
            print('Incorrect response. Please answer Y/N.')
    return answer