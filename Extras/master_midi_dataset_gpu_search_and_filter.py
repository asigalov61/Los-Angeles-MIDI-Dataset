# -*- coding: utf-8 -*-
"""Master_MIDI_Dataset_GPU_Search_and_Filter.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/asigalov61/Los-Angeles-MIDI-Dataset/blob/main/Extras/Master_MIDI_Dataset_GPU_Search_and_Filter.ipynb

# Master MIDI Dataset GPU Search and Filter (ver. 3.0)

***

Powered by tegridy-tools: https://github.com/asigalov61/tegridy-tools

***

#### Project Los Angeles

#### Tegridy Code 2024

***

# (SETUP ENVIRONMENT)

# ( GPU CHECK)
"""

# @title NVIDIA GPU Check
!nvidia-smi

"""# (SETUP ENVIRONMENT)"""

#@title Install all dependencies (run only once per session)

!git clone --depth 1 https://github.com/asigalov61/Los-Angeles-MIDI-Dataset
!pip install huggingface_hub

#@title Import all needed modules

print('Loading core modules... Please wait...')

import os
import copy
from collections import Counter
import random
import pickle
from tqdm import tqdm
import pprint
import statistics
import shutil

import cupy as cp

from huggingface_hub import hf_hub_download

print('Loading TMIDIX module...')
os.chdir('/content/Los-Angeles-MIDI-Dataset')

import TMIDIX

os.chdir('/content/')

print('Creating IO dirs... Please wait...')

if not os.path.exists('/content/Master-MIDI-Dataset'):
    os.makedirs('/content/Master-MIDI-Dataset')

if not os.path.exists('/content/Master-MIDI-Dataset'):
    os.makedirs('/content/Master-MIDI-Dataset')

if not os.path.exists('/content/Output-MIDI-Dataset'):
    os.makedirs('/content/Output-MIDI-Dataset')

print('Done!')
print('Enjoy! :)')

"""# (PREP MAIN MIDI DATASET)"""

#@title Download Los Angeles MIDI Dataset
print('=' * 70)
print('Downloading Los Angeles MIDI Dataset...Please wait...')
print('=' * 70)

hf_hub_download(repo_id='projectlosangeles/Los-Angeles-MIDI-Dataset',
                filename='Los-Angeles-MIDI-Dataset-Ver-4-0-CC-BY-NC-SA.zip',
                repo_type="dataset",
                local_dir='/content/Main-MIDI-Dataset',
                local_dir_use_symlinks=False)
print('=' * 70)
print('Done! Enjoy! :)')
print('=' * 70)

# Commented out IPython magic to ensure Python compatibility.
#@title Unzip Los Angeles MIDI Dataset
# %cd /content/Main-MIDI-Dataset/

print('=' * 70)
print('Unzipping Los Angeles MIDI Dataset...Please wait...')
!unzip 'Los-Angeles-MIDI-Dataset-Ver-4-0-CC-BY-NC-SA.zip'
print('=' * 70)

print('Done! Enjoy! :)')
print('=' * 70)
# %cd /content/

#@title Create Los Angeles MIDI Dataset files list
print('=' * 70)
print('Creating dataset files list...')
dataset_addr = "/content/Main-MIDI-Dataset/MIDIs"

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

#@title Load Los Angeles MIDI Dataset Signatures Data

print('=' * 70)
print('Loading LAMDa Signatures Data...')
sigs_data = pickle.load(open('/content/Main-MIDI-Dataset/SIGNATURES_DATA/LAMDa_SIGNATURES_DATA.pickle', 'rb'))
print('=' * 70)

print('Prepping signatures...')
print('=' * 70)

random.shuffle(sigs_data)

signatures_file_names = []
sigs_matrixes = [ [0]*(len(TMIDIX.ALL_CHORDS)+256) for i in range(len(sigs_data))]

idx = 0
for s in tqdm(sigs_data):

  signatures_file_names.append(s[0])

  for ss in s[1]:
    sigs_matrixes[idx][ss[0]] = ss[1]

  idx += 1

print('=' * 70)
print('Loading signatures...')
print('=' * 70)

signatures_data = cp.array(sigs_matrixes)

print('Done!')
print('=' * 70)

"""# (SEARCH AND FILTER)

### DO NOT FORGET TO UPLOAD YOUR MASTER DATASET TO "Master-MIDI-Dataset" FOLDER
"""

#@title Master MIDI Dataset Search and Filter

#@markdown NOTE: You can stop the search at any time to render partial results

number_of_top_matches_MIDIs_to_collect = 30 #@param {type:"slider", min:5, max:50, step:1}
search_matching_type = "Ratios" # @param ["Ratios", "Distances", "Correlations"]
maximum_match_ratio_to_search_for = 1 #@param {type:"slider", min:0, max:1, step:0.001}
distances_norm_order = 3 # @param {type:"slider", min:1, max:10, step:1}
match_drums = False # @param {type:"boolean"}

print('=' * 70)
print('Master MIDI Dataset GPU Search and Filter')
print('=' * 70)

###########

print('Loading MIDI files...')
print('This may take a while on a large dataset in particular.')

dataset_addr = "/content/Master-MIDI-Dataset"

filez = list()

for (dirpath, dirnames, filenames) in os.walk(dataset_addr):
    for file in filenames:
        if file.endswith(('.mid', '.midi', '.kar')):
            filez.append(os.path.join(dirpath, file))

print('=' * 70)

if filez:

  print('Randomizing file list...')
  random.shuffle(filez)
  print('=' * 70)

  ###################

  if not os.path.exists('/content/Output-MIDI-Dataset/'+search_matching_type):
      os.makedirs('/content/Output-MIDI-Dataset/'+search_matching_type)

  ###################

  input_files_count = 0
  files_count = 0

  for f in filez:
    try:

          input_files_count += 1

          fn = os.path.basename(f)
          fn1 = os.path.splitext(fn)[0]
          ext = os.path.splitext(f)[1]

          print('Processing MIDI File #', files_count+1, 'out of', len(filez))
          print('MIDI file name', fn)
          print('-' * 70)

          #=======================================================

          raw_score = TMIDIX.midi2single_track_ms_score(open(f, 'rb').read())
          escore = TMIDIX.advanced_score_processor(raw_score, return_score_analysis=False, return_enhanced_score_notes=True)[0]

          for e in escore:
            e[1] = int(e[1] / 16)
            e[2] = int(e[2] / 16)

          src_sigs = []

          for i in range(-6, 6):

            escore_copy = copy.deepcopy(escore)

            for e in escore_copy:
              e[4] += i

            cscore = TMIDIX.chordify_score([1000, escore_copy])

            sig = []

            for c in cscore:

              pitches = sorted(set([p[4] for p in c if p[3] != 9]))

              if pitches:
                if len(pitches) > 1:
                  tones_chord = sorted(set([p % 12 for p in pitches]))
                  checked_tones_chord = TMIDIX.check_and_fix_tones_chord(tones_chord)

                  sig_token = TMIDIX.ALL_CHORDS.index(checked_tones_chord) + 128

                elif len(pitches) == 1:
                  sig_token = pitches[0]

                sig.append(sig_token)

            fsig = [list(v) for v in Counter(sig).most_common()]

            src_sig_mat = [0] * (len(TMIDIX.ALL_CHORDS)+256)

            for s in fsig:

              src_sig_mat[s[0]] = s[1]

            src_sigs.append(src_sig_mat)

          src_signatures = cp.stack(cp.array(src_sigs))

          if not match_drums:
            src_signatures = cp.where(src_signatures < 128, src_signatures, 0)

          #=======================================================

          print('Searching for matches...Please wait...')
          print('-' * 70)

          lower_threshold = 0.0
          upper_threshold = maximum_match_ratio_to_search_for
          filter_size = number_of_top_matches_MIDIs_to_collect

          final_ratios = []

          avg_idxs = []

          all_filtered_means = []
          all_filtered_idxs = []
          all_filtered_tvs = []

          tv_idx = -6

          for target_sig in tqdm(src_signatures):

            if not match_drums:
              target_sig = cp.where(target_sig < 128, target_sig, 0)

            comps_lengths = cp.vstack((cp.repeat(cp.sum(target_sig != 0), signatures_data.shape[0]), cp.sum(signatures_data != 0, axis=1)))
            comps_lengths_ratios = cp.min(comps_lengths, axis=0) / cp.max(comps_lengths, axis=0)

            comps_counts_sums = cp.vstack((cp.repeat(cp.sum(target_sig), signatures_data.shape[0]), cp.sum(signatures_data, axis=1)))
            comps_counts_sums_ratios = cp.min(comps_lengths_ratios, axis=0) / cp.max(comps_lengths_ratios, axis=0)

            if search_matching_type == 'Ratios':

              ratios = cp.where(target_sig != 0, cp.divide(cp.minimum(signatures_data, target_sig), cp.maximum(signatures_data, target_sig)), 0)
              results = cp.mean(ratios, axis=1)

            elif search_matching_type == 'Distances':

              distances = cp.power(cp.sum(cp.power(cp.abs(signatures_data - target_sig), distances_norm_order), axis=1), 1 / distances_norm_order)
              results = 1 - cp.divide((distances - cp.min(distances)), (cp.max(distances) - cp.min(distances)))

            elif search_matching_type == 'Correlations':

              main_array_min = cp.min(signatures_data, axis=1, keepdims=True)
              main_array_max = cp.max(signatures_data, axis=1, keepdims=True)
              target_array_min = cp.min(target_sig)
              target_array_max = cp.max(target_sig)

              signatures_data_range = main_array_max - main_array_min
              target_sig_range = target_array_max - target_array_min

              signatures_data_normalized = cp.where(signatures_data_range != 0, (signatures_data - main_array_min) / signatures_data_range, 0)
              target_sig_normalized = cp.where(target_sig_range != 0, (target_sig - target_array_min) / target_sig_range, 0)

              correlations = cp.einsum('ij,j->i', signatures_data_normalized, target_sig_normalized)
              exp = cp.exp(correlations - cp.max(correlations))
              results = (exp / cp.sum(exp)) * 1000

            results = (results + comps_lengths_ratios + comps_counts_sums_ratios) / 3

            unique_means = cp.unique(results)
            sorted_means = cp.sort(unique_means)[::-1]

            filtered_means = sorted_means[(sorted_means >= lower_threshold) & (sorted_means <= upper_threshold)][:filter_size]

            filtered_idxs = cp.where(cp.in1d(results, filtered_means))[0]

            all_filtered_means.extend(results[cp.in1d(results, filtered_means)].tolist())

            all_filtered_idxs.extend(filtered_idxs.tolist())

            filtered_tvs = [tv_idx] * filtered_idxs.shape[0]

            all_filtered_tvs.extend(filtered_tvs)

            tv_idx += 1

          f_results = sorted(zip(all_filtered_means, all_filtered_idxs, all_filtered_tvs), key=lambda x: x[0], reverse=True)

          triplet_dict = {}

          for triplet in f_results:

              if triplet[0] not in triplet_dict:
                triplet_dict[triplet[0]] = triplet
              else:
                if triplet[2] == 0:
                  triplet_dict[triplet[0]] = triplet

          filtered_results = list(triplet_dict.values())[:filter_size]

          #=======================================================

          print('Done!')
          print('-' * 70)
          print('Max match ratio:', filtered_results[0][0])
          print('Max match transpose value:', filtered_results[0][2])
          print('Max match signature index:', filtered_results[0][1])
          print('Max match file name:', signatures_file_names[filtered_results[0][1]])
          print('-' * 70)
          print('Copying max ratios MIDIs...')

          for fr in filtered_results:

            max_ratio_index = fr[1]

            ffn = signatures_file_names[fr[1]]
            ffn_idx = [y[0] for y in LAMD_files_list].index(ffn)

            ff = LAMD_files_list[ffn_idx][1]

            #=======================================================

            dir_str = str(fn1)
            copy_path = '/content/Output-MIDI-Dataset/'+search_matching_type+'/'+dir_str
            if not os.path.exists(copy_path):
                os.mkdir(copy_path)

            fff = str(fr[0] * 100) + '_' + str(fr[2]) + '_' + ffn + '.mid'

            shutil.copy2(ff, copy_path+'/'+fff)

          shutil.copy2(f, copy_path+'/'+fn)

          #======================================================='''
          print('Done!')
          print('=' * 70)

          #=======================================================

          # Processed files counter
          files_count += 1

    except KeyboardInterrupt:
        print('Quitting...')
        print('Total number of processed MIDI files', files_count)
        print('=' * 70)
        break

    except Exception as ex:
        print('WARNING !!!')
        print('=' * 70)
        print('Bad file:', f)
        print('Error detected:', ex)
        print('=' * 70)
        continue

    print('Total number of processed MIDI files', files_count)
    print('=' * 70)

else:
  print('Could not find any MIDI files. Please check Dataset dir...')
  print('=' * 70)

"""# Congrats! You did it! :)"""