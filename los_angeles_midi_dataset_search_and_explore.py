# -*- coding: utf-8 -*-
"""Los_Angeles_MIDI_Dataset_Search_and_Explore.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/asigalov61/Los-Angeles-MIDI-Dataset/blob/main/Los_Angeles_MIDI_Dataset_Search_and_Explore.ipynb

# Los Angeles MIDI Dataset: Search and Explore (ver. 3.0)

***

Powered by tegridy-tools: https://github.com/asigalov61/tegridy-tools

***

#### Project Los Angeles

#### Tegridy Code 2023

***

# (SETUP ENVIRONMENT)
"""

#@title Install all dependencies (run only once per session)
!git clone --depth 1 https://github.com/asigalov61/Los-Angeles-MIDI-Dataset
!pip install huggingface_hub
!pip install matplotlib
!pip install sklearn
!pip install tqdm
!apt install fluidsynth #Pip does not work for some reason. Only apt works
!pip install midi2audio

#@title Import all needed modules

print('Loading core modules...')
import os
import copy
from collections import Counter
import random
import pickle
from tqdm import tqdm
import pprint
import statistics

from joblib import Parallel, delayed
import multiprocessing

if not os.path.exists('/content/LAMD'):
    os.makedirs('/content/LAMD')

print('Loading MIDI.py module...')
os.chdir('/content/Los-Angeles-MIDI-Dataset')
import MIDI

print('Loading aux modules...')
from sklearn.metrics import pairwise_distances, pairwise
import matplotlib.pyplot as plt

from midi2audio import FluidSynth
from IPython.display import Audio, display

from huggingface_hub import hf_hub_download

from google.colab import files

os.chdir('/content/')
print('Done!')

"""# (PREP DATA)"""

# Commented out IPython magic to ensure Python compatibility.
#@title Unzip LAMDa data
# %cd /content/Los-Angeles-MIDI-Dataset/META-DATA

print('=' * 70)
print('Unzipping META-DATA...Please wait...')

!cat LAMDa_META_DATA.zip* > LAMDa_META_DATA.zip
print('=' * 70)

!unzip -j LAMDa_META_DATA.zip
print('=' * 70)

print('Done! Enjoy! :)')
print('=' * 70)
# %cd /content/

#================================================

# %cd /content/Los-Angeles-MIDI-Dataset/TOTALS

print('=' * 70)
print('Unzipping TOTALS...Please wait...')

!unzip -j LAMDa_TOTALS.zip
print('=' * 70)

print('Done! Enjoy! :)')
print('=' * 70)
# %cd /content/

#@title Load LAMDa data
print('=' * 70)
print('Loading LAMDa data...Please wait...')
print('=' * 70)
print('Loading LAMDa META-DATA...')
meta_data = pickle.load(open('/content/Los-Angeles-MIDI-Dataset/META-DATA/LAMDa_META_DATA.pickle', 'rb'))
print('Done!')
print('=' * 70)
print('Loading LAMDa TOTALS...')
totals = pickle.load(open('/content/Los-Angeles-MIDI-Dataset/TOTALS/LAMDa_TOTALS.pickle', 'rb'))
print('Done!')
print('=' * 70)
print('Enjoy!')
print('=' * 70)

"""# (PREP MIDI DATASET)"""

#@title Download the dataset
print('=' * 70)
print('Downloading Los Angeles MIDI Dataset...Please wait...')
print('=' * 70)

hf_hub_download(repo_id='projectlosangeles/Los-Angeles-MIDI-Dataset',
                filename='Los-Angeles-MIDI-Dataset-Ver-3-0-CC-BY-NC-SA.zip',
                repo_type="dataset",
                local_dir='/content/LAMD',
                local_dir_use_symlinks=False)
print('=' * 70)
print('Done! Enjoy! :)')
print('=' * 70)

# Commented out IPython magic to ensure Python compatibility.
#@title Unzip the dataset
# %cd /content/LAMD

print('=' * 70)
print('Unzipping Los Angeles MIDI Dataset...Please wait...')
!unzip 'Los-Angeles-MIDI-Dataset-Ver-3-0-CC-BY-NC-SA.zip'
print('=' * 70)

print('Done! Enjoy! :)')
print('=' * 70)
# %cd /content/

#@title Create dataset files list
print('=' * 70)
print('Creating dataset files list...')
dataset_addr = "/content/LAMD/MIDIs"

# os.chdir(dataset_addr)
filez = list()
for (dirpath, dirnames, filenames) in os.walk(dataset_addr):
    filez += [os.path.join(dirpath, file) for file in filenames]

if filez == []:
    print('Could not find any MIDI files. Please check Dataset dir...')
    print('=' * 70)

print('=' * 70)
print('Randomizing file list...')
random.shuffle(filez)
print('=' * 70)

LAMD_files_list = []

for f in tqdm(filez):
  LAMD_files_list.append([f.split('/')[-1].split('.mid')[0], f])
print('Done!')
print('=' * 70)

"""# (PLOT TOTALS)"""

#@title Plot totals from MIDI matrixes (legacy)

cos_sim = pairwise.cosine_similarity(
      totals[0][0][4]
  )
plt.figure(figsize=(8, 8))
plt.imshow(cos_sim, cmap="inferno", interpolation="none")
im_ratio = 1
plt.colorbar(fraction=0.046 * im_ratio, pad=0.04)
plt.title('Times')
plt.xlabel("Position")
plt.ylabel("Position")
plt.tight_layout()
plt.plot()

cos_sim = pairwise.cosine_similarity(
      totals[0][0][5]
  )
plt.figure(figsize=(8, 8))
plt.imshow(cos_sim, cmap="inferno", interpolation="none")
im_ratio = 1
plt.colorbar(fraction=0.046 * im_ratio, pad=0.04)
plt.title('Durations')
plt.xlabel("Position")
plt.ylabel("Position")
plt.tight_layout()
plt.plot()

cos_sim = pairwise.cosine_similarity(
      totals[0][0][6]
  )
plt.figure(figsize=(8, 8))
plt.imshow(cos_sim, cmap="inferno", interpolation="none")
im_ratio = 1
plt.colorbar(fraction=0.046 * im_ratio, pad=0.04)
plt.title('Channels')
plt.xlabel("Position")
plt.ylabel("Position")
plt.tight_layout()
plt.plot()

cos_sim = pairwise.cosine_similarity(
      totals[0][0][7]
  )
plt.figure(figsize=(8, 8))
plt.imshow(cos_sim, cmap="inferno", interpolation="none")
im_ratio = 1
plt.colorbar(fraction=0.046 * im_ratio, pad=0.04)
plt.title('Instruments')
plt.xlabel("Position")
plt.ylabel("Position")
plt.tight_layout()
plt.plot()

cos_sim = pairwise.cosine_similarity(
      totals[0][0][8]
  )
plt.figure(figsize=(8, 8))
plt.imshow(cos_sim, cmap="inferno", interpolation="none")
im_ratio = 1
plt.colorbar(fraction=0.046 * im_ratio, pad=0.04)
plt.title('Pitches')
plt.xlabel("Position")
plt.ylabel("Position")
plt.tight_layout()
plt.plot()

cos_sim = pairwise.cosine_similarity(
      totals[0][0][9]
  )
plt.figure(figsize=(8, 8))
plt.imshow(cos_sim, cmap="inferno", interpolation="none")
im_ratio = 1
plt.colorbar(fraction=0.046 * im_ratio, pad=0.04)
plt.title('Velocities')
plt.xlabel("Position")
plt.ylabel("Position")
plt.tight_layout()
plt.plot()

#@title Plot totals from MIDI metadata

#===============================================================================

pitches_counts_totals = [0] * 128

for m in tqdm(meta_data):
  for mm in m[1][10][1]:
    if mm[0] < 128:
      pitches_counts_totals[mm[0]] += mm[1]

y = range(128)
plt.figure(figsize=(8, 8))
plt.plot(y, pitches_counts_totals)

plt.title('MIDI Instruments Pitches')
plt.xlabel("Pitch")
plt.ylabel("Count")
plt.tight_layout()
plt.plot()

sim_mat = [ [0]*128 for i in range(128)]
x = 0

for p in pitches_counts_totals:
  y = 0
  for pp in pitches_counts_totals:

    sim_mat[x][y] = min(10, (p / pp))
    y += 1

  x += 1

cos_sim = pairwise.cosine_similarity(
      sim_mat
  )
plt.figure(figsize=(8, 8))
plt.imshow(sim_mat, cmap="inferno", interpolation="none")
im_ratio = 1
plt.colorbar(fraction=0.046 * im_ratio, pad=0.04)
plt.title('MIDI Drums Pitches')
plt.xlabel("Pitch")
plt.ylabel("Count")
plt.tight_layout()
plt.plot()

#===============================================================================

pitches_counts_totals = [1] * 128


for m in tqdm(meta_data):
  for mm in m[1][10][1]:
    if mm[0] > 128:
      pitches_counts_totals[mm[0] % 128] += mm[1]

y = range(128)
plt.figure(figsize=(8, 8))
plt.plot(y, pitches_counts_totals)

plt.title('MIDI Drums Pitches')
plt.xlabel("Pitch")
plt.ylabel("Count")
plt.tight_layout()
plt.plot()

sim_mat = [ [0]*128 for i in range(128)]
x = 0

for p in pitches_counts_totals:
  y = 0
  for pp in pitches_counts_totals:

    sim_mat[x][y] = min(10, (p / pp))
    y += 1

  x += 1

cos_sim = pairwise.cosine_similarity(
      sim_mat
  )
plt.figure(figsize=(8, 8))
plt.imshow(sim_mat, cmap="inferno", interpolation="none")
im_ratio = 1
plt.colorbar(fraction=0.046 * im_ratio, pad=0.04)
plt.title('MIDI Drums Pitches')
plt.xlabel("Pitch")
plt.ylabel("Count")
plt.tight_layout()
plt.plot()

#===============================================================================

patches_counts_totals = [0] * 256


for m in tqdm(meta_data):
  for mm in m[1][12][1]:
    patches_counts_totals[mm[0]] += mm[1]


y = range(128)
plt.figure(figsize=(8, 8))
plt.plot(y, patches_counts_totals[:128])

plt.title('MIDI Patches')
plt.xlabel("Patch")
plt.ylabel('Count')
plt.tight_layout()
plt.plot()

"""# (LOAD SOURCE MIDI)"""

#@title Load source MIDI

full_path_to_source_MIDI = "/content/Los-Angeles-MIDI-Dataset/Come-To-My-Window-Modified-Sample-MIDI.mid" #@param {type:"string"}
render_MIDI_to_audio = False #@param {type:"boolean"}

#=================================================================================

f = full_path_to_source_MIDI

print('=' * 70)
print('Loading MIDI file...')

#==================================================

score = MIDI.midi2score(open(f, 'rb').read())

events_matrix = []

track_count = 0

for s in score:

    if track_count > 0:
        track = s
        track.sort(key=lambda x: x[1])
        events_matrix.extend(track)
    else:
        midi_ticks = s

    track_count += 1

events_matrix.sort(key=lambda x: x[1])

mult_pitches_counts = []

for i in range(-6, 6):

  events_matrix1 = []

  for e in events_matrix:

    ev = copy.deepcopy(e)

    if e[0] == 'note':
        if e[3] == 9:
            ev[4] = ((e[4] % 128) + 128)
        else:
          ev[4] = ((e[4] % 128) + i)

        events_matrix1.append(ev)

  pitches_counts = [[y[0],y[1]] for y in Counter([y[4] for y in events_matrix1 if y[0] == 'note']).most_common()]
  pitches_counts.sort(key=lambda x: x[0], reverse=True)

  mult_pitches_counts.append(pitches_counts)

patches_list = sorted(list(set([y[3] for y in events_matrix if y[0] == 'patch_change'])))


#==================================================

ms_score = MIDI.midi2ms_score(open(f, 'rb').read())

ms_events_matrix = []

itrack1 = 1

while itrack1 < len(ms_score):
    for event in ms_score[itrack1]:
        if event[0] == 'note':
            ms_events_matrix.append(event)
    itrack1 += 1

ms_events_matrix.sort(key=lambda x: x[1])


chords = []
pe = ms_events_matrix[0]
cho = []
for e in ms_events_matrix:
    if (e[1] - pe[1]) == 0:
      if e[3] != 9:
        if (e[4] % 12) not in cho:
          cho.append(e[4] % 12)
    else:
      if len(cho) > 0:
        chords.append(sorted(cho))
      cho = []
      if e[3] != 9:
        if (e[4] % 12) not in cho:
          cho.append(e[4] % 12)

    pe = e

if len(cho) > 0:
    chords.append(sorted(cho))

ms_chords_counts = sorted([[list(key), val] for key,val in Counter([tuple(c) for c in chords if len(c) > 1]).most_common()], reverse=True, key = lambda x: x[1])

times = []
pt = ms_events_matrix[0][1]
start = True
for e in ms_events_matrix:
    if (e[1]-pt) != 0 or start == True:
        times.append((e[1]-pt))
        start = False
    pt = e[1]

durs = [e[2] for e in ms_events_matrix]
vels = [e[5] for e in ms_events_matrix]

avg_time = int(sum(times) / len(times))
avg_dur = int(sum(durs) / len(durs))

mode_time = statistics.mode(times)
mode_dur = statistics.mode(durs)

median_time = int(statistics.median(times))
median_dur = int(statistics.median(durs))

#==================================================

print('=' * 70)
print('Done!')
print('=' * 70)

#============================================
# MIDI rendering code
#============================================

print('Rendering source MIDI...')
print('=' * 70)

ms_score = MIDI.midi2ms_score(open(f, 'rb').read())

itrack = 1
song_f = []

while itrack < len(ms_score):
    for event in ms_score[itrack]:
        if event[0] == 'note':
            song_f.append(event)
    itrack += 1

song_f.sort(key=lambda x: x[1])

fname = f.split('.mid')[0]

x = []
y =[]
c = []

colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'pink', 'orange', 'purple', 'gray', 'white', 'gold', 'silver', 'aqua', 'azure', 'bisque', 'coral']

for s in song_f:
  x.append(s[1] / 1000)
  y.append(s[4])
  c.append(colors[s[3]])

if render_MIDI_to_audio:
  FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
  display(Audio(str(fname + '.wav'), rate=16000))

plt.figure(figsize=(14,5))
ax=plt.axes(title=fname)
ax.set_facecolor('black')

plt.scatter(x,y, c=c)
plt.xlabel("Time")
plt.ylabel("Pitch")
plt.show()

"""# (SEARCH AND EXPLORE)"""

#@title MIDI Pitches Search

#@markdown NOTE: You can stop the search at any time to render partial results

#@markdown Match ratio control option

maximum_match_ratio_to_search_for = 1 #@param {type:"slider", min:0, max:1, step:0.01}

#@markdown MIDI pitches search options

pitches_counts_cutoff_threshold_ratio = 0 #@param {type:"slider", min:0, max:1, step:0.05}
search_transposed_pitches = False #@param {type:"boolean"}
skip_exact_matches = False #@param {type:"boolean"}

#@markdown Additional search options

add_pitches_counts_ratios = False #@param {type:"boolean"}
add_timings_ratios = False #@param {type:"boolean"}
add_durations_ratios = False #@param {type:"boolean"}

#@markdown Other options

render_MIDI_to_audio = False #@param {type:"boolean"}
download_MIDI = False #@param {type:"boolean"}

print('=' * 70)
print('MIDI Pitches Search')
print('=' * 70)

final_ratios = []

for d in tqdm(meta_data):

  try:
    p_counts = d[1][10][1]
    p_counts.sort(reverse = True, key = lambda x: x[1])
    max_p_count = p_counts[0][1]
    trimmed_p_counts = [y for y in p_counts if y[1] >= (max_p_count * pitches_counts_cutoff_threshold_ratio)]
    total_p_counts = sum([y[1] for y in trimmed_p_counts])

    if search_transposed_pitches:
      search_pitches = mult_pitches_counts
    else:
      search_pitches = [mult_pitches_counts[6]]

    #===================================================

    ratios_list = []

    #===================================================

    atrat = [0]

    if add_timings_ratios:

      source_times = [avg_time,
                      median_time,
                      mode_time]

      match_times = meta_data[0][1][3][1]

      times_ratios = []

      for i in range(len(source_times)):
        maxtratio = max(source_times[i], match_times[i])
        mintratio = min(source_times[i], match_times[i])
        times_ratios.append(mintratio / maxtratio)

      avg_times_ratio = sum(times_ratios) / len(times_ratios)

      atrat[0] = avg_times_ratio

    #===================================================

    adrat = [0]

    if add_durations_ratios:

      source_durs = [avg_dur,
                      median_dur,
                      mode_dur]

      match_durs = meta_data[0][1][4][1]

      durs_ratios = []

      for i in range(len(source_durs)):
        maxtratio = max(source_durs[i], match_durs[i])
        mintratio = min(source_durs[i], match_durs[i])
        durs_ratios.append(mintratio / maxtratio)

      avg_durs_ratio = sum(durs_ratios) / len(durs_ratios)

      adrat[0] = avg_durs_ratio

    #===================================================

    for m in search_pitches:

      sprat = []

      m.sort(reverse = True, key = lambda x: x[1])
      max_pitches_count = m[0][1]
      trimmed_pitches_counts = [y for y in m if y[1] >= (max_pitches_count * pitches_counts_cutoff_threshold_ratio)]
      total_pitches_counts = sum([y[1] for y in trimmed_pitches_counts])

      same_pitches = set([T[0] for T in trimmed_p_counts]) & set([m[0] for m in trimmed_pitches_counts])
      num_same_pitches = len(same_pitches)

      if num_same_pitches == len(trimmed_pitches_counts):
        same_pitches_ratio = (num_same_pitches / len(trimmed_p_counts))
      else:
        same_pitches_ratio = (num_same_pitches / max(len(trimmed_p_counts), len(trimmed_pitches_counts)))

      if skip_exact_matches:
        if same_pitches_ratio == 1:
          same_pitches_ratio = 0

      sprat.append(same_pitches_ratio)

      #===================================================

      spcrat = [0]

      if add_pitches_counts_ratios:

        same_trimmed_p_counts = sorted([T for T in trimmed_p_counts if T[0] in same_pitches], reverse = True)
        same_trimmed_pitches_counts = sorted([T for T in trimmed_pitches_counts if T[0] in same_pitches], reverse = True)

        same_trimmed_p_counts_ratios = [[s[0], s[1] / total_p_counts] for s in same_trimmed_p_counts]
        same_trimmed_pitches_counts_ratios = [[s[0], s[1] / total_pitches_counts] for s in same_trimmed_pitches_counts]

        same_pitches_counts_ratios = []

        for i in range(len(same_trimmed_p_counts_ratios)):
          mincratio = min(same_trimmed_p_counts_ratios[i][1], same_trimmed_pitches_counts_ratios[i][1])
          maxcratio = max(same_trimmed_p_counts_ratios[i][1], same_trimmed_pitches_counts_ratios[i][1])
          same_pitches_counts_ratios.append([same_trimmed_p_counts_ratios[i][0], mincratio / maxcratio])

        same_counts_ratios = [s[1] for s in same_pitches_counts_ratios]

        if len(same_counts_ratios) > 0:
          avg_same_pitches_counts_ratio = sum(same_counts_ratios) / len(same_counts_ratios)
        else:
          avg_same_pitches_counts_ratio = 0

        spcrat[0] = avg_same_pitches_counts_ratio

      #===================================================

      r_list = [sprat[0]]

      if add_pitches_counts_ratios:
        r_list.append(spcrat[0])

      if add_timings_ratios:
        r_list.append(atrat[0])

      if add_durations_ratios:
        r_list.append(adrat[0])

      ratios_list.append(r_list)

    #===================================================

    avg_ratios_list = []

    for r in ratios_list:
      avg_ratios_list.append(sum(r) / len(r))

    #===================================================

    final_ratio = max(avg_ratios_list)

    if final_ratio > maximum_match_ratio_to_search_for:
        final_ratio = 0

    final_ratios.append(final_ratio)

    #===================================================

  except KeyboardInterrupt:
    break

  except Exception as e:
    print('WARNING !!!')
    print('=' * 70)
    print('Error detected:', e)
    final_ratios.append(0)
    print('=' * 70)
    break

max_ratio = max(final_ratios)
max_ratio_index = final_ratios.index(max_ratio)

print('FOUND')
print('=' * 70)
print('Match ratio', max_ratio)
print('MIDI file name', meta_data[max_ratio_index][0])
print('=' * 70)
pprint.pprint(['Sample metadata entries', meta_data[max_ratio_index][1][:8]], compact = True)
print('=' * 70)

#============================================
# MIDI rendering code
#============================================

print('Rendering source MIDI...')
print('=' * 70)

fn = meta_data[max_ratio_index][0]
fn_idx = [y[0] for y in LAMD_files_list].index(fn)

f = LAMD_files_list[fn_idx][1]

ms_score = MIDI.midi2ms_score(open(f, 'rb').read())

itrack = 1
song_f = []

while itrack < len(ms_score):
    for event in ms_score[itrack]:
        if event[0] == 'note':
            song_f.append(event)
    itrack += 1

song_f.sort(key=lambda x: x[1])

fname = f.split('.mid')[0]

x = []
y =[]
c = []

colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'pink', 'orange', 'purple', 'gray', 'white', 'gold', 'silver', 'aqua', 'azure', 'bisque', 'coral']

for s in song_f:
  x.append(s[1] / 1000)
  y.append(s[4])
  c.append(colors[s[3]])

if render_MIDI_to_audio:
  FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
  display(Audio(str(fname + '.wav'), rate=16000))

plt.figure(figsize=(14,5))
ax=plt.axes(title=fname)
ax.set_facecolor('black')

plt.scatter(x,y, c=c)
plt.xlabel("Time")
plt.ylabel("Pitch")
plt.show()

#==============================================

if download_MIDI:
  print('=' * 70)
  print('Downloading MIDI file', str(fn) + '.mid')
  files.download(f)
  print('=' * 70)

#@title MIDI Chords Search

#@markdown NOTE: You can stop the search at any time to render partial results

maximum_match_ratio_to_search_for = 1 #@param {type:"slider", min:0, max:1, step:0.01}
chords_counts_cutoff_threshold_ratio = 0 #@param {type:"slider", min:0, max:1, step:0.05}
skip_exact_matches = False #@param {type:"boolean"}
render_MIDI_to_audio = False #@param {type:"boolean"}
download_MIDI = False #@param {type:"boolean"}

print('=' * 70)
print('MIDI Chords Search')
print('=' * 70)

ratios = []

for d in tqdm(meta_data):

  try:

    c_counts = d[1][8][1]
    if len(c_counts) == 0:
      c_counts = copy.deepcopy([[[0, 0], 0]])

    c_counts.sort(reverse = True, key = lambda x: x[0][1])
    max_c_count = c_counts[0][1]
    trimmed_c_counts = [y for y in c_counts if y[1] >= (max_c_count * chords_counts_cutoff_threshold_ratio)]
    trimmed_c_counts.sort(reverse = True, key = lambda x: x[1])

    max_chords_count = ms_chords_counts[0][1]
    trimmed_chords_counts = [y for y in ms_chords_counts if y[1] >= (max_chords_count * chords_counts_cutoff_threshold_ratio)]

    num_same_chords = len(set([tuple(T[0]) for T in trimmed_c_counts]) & set([tuple(t[0]) for t in trimmed_chords_counts]))

    if num_same_chords == len(trimmed_chords_counts):
      same_chords_ratio = (num_same_chords / len(trimmed_c_counts))
    else:
      same_chords_ratio = (num_same_chords / max(len(trimmed_c_counts), len(trimmed_chords_counts)))

    if skip_exact_matches:
      if same_chords_ratio == 1:
        same_chords_ratio = 0

    if same_chords_ratio > maximum_match_ratio_to_search_for:
      same_chords_ratio = 0

    ratios.append(same_chords_ratio)

  except KeyboardInterrupt:
    break

  except Exception as e:
    print('WARNING !!!')
    print('=' * 70)
    print('Error detected:', e)
    ratios.append(0)
    print('=' * 70)
    continue

max_ratio = max(ratios)
max_ratio_index = ratios.index(max(ratios))

print('FOUND')
print('=' * 70)
print('Match ratio', max_ratio)
print('MIDI file name', meta_data[max_ratio_index][0])
print('=' * 70)
pprint.pprint(['Sample metadata entries', meta_data[max_ratio_index][1][:8]], compact = True)
print('=' * 70)

#============================================
# MIDI rendering code
#============================================

print('Rendering source MIDI...')
print('=' * 70)

fn = meta_data[max_ratio_index][0]
fn_idx = [y[0] for y in LAMD_files_list].index(fn)

f = LAMD_files_list[fn_idx][1]

ms_score = MIDI.midi2ms_score(open(f, 'rb').read())

itrack = 1
song_f = []

while itrack < len(ms_score):
    for event in ms_score[itrack]:
        if event[0] == 'note':
            song_f.append(event)
    itrack += 1

song_f.sort(key=lambda x: x[1])

fname = f.split('.mid')[0]

x = []
y =[]
c = []

colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'pink', 'orange', 'purple', 'gray', 'white', 'gold', 'silver', 'aqua', 'azure', 'bisque', 'coral']

for s in song_f:
  x.append(s[1] / 1000)
  y.append(s[4])
  c.append(colors[s[3]])

if render_MIDI_to_audio:
  FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
  display(Audio(str(fname + '.wav'), rate=16000))

plt.figure(figsize=(14,5))
ax=plt.axes(title=fname)
ax.set_facecolor('black')

plt.scatter(x,y, c=c)
plt.xlabel("Time")
plt.ylabel("Pitch")
plt.show()

#==============================================

if download_MIDI:
  print('=' * 70)
  print('Downloading MIDI file', str(fn) + '.mid')
  files.download(f)
  print('=' * 70)

#@title MIDI Patches Search

#@markdown NOTE: You can stop the search at any time to render partial results

maximum_match_ratio_to_search_for = 1 #@param {type:"slider", min:0, max:1, step:0.01}
skip_exact_matches = False #@param {type:"boolean"}
render_MIDI_to_audio = False #@param {type:"boolean"}
download_MIDI = False #@param {type:"boolean"}

print('=' * 70)
print('MIDI Patches Search')
print('=' * 70)

ratios = []

for d in tqdm(meta_data):

  try:

    p_list= d[1][11][1]

    num_same_patches = len(set(p_list) & set(patches_list))

    if len(set(p_list + patches_list)) > 0:

      if num_same_patches == len(patches_list):
        same_patches_ratio = num_same_patches / len(p_list)
      else:
        same_patches_ratio = num_same_patches / max(len(p_list), len(patches_list))

    else:
      same_patches_ratio = 0

    if skip_exact_matches:
      if same_patches_ratio == 1:
        same_patches_ratio = 0

    if same_patches_ratio > maximum_match_ratio_to_search_for:
      same_patches_ratio = 0

    ratios.append(same_patches_ratio)

  except KeyboardInterrupt:
    break

  except Exception as e:
    print('WARNING !!!')
    print('=' * 70)
    print('Error detected:', e)
    ratios.append(0)
    print('=' * 70)
    continue

max_ratio = max(ratios)
max_ratio_index = ratios.index(max(ratios))

print('FOUND')
print('=' * 70)
print('Match ratio', max_ratio)
print('MIDI file name', meta_data[max_ratio_index][0])
print('=' * 70)
print('Found MIDI patches list', meta_data[max_ratio_index][1][12][1])
print('=' * 70)

#============================================
# MIDI rendering code
#============================================

print('Rendering source MIDI...')
print('=' * 70)

fn = meta_data[max_ratio_index][0]
fn_idx = [y[0] for y in LAMD_files_list].index(fn)

f = LAMD_files_list[fn_idx][1]

ms_score = MIDI.midi2ms_score(open(f, 'rb').read())

itrack = 1
song_f = []

while itrack < len(ms_score):
    for event in ms_score[itrack]:
        if event[0] == 'note':
            song_f.append(event)
    itrack += 1

song_f.sort(key=lambda x: x[1])

fname = f.split('.mid')[0]

x = []
y =[]
c = []

colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'pink', 'orange', 'purple', 'gray', 'white', 'gold', 'silver', 'aqua', 'azure', 'bisque', 'coral']

for s in song_f:
  x.append(s[1] / 1000)
  y.append(s[4])
  c.append(colors[s[3]])

if render_MIDI_to_audio:
  FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
  display(Audio(str(fname + '.wav'), rate=16000))

plt.figure(figsize=(14,5))
ax=plt.axes(title=fname)
ax.set_facecolor('black')

plt.scatter(x,y, c=c)
plt.xlabel("Time")
plt.ylabel("Pitch")
plt.show()

#==============================================

if download_MIDI:
  print('=' * 70)
  print('Downloading MIDI file', str(fn) + '.mid')
  files.download(f)
  print('=' * 70)

#@title Metadata Search

#@markdown You can search the metadata by search query or by MIDI md5 hash file name

search_query = "Come To My Window" #@param {type:"string"}
md5_hash_MIDI_file_name = "d9a7e1c6a375b8e560155a5977fc10f8" #@param {type:"string"}
case_sensitive_search = False #@param {type:"boolean"}

fields_to_search = ['track_name',
                    'text_event',
                    'lyric',
                    'copyright_text_event',
                    'marker',
                    'text_event_08',
                    'text_event_09',
                    'text_event_0a',
                    'text_event_0b',
                    'text_event_0c',
                    'text_event_0d',
                    'text_event_0e',
                    'text_event_0f',
                    ]

print('=' * 70)
print('Los Angeles MIDI Dataset Metadata Search')
print('=' * 70)
print('Searching...')
print('=' * 70)

if md5_hash_MIDI_file_name != '':
  for d in tqdm(meta_data):
    try:
      if d[0] == md5_hash_MIDI_file_name:
        print('Found!')
        print('=' * 70)
        print('Metadata index:', meta_data.index(d))
        print('MIDI file name:', meta_data[meta_data.index(d)][0])
        print('-' * 70)
        pprint.pprint(['Result:', d[1][:16]], compact = True)
        print('=' * 70)
        break

    except KeyboardInterrupt:
      print('Ending search...')
      print('=' * 70)
      break

    except Exception as e:
      print('WARNING !!!')
      print('=' * 70)
      print('Error detected:', e)
      print('=' * 70)
      continue

  if d[0] != md5_hash_MIDI_file_name:
    print('Not found!')
    print('=' * 70)
    print('md5 hash was not found!')
    print('Ending search...')
    print('=' * 70)

else:
  for d in tqdm(meta_data):
    try:
      for dd in d[1]:
        if dd[0] in fields_to_search:
          if case_sensitive_search:
            if str(search_query) in str(dd[2]):
              print('Found!')
              print('=' * 70)
              print('Metadata index:', meta_data.index(d))
              print('MIDI file name:', meta_data[meta_data.index(d)][0])
              print('-' * 70)
              pprint.pprint(['Result:', dd[2][:16]], compact = True)
              print('=' * 70)

          else:
            if str(search_query).lower() in str(dd[2]).lower():
              print('Found!')
              print('=' * 70)
              print('Metadata index:', meta_data.index(d))
              print('MIDI file name:', meta_data[meta_data.index(d)][0])
              print('-' * 70)
              pprint.pprint(['Result:', dd[2][:16]], compact = True)
              print('=' * 70)

    except KeyboardInterrupt:
      print('Ending search...')
      print('=' * 70)
      break

    except:
      print('Ending search...')
      print('=' * 70)
      break

"""# (MIDI FILE PLAYER)"""

#@title MIDI file player

#@markdown NOTE: You can use md5 hash file name or full MIDI file path to play it

md5_hash_MIDI_file_name = "d9a7e1c6a375b8e560155a5977fc10f8" #@param {type:"string"}
full_path_to_MIDI = "/content/Los-Angeles-MIDI-Dataset/Come-To-My-Window-Modified-Sample-MIDI.mid" #@param {type:"string"}
render_MIDI_to_audio = False #@param {type:"boolean"}
download_MIDI = False #@param {type:"boolean"}

#============================================
# MIDI rendering code
#============================================

print('=' * 70)
print('MIDI file player')
print('=' * 70)

try:

  if os.path.exists(full_path_to_MIDI):
    f = full_path_to_MIDI
    print('Using full path to MIDI')

  else:
    fn = md5_hash_MIDI_file_name
    fn_idx = [y[0] for y in LAMD_files_list].index(fn)
    f = LAMD_files_list[fn_idx][1]

    print('Using md5 hash filename')

  print('=' * 70)
  print('Rendering MIDI...')
  print('=' * 70)

  ms_score = MIDI.midi2ms_score(open(f, 'rb').read())

  itrack = 1
  song_f = []

  while itrack < len(ms_score):
      for event in ms_score[itrack]:
          if event[0] == 'note':
              song_f.append(event)
      itrack += 1

  song_f.sort(key=lambda x: x[1])

  fname = f.split('.mid')[0]

  x = []
  y =[]
  c = []

  colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'pink', 'orange', 'purple', 'gray', 'white', 'gold', 'silver', 'aqua', 'azure', 'bisque', 'coral']

  for s in song_f:
    x.append(s[1] / 1000)
    y.append(s[4])
    c.append(colors[s[3]])

  if render_MIDI_to_audio:
    FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
    display(Audio(str(fname + '.wav'), rate=16000))

  plt.figure(figsize=(14,5))
  ax=plt.axes(title=fname)
  ax.set_facecolor('black')

  plt.scatter(x,y, c=c)
  plt.xlabel("Time")
  plt.ylabel("Pitch")
  plt.show()

  #==============================================

  if download_MIDI:
    print('=' * 70)
    print('Downloading MIDI file', str(fn) + '.mid')
    files.download(f)
    print('=' * 70)

except:
  print('File not found!!!')
  print('Check the filename!')
  print('=' * 70)

"""# (COLAB MIDI FILES LOCATOR/DOWNLOADER)"""

#@title Loacate and/or download desired MIDI files by MIDI md5 hash file names

MIDI_md5_hash_file_name_1 = "d9a7e1c6a375b8e560155a5977fc10f8" #@param {type:"string"}
MIDI_md5_hash_file_name_2 = "" #@param {type:"string"}
MIDI_md5_hash_file_name_3 = "" #@param {type:"string"}
MIDI_md5_hash_file_name_4 = "" #@param {type:"string"}
MIDI_md5_hash_file_name_5 = "" #@param {type:"string"}
download_located_files = False #@param {type:"boolean"}

print('=' * 70)
print('MIDI files locator and downloader')
print('=' * 70)

md5_list = []

if MIDI_md5_hash_file_name_1 != '':
  md5_list.append(MIDI_md5_hash_file_name_1)

if MIDI_md5_hash_file_name_2 != '':
  md5_list.append(MIDI_md5_hash_file_name_2)

if MIDI_md5_hash_file_name_3 != '':
  md5_list.append(MIDI_md5_hash_file_name_3)

if MIDI_md5_hash_file_name_4 != '':
  md5_list.append(MIDI_md5_hash_file_name_4)

if MIDI_md5_hash_file_name_5 != '':
  md5_list.append(MIDI_md5_hash_file_name_5)

if len(md5_list) > 0:
  for m in md5_list:
    try:

      fn = m
      fn_idx = [y[0] for y in LAMD_files_list].index(fn)
      f = LAMD_files_list[fn_idx][1]

      print('Found md5 hash file name', m)

      location_str = ''

      fl = f.split('/')
      for fa in fl[:-1]:
        if fa != '' and fa != 'content':
          location_str += '/'
          location_str += str(fa)

      print('Colab location/folder', location_str)

      if download_located_files:
        print('Downloading MIDI file', str(m) + '.mid')
        files.download(f)

      print('=' * 70)

    except:
      print('md5 hash file name', m, 'not found!!!')
      print('Check the file name!')
      print('=' * 70)
      continue

else:
  print('No md5 hash file names were specified!')
  print('Check input!')
  print('=' * 70)

"""# (CUSTOM ANALYSIS TEMPLATE)"""

#@title Los Angeles MIDI Dataset Reader

print('=' * 70)
print('Los Angeles MIDI Dataset Reader')
print('=' * 70)
print('Starting up...')
print('=' * 70)

###########

print('Loading MIDI files...')
print('This may take a while on a large dataset in particular.')

dataset_addr = "/content/LAMD/MIDIs"

# os.chdir(dataset_addr)
filez = list()
for (dirpath, dirnames, filenames) in os.walk(dataset_addr):
    filez += [os.path.join(dirpath, file) for file in filenames]

if filez == []:
    print('Could not find any MIDI files. Please check Dataset dir...')
    print('=' * 70)

print('=' * 70)
print('Randomizing file list...')
random.shuffle(filez)
print('=' * 70)

###########

START_FILE_NUMBER = 0
LAST_SAVED_BATCH_COUNT = 0

input_files_count = START_FILE_NUMBER
files_count = LAST_SAVED_BATCH_COUNT

stats = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

print('Reading MIDI files. Please wait...')
print('=' * 70)

for f in tqdm(filez[START_FILE_NUMBER:]):
    try:
        input_files_count += 1

        fn = os.path.basename(f)
        fn1 = fn.split('.mid')[0]

        #=======================================================
        # START PROCESSING
        #=======================================================

        # Convering MIDI to score with MIDI.py module
        score = MIDI.midi2score(open(f, 'rb').read())

        events_matrix = []

        itrack = 1

        while itrack < len(score):
            for event in score[itrack]:
              events_matrix.append(event)
            itrack += 1

        # Sorting...
        events_matrix.sort(key=lambda x: x[1])

        if len(events_matrix) > 0:

          #=======================================================
          # INSERT YOUR CUSTOM ANAYLSIS CODE RIGHT HERE
          #=======================================================

          # Processed files counter
          files_count += 1

          # Saving every 5000 processed files
          if files_count % 10000 == 0:
            print('=' * 70)
            print('Processed so far:', files_count, 'out of', input_files_count, '===', files_count / input_files_count, 'good files ratio')
            print('=' * 70)

    except KeyboardInterrupt:
        print('Saving current progress and quitting...')
        break

    except Exception as ex:
        print('WARNING !!!')
        print('=' * 70)
        print('Bad MIDI:', f)
        print('Error detected:', ex)
        print('=' * 70)
        continue

print('=' * 70)
print('Final files counts:', files_count, 'out of', input_files_count, '===', files_count / input_files_count, 'good files ratio')
print('=' * 70)

print('Resulting Stats:')
print('=' * 70)
print('Total good processed MIDI files:', files_count)
print('=' * 70)
print('Done!')
print('=' * 70)

"""# Congrats! You did it! :)"""