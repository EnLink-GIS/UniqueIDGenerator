## This script will grab random values from the characters list
## and then compare it to a "list" to make sure it is unique
## before it writes it out to a feature class.

## Created 12/1/2010
## Written by Mike Long
## www.geoville.org
## Mike@geoville.org

import random, string, arcpy, time, re

# Set the date.
Date = time.strftime("%A, %B %d, %Y", time.localtime())

# Set the time.
Time = time.strftime("%H:%M:%S", time.localtime())

DT =  str(Date) + " " + str(Time)

print "Started at " + str(DT)


arcpy.OverwriteOutput = 1

#Static values for testing.
layer = r"\\crosstexenergy.com\dfsshare\engr\Tools\Models & Python\10.1 Model Connection.sde\GIS.GIS.LineLoop"
##layer = "Database Connections\GIS@GIS.sde\GIS.GIS.LineLoop"
field = "Remarks"
##parent = "GF-106-01" # Alpha
parent = "CC-101-09" # Alpha
##parent = "GF-911" # Digit
##parent = "JP-111-02" #Alpha & Digit
##parent = "JP-305-09" #Digit goes to 10?
##parent = "P"
pre = parent + "."
length = 4


# Dynamic parameters for tools
##layer = arcpy.GetParameterAsText(0)
##field = arcpy.GetParameterAsText(1)
##length = arcpy.GetParameter(2)

arcpy.AddMessage(length)

uniquelist = [] # Empty list to store already created characters.

regex = re.compile(pre)

##########Define the random character generator##############

def ranchar(length):
    myrg=random.SystemRandom

    characters=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    numbers = ["1","2","3","4","5","6","7","8","9"]
    pw=string.join(myrg(random).sample(numbers,length))
    randomval = (pw.replace(' ', '')) # Removes some spaces between the letters.

    return randomval

#############################################################

fc = layer
field = field
cursor = arcpy.SearchCursor(fc)
for row in cursor:
    uniquelist.append(row.getValue(field)) # Adds the existing values to the list.

matches = [string for string in uniquelist if re.match(regex, string)]
print matches

# Remove parent prefix from every item.
for idx, item in enumerate(matches):
    if str(parent) + "-" in item:
        matches[idx] = item.replace(str(parent) + "-", '')
    elif parent in item:
        matches[idx] = item.replace(parent, '')
    else:
        print "Nothing to replace"
print matches

# Remove items with a dash in them.
should_restart = True
while should_restart:
    should_restart = False
    for idx, item in enumerate(matches):
        if "-" in item:
            matches.remove(item)
            should_restart = True



print matches

# Add dash if parent is not P or doesn't already have a dash.
# http://stackoverflow.com/questions/19954593/python-checking-a-strings-first-and-last-character
if parent <> "P" and parent.endswith('-'):
    parent = parent
else:
    parent = parent + "-"

if not matches: # http://stackoverflow.com/questions/53513/best-way-to-check-if-a-list-is-empty
    NewLineNum = parent + "01"
else:

    #if string.digits in enumerate(matches):
    Digit = [s for s in matches if s.isdigit()]
    if not Digit:
        D = False
    else:
        D = True

    Alpha = [s for s in matches if s.isalpha()]
    if not Alpha:
        A = False
    else:
        A = True

##    Punc = [s for s in matches if s.is()]
##    if string.punctuation in matches:
##        Punc = True
##    else:
##        Punc = False

    #Numeric only?
##    if Digit == True and Alpha == False and Punc == False:
##    if Digit == matches and Alpha <> matches:
    if D is True and A is False:
        i = int(matches[0])
        # Determine the length of the longest item in the list.
        MaxLen = len(max(matches, key=len))
        print str(MaxLen) + " is the max length."
        # Create next value in sequence.
        NewVal = int(max(matches)) + 1
        print str(NewVal)  + " is the next value in sequence."
        # Determine the length of new value.
        NewValLen = len(str(NewVal))
        print str(NewValLen) + " is the new values length."
        # Create the new line number.
        # http://stackoverflow.com/questions/733454/best-way-to-format-integer-as-string-with-leading-zeros
        if NewValLen < MaxLen:
            add_nulls = lambda number, zero_count : "{0:0{1}d}".format(number, zero_count)
            NewLineNum = parent + str(add_nulls(int(NewVal),(int(MaxLen)-int(NewValLen)+1)))
        else:
            NewLineNum = parent + str(NewVal)

    #Alpha only?
    elif D is False and A is True:
        print Alpha
        Alpha.sort()
        LastAlpha = (Alpha[-1])
        print string.strip(LastAlpha)
        #NewVal = string.uppercase[string.uppercase.index([LastAlpha]) + 1]
        #NewVal = int(max(matches)) + 1
        #print NewVal
        ##print str(NewVal)  + " is the next value in sequence."

    #Combo?
    elif D is True and A is True:
        print"Combo"

    else:
        print "Confused"
##    print NewLineNum

##for pre in uniquelist:
##    print pre
#print uniquelist

##    randomval = ranchar(length) # Grabs a random character from the function above.
##    preval = pre + randomval
##    print preval
##    if preval in uniquelist:
##        print str(preval) + " already exists, generating new value."
##        #randomval = ranchar(length) # check to see if it already exists.

##cur = arcpy.UpdateCursor(layer)
##row = cur.Next()
##
##while row:
##    randomval = ranchar(length) # Grabs a random character.
##    while randomval in uniquelist:
##        randomval = ranchar(length) # check to see if it already exists.
##
##    uniquelist.append(randomval) # If the value isn't in the list, adds it.
##    row.setValue(field, randomval) # Writes the value to the row.
##    cur.UpdateRow(row)
##    row = cur.Next()


arcpy.AddMessage(arcpy.GetMessages())
# Delete cursor and row objects to remove locks on the data
#