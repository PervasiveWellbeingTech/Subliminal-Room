from __future__ import division
import random
import json

attempts = 0
rmin = .25
rmax = .35
stimCount = 15
dlength = 20
length = 0
goal = 2000
stim = []
finalSeq = []
finalResp = {
'2': [],
'3': []
}
run = True

def dump(seq, resp):
    with open('dump.json', mode='w') as f:
        data = {
        'responses': resp,
        'sequence': seq
        }
        json.dump(data, f)

def check(l, n):
    return l[0] is l[n]

def shift(l, cur):
    n = len(l)
    for i in range(n-1):
        l[n-1-i] = l[n-2-i]
    l[0] = cur
    # print('shifted nback is {}'.format(l))

def calculateSuccessRate(seq, n):
    responses = {}
    nmax = 0
    for i in n:
        nmax = max(nmax, i)
    # print('nmax is {}.'.format(nmax))
    nback = [None] * (nmax+1)
    success = [0] * len(n)

    for i in n:
        responses[str(i)] = [0] * len(seq)

    for i in range(len(seq)):
        shift(nback, seq[i])
        for j in range(len(n)):
            if check(nback, n[j]):
                success[j]+=1
                responses[str(n[j])][i] = 1


                # print('Success for n={}, nback={}'.format(n[j], nback))

    for i in range(len(success)):
        success[i] = success[i]/dlength
    return success, responses

for i in range(stimCount):
    stim.append(i)
if run:
    while length < goal:
        looking = True
        while looking:
            sequence = []
            nbackStore = []
            for i in range(dlength):
                index = random.randint(0, len(stim) - 1)
                sequence.append(index)
            inRow = False
            for i in range(2, len(sequence)):
                if sequence[i] is sequence[max(i-1, 0)] and sequence[i] is sequence[max(i-2, 0)]:
                    inRow = True
                    break
            if inRow:
                continue
            rates, responses = calculateSuccessRate(sequence, n=[2,3])
            looking = False
            for r in rates:
                if r > rmax or r < rmin:
                    looking = True
                    # print('r={} is not right, still looking, attempt={}.'.format(r, attempts+1))
                    break
            attempts+=1
            # print(attempts)
        print('good sequence of length {} after {} attempts'.format(dlength, attempts))
        print(sequence)
        length += dlength
        attempts = 0
        for i in sequence:
            finalSeq.append(i)
        for i in responses['2']:
            finalResp['2'].append(i)
        for i in responses['3']:
            finalResp['3'].append(i)

    print finalSeq
    print finalResp
    counts = [0] * stimCount
    for i in finalSeq:
        counts[i]+=1
    for c in counts:
        c = c/len(finalSeq)
    print counts
