import json

gt = json.load(open('answer.json', 'r'))

pred = json.load(open('result.json', 'r'))

total_data = len(gt)

cnt = 0

for gg in gt:
    curr_sentence = gg['sentence']
    curr_answer = gg['user_id']

    search = True
    for pp in pred:
        if pp['sentence'] == curr_sentence:
            if int(pp['user_id']) == int(curr_answer):
                cnt += 1
                search = False
        if not search:
            break

print(cnt/total_data)