from ftw.lawgiver.wdl.interfaces import IWorkflowSpecificationParser
from ftw.lawgiver.wdl.grammar import WORKFLOW_SPEC
from zope.interface import implements


class SpecificationParser(object):

    implements(IWorkflowSpecificationParser)

    def parse(self, stream):
        data = stream.read().decode('utf-8')
        ast = WORKFLOW_SPEC.parseString(data)
        assert len(ast) == 1
        spec = ast[0]

        objects = set()
        spec.recursive_collect_objects(objects)

        warnings = []
        for obj in objects:
            obj.validate(spec, warnings)

        for obj in objects:
            obj.augment(spec)

        return spec