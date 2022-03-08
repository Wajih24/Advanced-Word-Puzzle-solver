import  tensorflow as tf
print(tf.__version__)
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import cv2
import os
import copy
import progressbar
import pickle
from collections import Counter


def set_node_labels(G, arr):
    values = arr.flatten()
    labels = {}
    for node in G.nodes():
        labels[node] = values[node]
    nx.set_node_attributes(G, labels, "label")
    return labels


def get_possible_words(word, idx_array, letter_array, G):
    found_word = []
    found_word_loc = []
    first_letter = word[0]
    last_letters = word[1:]
    first_letter_idx = idx_array[np.where(letter_array == first_letter)]
    last_letters_idx = []
    for letters in last_letters:
        last_letters_idx.extend(idx_array[np.where(letter_array == [letter for letter in letters])])
    print(f'{word}')
    paths = []
    idx = 0
    for s in first_letter_idx:
        last_letters_idx = np.array(last_letters_idx)[last_letters_idx != s]
        for path in nx.all_simple_paths(G, s, last_letters_idx, cutoff=len(word)):
            string = []
            for node in path:
                string.extend(G.nodes[node]['label'])
            found_word.append(string)
            found_word_loc.append(path)
    return found_word, found_word_loc


def check_validity(sequence_arr, W):
    flag = False
    id = -1
    for i, seq in enumerate(sequence_arr):
        sorted_seq = sorted(seq)
        first_number = sorted_seq[0]
        horiz = np.arange(first_number, first_number + len(seq), 1).tolist()
        down = np.arange(first_number, first_number + W*len(seq) - W + 1, W).tolist()
        diag = np.arange(first_number, first_number + W*len(seq), W+1).tolist()
        diag_rev = np.arange(first_number, first_number + (W-1)*len(seq), W-1).tolist()
        if sorted_seq == horiz:
            print('match horiz')
            flag = True
            id = i
            break
        elif sorted_seq == diag:
            print('match diag')
            flag = True
            id = i
            break
        elif sorted_seq == down:
            print('match down')
            flag = True
            id = i
            break
        elif sorted_seq == diag_rev:
            print('match diag rev')
            flag = True
            id = i
            break
    return flag, id


def clean_string(string):
    tmp = ''
    for line in string:
        tmp += line.strip(' ').replace('-', '').replace('.', '')
    tmp = tmp.replace("'", '"')
    tmp = os.linesep.join([s for s in tmp.splitlines() if s])
    return tmp


data_dir = Path('data')
paths = list(data_dir.glob('*/*.png'))
screenshot_dir = 'images'
print("[INFO] loading pre-trained network...")
model = load_model('models')

# Hydrate the serialized objects.
with open('label-binarizer.pkl', 'rb') as f:
    lb = pickle.load(f)

labels = []

widgets = ["Processing image: ", progressbar.Percentage(), " ",
           progressbar.Bar(), " ", progressbar.ETA()]

for entry in os.scandir(screenshot_dir):
    if entry.path.endswith(".png") and entry.is_file():
        print('[INFO] assigning characters to image...')
        im = cv2.imread(entry.path)
        gray = cv2.cvtColor(im.astype('uint8'), cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        thresh = thresh[1]
        conn = cv2.connectedComponentsWithStats(thresh, 8, cv2.CV_16U)
        stats = conn[2]
        pad = 8
        counts = {}

        pbar = progressbar.ProgressBar(maxval=len(stats),
                                       widgets=widgets).start()

        for i, (x, y, w, h, a) in enumerate(stats[1:]):
            cv2.rectangle(im, (x - pad, y - pad), (x + w + pad, y + h + pad), (0, 255, 0), 2)
            roi = gray[y - pad:y + h + pad, x - pad:x + w + pad]
            image = cv2.resize(roi, (28, 28))
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0)
            pred = model.predict(image)
            pred = np.where(pred == np.max(pred, axis=1), 1, 0)
            label = lb.inverse_transform(pred).tolist()[0]
            labels.append(label)
            cv2.putText(im, label, (x + 3, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
            pbar.update(i)
        pbar.finish()
        label_array = np.array(labels).reshape((80,80))
        print(label_array)
        with open(r"output/wordsearch-test-grid-output.txt", "w") as f:
            for line in label_array:
                clean_line = clean_string(line)
                f.write("%s\n" % clean_line)
        cv2.imwrite(r'output\wordsearch-test-grid-output.png', im)
        if cv2.waitKey(0) & 0xFF == ord("q"):
            cv2.destroyAllWindows()

        break

model = load_model('models1')


with open('label-binarizer.pkl', 'rb') as f:
    lb = pickle.load(f)

labels = []

widgets = ["Processing image: ", progressbar.Percentage(), " ",
           progressbar.Bar(), " ", progressbar.ETA()]

for entry in os.scandir(screenshot_dir):
    if entry.path.endswith(".png") and entry.is_file():
        print('[INFO] assigning characters to image...')
        im = cv2.imread(entry.path)
        gray = cv2.cvtColor(im.astype('uint8'), cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        thresh = thresh[1]
        conn = cv2.connectedComponentsWithStats(thresh, 8, cv2.CV_16U)
        stats = conn[2]
        pad = 8
        counts = {}

        pbar = progressbar.ProgressBar(maxval=len(stats),
                                       widgets=widgets).start()

        for i, (x, y, w, h, a) in enumerate(stats[1:]):
            cv2.rectangle(im, (x - pad, y - pad), (x + w + pad, y + h + pad), (0, 255, 0), 2)
            roi = gray[y - pad:y + h + pad, x - pad:x + w + pad]
            image = cv2.resize(roi, (28, 28))
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0)
            pred = model.predict(image)
            pred = np.where(pred == np.max(pred, axis=1), 1, 0)
            label = lb.inverse_transform(pred).tolist()[0]
            labels.append(label)
            cv2.putText(im, label, (x + 3, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
            pbar.update(i)
        pbar.finish()
        label_array = np.array(labels).reshape((80,80))
        print(label_array)
        with open(r"output/wordsearch-test-grid-output1.txt", "w") as f:
            for line in label_array:
                clean_line = clean_string(line)
                f.write("%s\n" % clean_line)
        cv2.imwrite(r'output\wordsearch-test-grid-output1.png', im)
        if cv2.waitKey(0) & 0xFF == ord("q"):
            cv2.destroyAllWindows()

        break
model = load_model('models2')


with open('label-binarizer.pkl', 'rb') as f:
    lb = pickle.load(f)

labels = []
widgets = ["Processing image: ", progressbar.Percentage(), " ",
           progressbar.Bar(), " ", progressbar.ETA()]

for entry in os.scandir(screenshot_dir):
    if entry.path.endswith(".png") and entry.is_file():
        print('[INFO] assigning characters to image...')
        im = cv2.imread(entry.path)
        gray = cv2.cvtColor(im.astype('uint8'), cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        thresh = thresh[1]
        conn = cv2.connectedComponentsWithStats(thresh, 8, cv2.CV_16U)
        stats = conn[2]
        pad = 8
        counts = {}

        pbar = progressbar.ProgressBar(maxval=len(stats),
                                       widgets=widgets).start()

        for i, (x, y, w, h, a) in enumerate(stats[1:]):
            cv2.rectangle(im, (x - pad, y - pad), (x + w + pad, y + h + pad), (0, 255, 0), 2)
            roi = gray[y - pad:y + h + pad, x - pad:x + w + pad]
            image = cv2.resize(roi, (28, 28))
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0)
            pred = model.predict(image)
            pred = np.where(pred == np.max(pred, axis=1), 1, 0)
            label = lb.inverse_transform(pred).tolist()[0]
            labels.append(label)
            cv2.putText(im, label, (x + 3, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
            pbar.update(i)
        pbar.finish()
        label_array = np.array(labels).reshape((80,80))
        print(label_array)
        with open(r"output/wordsearch-test-grid-output2.txt", "w") as f:
            for line in label_array:
                clean_line = clean_string(line)
                f.write("%s\n" % clean_line)
        cv2.imwrite(r'output\wordsearch-test-grid-output2.png', im)
        if cv2.waitKey(0) & 0xFF == ord("q"):
            cv2.destroyAllWindows()

        break


elem0= open('output/wordsearch-test-grid-output.txt','r')
elem1= open('output/wordsearch-test-grid-output1.txt','r')
elem2= open('output/wordsearch-test-grid-output2.txt','r')
final = open('output/final.txt','w')
pz=(elem0.readlines())
pz1=elem1.readlines()
pz2=elem2.readlines()

finalpz=[["?" for _ in range(80)]for _ in range(80)]
for i in range(len(pz)):
    for j in range(len(pz)):
        wd = [pz[i][j],pz1[i][j],pz2[i][j]]
        C=Counter(wd)
        if max(C.values())>1:
            finalpz[i][j]=max(C, key=C.get)
        else : 
            finalpz[i][j]=pz2[i][j]

for i in finalpz :
    final.write(''.join(i)+ "\n")

final.close()