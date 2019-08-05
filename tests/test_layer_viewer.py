import skimage.data

from layer_viewer import LayerViewerWidget
from layer_viewer.layers import *


def test_layer_viewer_widget(qtbot):
    # test data
    image = skimage.data.astronaut().swapaxes(0, 1)

    viewer = LayerViewerWidget()
    # viewer.show()
    viewer.setWindowTitle('LayerViewer')

    layer = MultiChannelImageLayer(name='img', data=image[...])
    viewer.add_layer(layer=layer)

    assert viewer.has_layer('img')
    assert viewer.has_layer('labels') is False

    labels = numpy.zeros(image.shape[0:2], dtype='uint8')
    label_layer = LabelLayer(name='labels', data=None)
    viewer.add_layer(layer=label_layer)
    viewer.set_data('labels', image=labels)

    assert viewer.has_layer('img')
    assert viewer.has_layer('labels')
