# Frequency Shifter

References:

[Wardle, Scott. "A Hilbert-transformer frequency shifter for audio." First Workshop on Digital Audio Effects DAFx. 1998.](https://www.mikrocontroller.net/attachment/33905/Audio_Hilbert_WAR19.pdf)

## How to test:

```
python freqshifter.py (file) (frequency) (outputfile)
```

## Note

It is very common to have pre-filtering so that aliasing does not occur.
However there are no plans to implement pre-filtering for this frequency shifter.
We may choose to implement a "brickwall" LPF or HPF later, but that's a completely different story.