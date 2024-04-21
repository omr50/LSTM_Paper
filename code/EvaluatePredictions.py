from keras.models import load_model
import numpy as np
import csv
from keras.preprocessing.sequence import pad_sequences
from collections import Counter
import unicodecsv

filepath = '../data/helpdesk.csv'
outputCsv = './output_files/results/suffix_and_remaining_time_helpdesk.csv'

def extract_unique_chars(csv_filepath):
    unique_chars = set()
    with open(csv_filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header if your CSV has one
        for row in reader:
            event_type = row[1]  # Assuming the event type is in the second column
            unique_chars.add(event_type)
    return sorted(unique_chars)  # Sorting ensures consistent order

chars = extract_unique_chars(filepath)

char_indices = {c: i for i, c in enumerate(chars)}

model = load_model('output_files/models/model_40-1.51.h5')
print("IT LOADED?")

def encode_input(sequence, maxlen):
    num_features = len(chars) + 5  # number of event types + number of time features
    X = np.zeros((1, maxlen, num_features), dtype=np.float32)
    times2 = np.cumsum(times)  # cumulative time since case start
    leftpad = maxlen - len(sentence)  # padding to ensure fixed length sequences
    
    for t, char in enumerate(sentence):
        midnight = times3[t].replace(hour=0, minute=0, second=0, microsecond=0)
        timesincemidnight = (times3[t] - midnight).total_seconds()
        multiset_abstraction = Counter(sentence[:t+1])
        
        X[0, t + leftpad, char_indices[char]] = 1  # One-hot encoding of the character
        X[0, t + leftpad, len(chars)] = t + 1  # Position in the sequence
        X[0, t + leftpad, len(chars)+1] = times[t] / divisor  # Normalized time since last event
        X[0, t + leftpad, len(chars)+2] = times2[t] / divisor2  # Normalized cumulative time
        X[0, t + leftpad, len(chars)+3] = timesincemidnight / 86400  # Time since midnight, normalized
        X[0, t + leftpad, len(chars)+4] = times3[t].weekday() / 7.0  # Day of the week, normalized

    return X

indices_char = {i: c for i, c in enumerate(chars)}

def decode_output(output):
    predicted_char_indices = np.argmax(predictions, axis=-1)
    predicted_chars = [indices_char[idx] for idx in predicted_char_indices]
    return ''.join(predicted_chars)

def read_data(filepath):
    with open(filepath, 'rb') as csvfile:
        reader = unicodecsv.reader(csvfile, encoding='utf-8')
        next(reader)  # Skip the header
        data = [row for row in reader]
    print(data[:5])  # Print first 5 rows to check data
    return data

def calculate_accuracy(data):
    correct = 0
    total = 0
    for row in data:
        ground_truth = row[2].decode('latin1') if isinstance(row[2], bytes) else row[2]
        predicted = row[3].decode('latin1') if isinstance(row[3], bytes) else row[3]
        if ground_truth == predicted:
            correct += 1
        else:
            print('Mismatch: Ground Truth =', ground_truth, 'Predicted = ', predicted)  # Debug output
        total += 1
    return correct / total if total > 0 else 0

data = read_data(outputCsv)
accuracy = calculate_accuracy(data)
print("Accuracy: {:.2%}".format(accuracy))




