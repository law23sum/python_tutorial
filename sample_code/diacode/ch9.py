######################chapter 9


import pandas as pd

ess = pd.read_csv('ess.csv')

print(ess.shape)

print(ess.loc[:, 'happy'].head())

print(ess.loc[:, 'sclmeet'].head())

ess = ess.loc[ess['sclmeet'] <= 10, :].copy()
ess = ess.loc[ess['rlgdgr'] <= 10, :].copy()
ess = ess.loc[ess['hhmmb'] <= 50, :].copy()
ess = ess.loc[ess['netusoft'] <= 5, :].copy()
ess = ess.loc[ess['agea'] <= 200, :].copy()
ess = ess.loc[ess['health'] <= 5, :].copy()
ess = ess.loc[ess['happy'] <= 10, :].copy()
ess = ess.loc[ess['eduyrs'] <= 100, :].copy().reset_index(drop=True)

import numpy as np

social = list(ess.loc[:, 'sclmeet'])
happy = list(ess.loc[:, 'happy'])
low_social_happiness = [hap for soc, hap in zip(social, happy) if soc <= 5]
high_social_happiness = [hap for soc, hap in zip(social, happy) if soc > 5]
meanlower = np.mean(low_social_happiness)
meanhigher = np.mean(high_social_happiness)

lowererrors = [abs(lowhappy - meanlower) for lowhappy in low_social_happiness]
highererrors = [abs(highhappy - meanhigher) for highhappy in high_social_happiness]
total_error = sum(lowererrors) + sum(highererrors)


def get_splitpoint(allvalues, predictedvalues):
    lowest_error = float('inf')
    best_split = None
    best_lowermean = np.mean(predictedvalues)
    best_highermean = np.mean(predictedvalues)
    for pctl in range(0, 100):
        split_candidate = np.percentile(allvalues, pctl)
        loweroutcomes = [outcome for value, outcome in zip(allvalues, predictedvalues) if \
                         value <= split_candidate]
        higheroutcomes = [outcome for value, outcome in zip(allvalues, predictedvalues) if \
                          value > split_candidate]
        if np.min([len(loweroutcomes), len(higheroutcomes)]) > 0:
            meanlower = np.mean(loweroutcomes)
            meanhigher = np.mean(higheroutcomes)
            lowererrors = [abs(outcome - meanlower) for outcome in loweroutcomes]
            highererrors = [abs(outcome - meanhigher) for outcome in higheroutcomes]
            total_error = sum(lowererrors) + sum(highererrors)
            if total_error < lowest_error:
                best_split = split_candidate
                lowest_error = total_error
                best_lowermean = meanlower
                best_highermean = meanhigher
    return (best_split, lowest_error, best_lowermean, best_highermean)


allvalues = list(ess.loc[:, 'hhmmb'])
predictedvalues = list(ess.loc[:, 'happy'])
print(get_splitpoint(allvalues, predictedvalues))


def getsplit(data, variables, outcome_variable):
    best_var = ''
    lowest_error = float('inf')
    best_split = None
    predictedvalues = list(data.loc[:, outcome_variable])
    best_lowermean = -1
    best_highermean = -1
    for var in variables:
        allvalues = list(data.loc[:, var])
        splitted = get_splitpoint(allvalues, predictedvalues)
        if (splitted[1] < lowest_error):
            best_split = splitted[0]
            lowest_error = splitted[1]
            best_var = var
            best_lowermean = splitted[2]
            best_highermean = splitted[3]
    generated_tree = [[best_var, float('-inf'), best_split, best_lowermean], [best_var, best_split, \
                                                                              float('inf'), best_highermean]]
    return (generated_tree)


variables = ['rlgdgr', 'hhmmb', 'netusoft', 'agea', 'eduyrs']
outcome_variable = 'happy'
print(getsplit(ess, variables, outcome_variable))


def getsplit(depth, data, variables, outcome_variable):
    best_var = ''
    lowest_error = float('inf')
    best_split = None
    predictedvalues = list(data.loc[:, outcome_variable])
    best_lowermean = -1
    best_highermean = -1
    for var in variables:
        allvalues = list(data.loc[:, var])
        splitted = get_splitpoint(allvalues, predictedvalues)
        if (splitted[1] < lowest_error):
            best_split = splitted[0]
            lowest_error = splitted[1]
            best_var = var
            best_lowermean = splitted[2]
            best_highermean = splitted[3]
    generated_tree = [[best_var, float('-inf'), best_split, []], [best_var, \
                                                                  best_split, float('inf'), []]]
    if depth < maxdepth:
        splitdata1 = data.loc[data[best_var] <= best_split, :]
        splitdata2 = data.loc[data[best_var] > best_split, :]
        if len(splitdata1.index) > 10 and len(splitdata2.index) > 10:
            generated_tree[0][3] = getsplit(depth + 1, splitdata1, variables, outcome_variable)
            generated_tree[1][3] = getsplit(depth + 1, splitdata2, variables, outcome_variable)
        else:
            depth = maxdepth + 1
            generated_tree[0][3] = best_lowermean
            generated_tree[1][3] = best_highermean
    else:
        generated_tree[0][3] = best_lowermean
        generated_tree[1][3] = best_highermean
    return (generated_tree)


variables = ['rlgdgr', 'hhmmb', 'netusoft', 'agea', 'eduyrs']
outcome_variable = 'happy'
maxdepth = 2
print(getsplit(0, ess, variables, outcome_variable))

variables = ['sclmeet', 'rlgdgr', 'hhmmb', 'netusoft', 'agea', 'eduyrs', 'health']
outcome_variable = 'happy'
maxdepth = 3
print(getsplit(0, ess, variables, outcome_variable))


def get_prediction(observation, tree):
    j = 0
    keepgoing = True
    prediction = - 1
    while (keepgoing):
        j = j + 1
        variable_tocheck = tree[0][0]
        bound1 = tree[0][1]
        bound2 = tree[0][2]
        bound3 = tree[1][2]
        if observation.loc[variable_tocheck] < bound2:
            tree = tree[0][3]
        else:
            tree = tree[1][3]
        if isinstance(tree, float):
            keepgoing = False
            prediction = tree
    return (prediction)


predictions = []
outcome_variable = 'happy'
maxdepth = 4
thetree = getsplit(0, ess, variables, outcome_variable)
for k in range(0, 30):
    observation = ess.loc[k, :]
    predictions.append(get_prediction(observation, thetree))

print(predictions)

predictions = []
for k in range(0, len(ess.index)):
    observation = ess.loc[k, :]
    predictions.append(get_prediction(observation, thetree))

ess.loc[:, 'predicted'] = predictions
errors = abs(ess.loc[:, 'predicted'] - ess.loc[:, 'happy'])
print(np.mean(errors))

import numpy as np

np.random.seed(518)
ess_shuffled = ess.reindex(np.random.permutation(ess.index)).reset_index(drop=True)
training_data = ess_shuffled.loc[0:37000, :]
test_data = ess_shuffled.loc[37001:, :].reset_index(drop=True)

thetree = getsplit(0, training_data, variables, outcome_variable)

predictions = []
for k in range(0, len(test_data.index)):
    observation = test_data.loc[k, :]
    predictions.append(get_prediction(observation, thetree))

test_data.loc[:, 'predicted'] = predictions
errors = abs(test_data.loc[:, 'predicted'] - test_data.loc[:, 'happy'])
print(np.mean(errors))
