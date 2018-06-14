from django.test import TestCase


from random import choice
import string



def GenPassword(length=8,chars=string.ascii_letters+string.digits):
    return ''.join([choice(chars) for i in range(length)])

if __name__=="__main__":

    for i in range(10):

        print(GenPassword(8))