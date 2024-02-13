# Los Angeles MIDI Dataset CHORDS DATA

***

### Los Angeles MIDI Dataset CHORDS DATA can be found in the Los Angeles MIDI dataset archive which you can download from HUgging Face

***

### CHORDS DATA was collected from all compositions in Los Angeles MIDI Dataset by time-based chordification and has the following format:

```
[composition file name/md5 hash (str), CHORDS_DATA (list of lists]
```

### Each CHORDS DATA entry is a long list and has the following format:

```
[delta start time, (duration, patch, pitch, velocity), (duration, patch, pitch, velocity), ...]
```

#### 1) delta start time (0-255) (1000/16 ms)
#### 2) duration (0-255) (1000/16 ms)
#### 3) MIDI patch (0-128) (128 == drums)
#### 4) MIDI pitch (0-127)
#### 5) MIDI velocity (0-127)

***

### You can easily decode CHORDS DATA with the provided decoder code

***

### If you want to convert CHORDS DATA into more conventional format, please see [tegridy-tools](https://github.com/asigalov61/tegridy-tools) repo for different options to do so.

***

### Project Los Angeles
### Tegridy Code 2024
