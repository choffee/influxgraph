import unittest
from timeit import timeit
from pprint import pprint

class TemplatesPerfTestCase(unittest.TestCase):
    template_stmt = """
for serie in series:
    for split_path in get_series_with_tags(serie.split(','), fields, templates):
        pass
    """
    timeit_setup = """from string import ascii_letters
from random import choice
from influxgraph.templates import parse_influxdb_graphite_templates
measurements = [u''.join([choice(ascii_letters) for _ in range(10)]) for _ in range(500)]
series = [u'%s,a=1,b=2,c=3,d=4,e=6,f=7,g=8,m=9,n=10,j=11' % (m,) for m in measurements]
fields = {m: [u'f1', u'f2', u'f3', u'f4', u'f5', u'f6', u'f7', u'f8', u'f9', u'f10'] for m in measurements}
templates = parse_influxdb_graphite_templates(["a.b.c.d.e.f.g.m.n.j.measurement.field* env=int,region=the_west"])
    """

    def test_python_template(self):
        setup = '\n'.join(["from influxgraph.templates import get_series_with_tags",
                           self.timeit_setup])
        parse_time = timeit(
            stmt=self.template_stmt, setup=setup, number=100)
        pprint("Python template parse time is %s" % (parse_time,))

    def test_cython_template(self):
        setup = '\n'.join(["""
try:
    from influxgraph.ext.templates import get_series_with_tags
except ImportError:
    from influxgraph.templates import get_series_with_tags
""",
                           self.timeit_setup])
        parse_time = timeit(
            stmt=self.template_stmt, setup=setup, number=100)
        pprint("Cython template parse time is %s" % (parse_time,))
