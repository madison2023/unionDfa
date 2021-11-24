import json
#Authors: Rachel Madison and Caroline Cavaliere

fileNum = input("Enter a number 1-5 corresponding to the number at the end of the input file name: ")


with open("testinput" + fileNum + ".json" , "r") as read_file:
    data = json.load(read_file) #load DFA JSON data from test input file


def isValidDfa(dfa):
    isValid = True
    
    if not "Q" in dfa:
        isValid = False
        print("no Q")
    elif dfa["Q"] == '':
        isValid = False
        print("Q empty")
    elif not "initialState" in dfa:
        isValid = False
        print("no initalState")
    elif dfa["initialState"] == '':
        isValid = False
        print("initialState empty")
    elif not "delta" in dfa:
        isValid = False
        print("no delta")
    elif dfa["delta"] == '':
        isValid = False
        print("delta empty")
    else:
        for i in dfa["Q"]:
            for j in dfa["sigma"]:
                if not j in dfa["delta"][i].keys():
                    isValid = False
                    print("delta transition missing character in sigma")
                    return isValid
                
                if not dfa["delta"][i][j] in dfa["Q"]:
                    isValid = False
                    print("Delta transition doesn't go to a state in Q")
                    return isValid

            for k in dfa["delta"][i].keys():
                if not k in dfa["sigma"]:
                    isValid = False
                    print("character in delta not also in sigma")
                    return isValid
    return isValid

#check if dfa's from input file are isValid
isDfa1Valid = isValidDfa(data["dfa1"])
isDfa2Valid = isValidDfa(data["dfa2"])

#quit program if dfa input is not isValid
if isDfa1Valid == False or isDfa2Valid == False:
    print("At least one DFA input is not valid")
    quit()
else:
    print("valid input!")

q_arr = [] #array of states
f_arr = []  #array of accepting states
count = 0
delta = {} #python dict for union DFA delta table
diff_sigmas = False

#check if the DFAs have different sigmas
for i in data["dfa1"]["sigma"]:
    for j in data["dfa2"]["sigma"]:
        if not i in data["dfa2"]["sigma"] or not j in data["dfa1"]["sigma"]:
            diff_sigmas = True

#add Q_Reject state if DFAs have different sigmas         
if diff_sigmas == True:
    q_arr.append("Q_Reject")
    delta["Q_Reject"] = {}

dfa1_alphabet = set(data["dfa1"]["sigma"])
dfa2_alphabet = set(data["dfa2"]["sigma"])

dfa_2_chars_not_in_dfa_1 = list(dfa2_alphabet - dfa1_alphabet)
combined_list = data["dfa1"]["sigma"] + dfa_2_chars_not_in_dfa_1


if diff_sigmas == True:
    for letter in combined_list:
        transition = {letter: "Q_Reject"} #add self loop to Q_Reject for all characters in both sigmas
        delta["Q_Reject"].update(transition)

for i in data["dfa1"]["Q"]:
    for j in data["dfa2"]["Q"]:
        q_arr.append(i+j) #add combined states from both DFAs to union Q
        if i in data["dfa1"]["F"]:
            f_arr.append(i + j) #add any final states from dfa1 to union F
        elif j in data["dfa2"]["F"]:
            f_arr.append(i + j) #add any final states from dfa2 to union F
        delta[i+j] = {} #create empty delta table
        for k in data["dfa1"]["sigma"]:
            for m in data["dfa2"]["sigma"]:
                if k in data["dfa2"]["sigma"] and m in data["dfa2"]["sigma"]: 
                    delta[i+j][k] = data["dfa1"]["delta"][i][k] + data["dfa2"]["delta"][j][k] #add transitions for characters that are in both sigmas
                elif k not in data["dfa2"]["sigma"]:
                    delta[i+j][k] = "Q_Reject" #send transition to Q_Reject if character does not belong to both sigmas
        for m in data["dfa2"]["sigma"]:
            for k in data["dfa1"]["sigma"]:
                if m not in data["dfa1"]["sigma"]:
                    delta[i+j][m] = "Q_Reject" #send transition to Q_Reject if character does not belong to both sigmas
                    

#union DFA JSON object   
dfa_union = {
    "Q":q_arr,
    "sigma":combined_list,
    "delta":delta,
    "initialState":data["dfa1"]["initialState"] + data["dfa2"]["initialState"],
    "F":f_arr
}

with open('dfa_union.json', 'w') as f:
    json.dump(dfa_union, f, indent=4) #output union DFA as JSON object

