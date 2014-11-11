# CSV to XML converter...
# Converts your CSV file into XML using a list of tags.
# Fields in CSV must be in the order they will be in XML file.

import sys
import string
import csv
from xml.sax.saxutils import escape
xrclc={'\'':"&apos;", '\"':'&quot;', u'\u2019':'&apos;', u'\u2013':'-'} # for escape...

"""
S = start of list of properties. "<address "
A = append as property of previous item. "tag=field". followed by another dash won't close xml entity.
1 = single field from 1. named via 'tags[index]' and tag will include contents of field at index. three lines. start of field, contents, end of field
E = end of list of properties. closes previous tag.

--- following items are not yet implemented ---
2 = single field from 2.
M = multiple repeating single fields from last source.
N = next source.
P = previous source
"""

# setup objects...
spamReader = csv.reader(open('eggs.csv'))

# key - this makes it easier to understand the tokenlist...
# SA = take a tag, next tag is attribute
# SAA = take a tag, next two tags are attributes (means include values)
# AS = attribute, close tag, new tag
# SS = nesting.. open tag, open tag...
# SE = open tag then close it. an empty tag.
# 1 = open tag, value, close tag
# S1E = single tag, followed by another tag, the value, then close tag

#               0           1          2                       3               4                 5                  6                 7      8              9      10                        11              12                       13                    14          15         16      17     18      19            20      21      22          23       24              25          26                 27                        28         29              30           31          32         33      34
tagsinitial = ["PROVIDERS", "PROVIDER", "PROVIDER_EXTERNAL_KEY", "PROVIDER_TYPE", "IS_PRACTITIONER", "MASTER_CONTRACTS", "MASTER_CONTRACT", "NAME","SUB_CONTRACT", "NAME", "PROVIDER_SUBCONTRACT_ID", "FACILITY_NAME", "ELIGIBLE_FOR_REFERRALS", "PRACTICE_PHILOSOPHY", "LOCATIONS", "LOCATION", "LINE1", "CITY", "STATE", "POSTAL_CODE", "LINE2", "PHONE", "AREA_CODE", "NUMBER", "COUNTRY_CODE", "EXTENSION", "ACCEPTS_CHILDREN", "ACCEPTING_NEW_PATIENTS", "COMMENT", "COMMENT_LINE", "SCHEDULES", "SCHEDULE", "WEEKDAY", "OPEN", "CLOSE"]

#  tags numbering - see below. makes it easy to find which tags are used where.
#  first tag is the root, so ignore it for the tokenlist...
#                   1   111111111 222222 2222 33333
#          1234567890   123456789 012345 6789 01234
tokenList="SAAASSASAAEEE111SSAAAAE1SAA11E11S1ESSAAAEEE"
#tokenList="SA1SAA111ESSA1EEEEE" old
tagsinitial.reverse() # reversing the tags allows us to 'pop' the first item instead of the last. taking a fifo queue and reversing it makes it a lifo queue.
root = tagsinitial.pop()
tagsinitial.reverse()
print "<%s>" %root

for raw in spamReader:
    tags = list(tagsinitial)
    tags.reverse()
    closingtags = []
    #print tags.pop()
    tokens = list(tokenList[::-1]) # reverses string and converts it to a list.

    # cleans up data...
    fields = [escape(field.strip("\""),xrclc) for field in raw]
    fields.reverse()

    while tokens:
        # get xml output instructions
        token = tokens.pop()

        # get xml tags (if any)
        if len(tags) == 0:
            tags.append("")
        tag = tags.pop()

        if len(fields) == 0:
            fields.append("")

        field = fields.pop()

        if token == "S":
            print "<" + tag,
            fields.append(field)
            closingtags.append(tag)
            testtoken = tokens.pop()
            tokens.append(testtoken)
            if testtoken in ('S','1','E'):
                print ">"

        elif token == "E":
            print "</" + closingtags.pop() + ">"
            tags.append(tag)
            fields.append(field)

        elif token == "1":
            print "<" + tag + ">" + field + "</" + tag + ">"

        elif token == "A":
            print tag + "=\"" + field + "\"",
            testtoken = tokens.pop() #pop a peek...
            tokens.append(testtoken)
            if testtoken <> "A": # if multiple appends, dont close it just yet...
                print ">"

if len(closingtags) != 0: # close up if forgotten...
    for tag in closingtags:
        print "</%s>" % tag

print "</%s>" %root





