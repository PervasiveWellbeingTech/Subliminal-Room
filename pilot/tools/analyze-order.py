from __future__ import division
import json
import libs

inputDir = libs.path + 'pilot/input/nback/JSON/'
data = None
with open(inputDir + '1.json', 'r') as f:
    data = json.load(f, data)

sequence = data['sequence']
correct = [0] * len(sequence)
# print len(sequence)
for i in reversed(range(2, len(sequence))):
    if sequence[i] is sequence[i-2]:
        correct[i] = 1

for i in range(len(correct)):
    if correct[i] is not data['responses']['2'][i]:
        print i
    else:
        print '{} and {} are the same'.format(correct[i], data['responses']['2'][i])
