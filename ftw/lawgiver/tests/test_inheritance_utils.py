from ftw.lawgiver.utils import get_roles_inherited_by
from ftw.lawgiver.utils import get_roles_inheriting_from
from ftw.lawgiver.utils import merge_role_inheritance
from ftw.lawgiver.wdl.specification import Specification
from ftw.lawgiver.wdl.specification import Status
from unittest import TestCase


ROLE_MAPPING = {'admin': 'Manager',
                'visitor': 'Anonymous',
                'writer': 'Editor'}


class TestMergeRoleInheritance(TestCase):

    def test_includes_general_inheritance(self):
        spec = Specification(title='My Workflow',
                             role_inheritance=[('admin', 'visitor')],
                             role_mapping=ROLE_MAPPING)
        status = Status('Private', [])

        self.assertEqual(
            [('Manager', 'Anonymous')],
            merge_role_inheritance(spec, status))

    def test_includes_status_inheritance(self):
        spec = Specification(title='My Workflow',
                             role_mapping=ROLE_MAPPING)
        status = Status('Private', [],
                        role_inheritance=[('admin', 'writer')])

        self.assertEqual(
            [('Manager', 'Editor')],
            merge_role_inheritance(spec, status))

    def test_merges_general_and_status_inheritance(self):
        spec = Specification(title='My Workflow',
                             role_inheritance=[('admin', 'visitor')],
                             role_mapping=ROLE_MAPPING)
        status = Status('Private', [],
                        role_inheritance=[('admin', 'writer')])

        self.assertCountEqual(
            [('Manager', 'Anonymous'),
             ('Manager', 'Editor')],
            merge_role_inheritance(spec, status))


class TestGetRolesInheritingFrom(TestCase):

    def test_docstring_example(self):
        # A inherits from B
        # B inherits from C
        role_inheritance = (('A', 'B'), ('B', 'C'))
        self.assertEqual(['A'],
                         get_roles_inheriting_from(['A'], role_inheritance))
        self.assertEqual(['A', 'B'],
                         get_roles_inheriting_from(['B'], role_inheritance))
        self.assertEqual(['A', 'B', 'C'],
                         get_roles_inheriting_from(['C'], role_inheritance))

    def test_basic_resolution(self):
        self.assertEqual(
            ['Anonymous', 'Manager'],
            get_roles_inheriting_from(
                ['Anonymous'],
                [('Manager', 'Anonymous')]))

    def test_recursive_resolution(self):
        self.assertEqual(
            ['Anonymous', 'Contributor', 'Editor', 'Manager'],

            get_roles_inheriting_from(
                ['Anonymous'],
                [('Contributor', 'Anonymous'),
                 ('Manager', 'Editor'),
                 ('Editor', 'Contributor')]))

    def test_basic(self):
        self.assertEqual(
            set(['Foo', 'Bar']),
            set(get_roles_inheriting_from(['Foo'], [('Bar', 'Foo')])))

    def test_not_matching(self):
        self.assertEqual(
            set(['Foo']),
            set(get_roles_inheriting_from(['Foo'], [('Bar', 'Baz')])))

        self.assertEqual(
            set(['Foo']),
            set(get_roles_inheriting_from(['Foo'], [('Foo', 'Bar')])))

    def test_multi_stage(self):
        expected = set(['Foo', 'Bar', 'Baz'])
        roles = ['Foo']

        self.assertEqual(
            expected,
            set(get_roles_inheriting_from(
                roles,
                [('Bar', 'Foo'),
                 ('Baz', 'Bar')])))

        self.assertEqual(
            expected,
            set(get_roles_inheriting_from(
                roles,
                [('Baz', 'Bar'),
                 ('Bar', 'Foo')])))

    def test_circular(self):
        expected = set(['Foo', 'Bar', 'Baz'])
        roles = ['Foo']
        role_inheritance = [('Foo', 'Bar'),
                            ('Bar', 'Baz'),
                            ('Baz', 'Foo')]

        self.assertEqual(
            expected,
            set(get_roles_inheriting_from(roles, role_inheritance)))


class TestGetRolesInheritedBy(TestCase):

    def test_docstring_example(self):
        # A inherits from B
        # B inherits from C
        role_inheritance = (('A', 'B'), ('B', 'C'))

        self.assertEqual(['A', 'B', 'C'],
                         get_roles_inherited_by(['A'], role_inheritance))
        self.assertEqual(['B', 'C'],
                         get_roles_inherited_by(['B'], role_inheritance))
        self.assertEqual(['C'],
                         get_roles_inherited_by(['C'], role_inheritance))

    def test_basic(self):
        self.assertCountEqual(
            ['Foo', 'Bar'],
            get_roles_inherited_by(['Bar'], [('Bar', 'Foo')]))

    def test_not_matching(self):
        self.assertEqual(
            ['Foo'],
            get_roles_inherited_by(['Foo'], [('Bar', 'Baz')]))

        self.assertEqual(
            ['Foo'],
            get_roles_inherited_by(['Foo'], [('Bar', 'Foo')]))

    def test_recursive(self):
        expected = ['Foo', 'Bar', 'Baz']
        roles = ['Foo']

        self.assertEqual(
            expected,
            get_roles_inherited_by(
                roles,
                [('Foo', 'Bar'),
                 ('Bar', 'Baz')]))

        self.assertEqual(
            expected,
            get_roles_inherited_by(
                roles,
                [('Bar', 'Baz'),
                 ('Foo', 'Bar')]))

    def test_circular(self):
        expected = set(['Foo', 'Bar', 'Baz'])
        roles = ['Foo']
        role_inheritance = [('Foo', 'Bar'),
                            ('Bar', 'Baz'),
                            ('Baz', 'Foo')]

        self.assertEqual(
            expected,
            set(get_roles_inherited_by(roles, role_inheritance)))
