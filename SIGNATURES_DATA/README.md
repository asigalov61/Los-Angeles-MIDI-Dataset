# Los Angeles MIDI Dataset SIGNATURES DATA

***

### Los Angeles MIDI Dataset SIGNATURES DATA was collected from all compositions in the dataset and has the following format:

```[composition name/md5 hash (str), composition signature (list of lists)]```

### Each signature entry is a list of lists and has the following format:

```[[note_or_chord (0-449), count], [note_or_chord (0-449), count], [note_or_chord (0-449), count], ...]```

### note_or_chord value represent either standard note MIDI pitch (0-127), a tonal chord (128-448) or drums MIDI pitch (449-577)

### You can decode the tonal chord values by using TMIDIX module like so:

```
if 127 < note_or_chord < 449:
  tonal_chord = note_or_chord - 128
  TMIDIX.ALL_CHORDS.index(tonal_chord)
```

### Each signature pitch/chord/drum value appears in order of the composition

***

### Los Angeles MIDI Dataset SIGNATURES DATA application example can be found here:

### [Master MIDI Dataset GPU Search and Filter](https://colab.research.google.com/github/asigalov61/Los-Angeles-MIDI-Dataset/blob/main/Extras/Master_MIDI_Dataset_GPU_Search_and_Filter.ipynb)

***

### Project Los Angeles
### Tegridy Code 2024
