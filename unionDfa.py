import json

with open("testinput.json", "r") as read_file:
    data = json.load(read_file)
    #print(data["dfa1"]["delta"]["Q"][0])


num_states = len(data["dfa1"]["Q"]) * len(data["dfa2"]["Q"])
q_arr = [""]*num_states
count = 0
for i in data["dfa1"]["Q"]:
    for j in data["dfa2"]["Q"]:
        q_arr[count] = i+j
        count+=1
    
    
dfa_union = {
    "Q":q_arr,
    "sigma":["B", "A"],
    "delta":"",
    "initialState":data["dfa1"]["initialState"] + data["dfa2"]["initialState"],
    "F":""
}

with open('dfa_union.json', 'w') as f:
    json.dump(dfa_union, f)

