# Code written by Jayeon Yi (stetstet)

from math import pi
import torch
import torchaudio
import scipy

def make_dht_kernel(length=255, windowtype="blackman"):
    """
    Makes Kernels for Discrete Hilbert Transform, as given by Kak (1970)
    https://ieeexplore.ieee.org/abstract/document/1449626
    """ 
    const = 2 / pi
    kernel = torch.zeros(length)
    window = torch.Tensor(scipy.signal.get_window(windowtype, length))
    for idx in range(length//2, length):
        if idx%2 == (length//2)%2:
            kernel[idx] = 0.
        else:
            kernel[idx] = 1 / (idx - length//2)
        kernel[length - idx - 1] = -kernel[idx]
    return const * kernel * window

def make_sin(length, freq, sr):
    arguments = torch.arange(0, length) * (freq * 2 * pi / sr)
    return torch.sin(arguments)

def make_cos(length, freq, sr):
    arguments = torch.arange(0, length) * (freq * 2 * pi / sr)
    return torch.cos(arguments)

class FreqShifter():
    """
    Frequency Shifter, implemented with Hilbert transform & FIR filter
    a.k.a. single-sideband modulation
    Wardle, S. (1998). A Hilbert-transformer frequency shifter for audio. 
    In First Workshop on Digital Audio Effects DAFx (pp. 25-29).

    Args:
        - dht_length: the length of DHT filter
        - window_type: the window type to use, see scipy.signals.get_window
    """
    def __init__(self, dht_length=255, window_type="blackman"):
        """
        """
        assert dht_length % 2 == 1
        self.dht_kernel = make_dht_kernel(dht_length, window_type)
        self.half_kernel_length = dht_length // 2

    def __call__(self, y, sr, up_freq):
        """
        perform frequency shifting on signal y
        Args:
            - y : the signal, (..., N)
            - sr : sample rate of y
            - up_freq : Amount to shift. nudges up if >0, down if <0
        Output:
            - torch.Tensor of shape identical to y
        """
        n_samples = y.shape[-1]
        dht = torchaudio.functional.convolve(y, self.dht_kernel, "same")
        return y * make_cos(n_samples, up_freq, sr) - dht * make_sin(n_samples, up_freq, sr)
    
if __name__ == "__main__":
    import sys
    import soundfile as sf
    infile = sys.argv[1]
    outfile = sys.argv[3]
    up_freq = float(sys.argv[2])

    shifter = FreqShifter()

    y, sr = sf.read(infile)
    y = torch.Tensor(y)
    shifted = shifter(y, sr, up_freq)
    sf.write(outfile,shifted.numpy(),sr)


