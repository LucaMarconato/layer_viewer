from .distinct_colors import *  # noqa: F401
from .layer_viewer_widget import LayerViewerWidget  # noqa: F401
from .layers import *  # noqa: F401
from .version import __version__  # noqa: F401

dcolors = distinct_colors

# note on the case convention all the symbols that are used by qt, for instance methods that overridden in derived
# classes, are typed using the camel case, which is the case adpoted by qt. For all the other names the PEP 8
# standard is followed
