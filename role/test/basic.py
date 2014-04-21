import unittest
import role.test.hacker
import role.test.interface
import role.test.messenger
import role.test.passenger

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

    def test_consume_two_roles(self):
        @consume(role.test.messenger, role.test.passenger)
        class Foo(object):
            def how(self):
                return 'I am fine'
        obj = Foo()
        self.assertEqual(obj.hello(), 'hello world')
        self.assertEqual(obj.introduce(), 'I am the passenger')
        self.assertEqual(obj.how(), 'I am fine')
        self.assertEqual(obj.bye(), 'bye bye world')

    def test_conflict_managed_separately(self):
        @consume(role.test.hacker)
        @consume(role.test.passenger)
        class Foo(object):
            pass
        obj = Foo()
        self.assertEqual(obj.introduce(), 'I am the passenger')

    def test_conflict_managed(self):
        @consume(role.test.hacker, role.test.passenger)
        class Foo(object):
            def introduce(self):
                return 'I am somebody'
        obj = Foo()
        self.assertEqual(obj.introduce(), 'I am somebody')

    def test_conflict_unmanaged(self):
        with self.assertRaisesRegexp(NameError, 'conflicts with'):
            @consume(role.test.hacker, role.test.passenger)
            class Foo(object):
                def talk(self):
                    return self.introduce()

    def test_requirements_managed(self):
        @consume(role.test.interface, role.test.passenger)
        class Foo(object):
            def walk(self):
                return 'Walking along'
        obj = Foo()
        self.assertEqual(obj.talk(), 'I am the passenger')
        self.assertEqual(obj.walk(), 'Walking along')

    def test_requirements_unmanaged(self):
        with self.assertRaisesRegexp(TypeError, 'which is required by'):
            @consume(role.test.interface, role.test.passenger)
            class Foo(object):
                pass

if __name__ == '__main__':
    unittest.main()
