from to_test import *
    

def test_add():
    assert add(2, 3) == 5
    assert add('hello ', 'world') == 'hello world'

def test_failing_test():
    assert False   # This will fail the test
