import json
#Authors: Rachel Madison and Caroline Cavaliere

fileNum = input("Enter a number 1-5 corresponding to the number at the end of the input file name: ")


with open("testinput" + fileNum + ".json" , "r") as read_file:
    data = json.load(read_file) #load DFA JSON data from test input file


num_states = len(data["dfa1"]["Q"]) * len(data["dfa2"]["Q"]) #num states in union DFA
q_arr = [""]*num_states #array of states
f_arr = []  #array of accepting states
count = 0
delta = {} #python dict for union DFA delta table

for i in data["dfa1"]["Q"]:
    for j in data["dfa2"]["Q"]:
        q_arr[count] = i+j #add combined states from both DFAs to union Q
        if i in data["dfa1"]["F"]:
            f_arr.append(i + j) #add any final states from dfa1 to union F
        elif j in data["dfa2"]["F"]:
            f_arr.append(i + j) #add any final states from dfa1 to union F
        delta[i+j] = {} #create empty delta table
        delta[i+j]['A'] = data["dfa1"]["delta"][i]["A"] + data["dfa2"]["delta"][j]["A"] #add A transitions
        delta[i+j]['B'] = data["dfa1"]["delta"][i]["B"] + data["dfa2"]["delta"][j]["B"] #add B transitions
        count+=1

 #union DFA JSON object   
dfa_union = {
    "Q":q_arr,
    "sigma":data["dfa1"]["sigma"],
    "delta":delta,
    "initialState":data["dfa1"]["initialState"] + data["dfa2"]["initialState"],
    "F":f_arr
}

with open('dfa_union.json', 'w') as f:
    json.dump(dfa_union, f) #output union DFA as JSON object

