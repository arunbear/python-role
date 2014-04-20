import unittest
import role.test.messenger

from role import consume

class RoleTester(unittest.TestCase):
    def test_consume_one_role(self):
        @consume(role.test.messenger)
        class Foo(object):
            def how(self):
                return 'I am fine'
        obj = Foo()
        self.assertEqual(obj.hello(), 'hello world')
        self.assertEqual(obj.how(), 'I am fine')
        self.assertEqual(obj.bye(), 'bye bye world')


if __name__ == '__main__':
    unittest.main()
