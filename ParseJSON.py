import json
# import requests

# open and load JSON file for parsing
# SystemViewController | Test
with open("SystemViewController.json") as jsonFile:
    jsonData = json.load(jsonFile)

selector = ""

# user input
while True:
    selector = input("please enter selector: ")
    
    if len(selector) > 0:
        break;


matchedViews = list()

selectors = list()

# finds if is chained selector is and splits 
# into list of the individual selectiors
if ' ' in selector:
    for selector in selector.split(' '):
        selectors.append(selector)
else:
    selectors.append(selector)

print(selectors) # <-- DEBUGGING

# recursive JSON tree parser which finds & stores selected views
def parseJSON(lis, selectName, selectType, matches):
    m = matches
    
    for dic in lis:
        if selectType == "classNames":
            if selectType in dic and len(dic[selectType]) > 0:
                for cName in dic[selectType]:
                    if cName == selectName:
                        m.append(dic)
        else:
            if selectType in dic and dic[selectType] == selectName:
                m.append(dic)

        # if has deeper level, dive one hierarchy level and do it again
        if 'subviews' in dic and len(dic['subviews']) > 0:
            m = parseJSON(dic['subviews'], selectName, selectType, m)
        elif 'contentView' in dic:
            m = parseJSON(dic['contentView']['subviews'], selectName, selectType, m)
        elif 'control' in dic:
            m = parseJSON([dic['control']], selectName, selectType, m)

    return m

print()

# initialize dictionary to which 
# the selected views will be inserted
dct = {'results' : [jsonData]}

# for each chained selector, recursevely parse JSON
# to find view with matching selector
for select in selectors:
    selectType = select[0]
    selectName = select[1:]

    if selectType == '.':
        print("Parsing for Objs w/ CLASSNAME:", selectName, "...")
        dct['results'] = parseJSON(dct['results'], selectName, 'classNames', list())

    elif selectType == '#':
        print("Parsing for Objs w/ IDENTIFIER:", selectName, "...")
        dct['results'] = parseJSON(dct['results'], selectName, 'identifier', list())

    else:
        print("Parsing for Objs w/ CLASS:", select, "...")
        dct['results'] = parseJSON(dct['results'], select, 'class', list())

# report number os selections
print("# of results: ", len(dct['results']), "\n")

# sturcture JSON and print to stdin
printOut = json.dumps(dct['results'], indent=2)
print(printOut, "\n")

# write output JSON to file
with open("output.json", "w") as output:
    output.truncate(0)
    json.dump(dct, output, indent=2)
    print("Selected views written to", output.name, "file\n")