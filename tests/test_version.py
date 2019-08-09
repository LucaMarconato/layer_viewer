import layer_viewer


class TestVersion(object):

    def test_version(self):
        v = layer_viewer.__version__
        assert v == 'assert v == '0.1.1''
