from __future__ import print_function
import numpy as np

from .augment import Augment, Compose


__all__ = ['Flip', 'flip_x', 'flip_y', 'flip_z',
           'Transpose', 'transpose_xy', 'flip_rotate']


class Flip(Augment):
    """Random flip.

    Args:
        axis (int):
        prob (float, optional):
    """
    def __init__(self, axis, prob=0.5):
        self.axis = axis
        self.prob = np.clip(prob, 0, 1)

    def __call__(self, sample, **kwargs):
        sample = Augment.to_tensor(sample)
        # Biased coin toss.
        if np.random.rand() < self.prob:
            for k, v in sample.items():
                # Prevent potential negative stride issues by copying.
                sample[k] = np.copy(np.flip(v, self.axis))
        return Augment.sort(sample)

    def __repr__(self):
        format_string = self.__class__.__name__ + '('
        format_string += 'axis={}, '.format(self.axis)
        format_string += 'prob={:.3f}'.format(self.prob)
        format_string += ')'
        return format_string


# Predefined ``Flip``s along the x, y, and z-directions.
flip_x = Flip(axis=-1)
flip_y = Flip(axis=-2)
flip_z = Flip(axis=-3)


class Transpose(Augment):
    """Random transpose.

    Args:
        axes (list of int, optional):
        prob (float, optional):
    """
    def __init__(self, axes=None, prob=0.5):
        assert (axes is None) or (len(axes)==4)
        self.axes = axes
        self.prob = np.clip(prob, 0, 1)

    def __call__(self, sample, **kwargs):
        sample = Augment.to_tensor(sample)
        # Biased coin toss.
        if np.random.rand() < self.prob:
            for k, v in sample.items():
                # Prevent potential negative stride issues by copying.
                sample[k] = np.copy(np.transpose(v, self.axes))
        return Augment.sort(sample)

    def __repr__(self):
        format_string = self.__class__.__name__ + '('
        format_string += 'axes={}, '.format(self.axes)
        format_string += 'prob={:.3f}'.format(self.prob)
        format_string += ')'
        return format_string


# Predefined ``Transpose`` in xy-plane.
transpose_xy = Transpose(axes=[0,1,3,2])


# Random flip and rotation (by 90 degree) for anisotropic 3D data.
flip_rotate = Compose([flip_z, flip_y, flip_x, transpose_xy])


########################################################################
## Testing.
########################################################################
if __name__ == "__main__":

    sample = dict(image=np.arange(8).reshape(2,2,2))
    print('sample = {}'.format(sample))

    print(Flip(axis=-1, prob=1)(sample))
    print(Flip(axis=-2, prob=1)(sample))
    print(Flip(axis=-3, prob=1)(sample))
    print(Transpose(axes=[0,1,3,2], prob=1)(sample))

    sample = dict(image=np.arange(8).reshape(2,2,2))
    print('sample = {}'.format(sample))

    print(flip_rotate(sample))
    print(flip_rotate(sample))
    print(flip_rotate(sample))
    print(flip_rotate(sample))