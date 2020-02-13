# csv2json.py
#
# Copyright 2009 Brian Gershon -- briang at webcollective.coop
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import getopt
import csv
from os.path import dirname
import simplejson




def convert(input, output, modelName):
    in_file = dirname(__file__) + input
    out_file = dirname(__file__) + output + ".json"


    f = open(in_file, 'r' )
    fo = open(out_file, 'w')

    reader = csv.reader( f )

    header_row = []
    entries = []

    # debugging
    # if model_name == 'app_airport.Airport':
    #     import pdb ; pdb.set_trace( )

    for row in reader:
        if not header_row:
            header_row = row
            continue

        pk = row[0]
        model = modelName
        fields = {}
        for i in range(len(row)-1):
            active_field = row[i+1]

            # convert numeric strings into actual numbers by converting to either int or float
            if active_field.isdigit():
                try:
                    new_number = int(active_field)
                except ValueError:
                    new_number = float(active_field)
                fields[header_row[i+1]] = new_number
            else:
                fields[header_row[i+1]] = active_field.strip()

        row_dict = {}
        row_dict["pk"] = int(pk)
        row_dict["model"] = modelName

        row_dict["fields"] = fields
        entries.append(row_dict)

    fo.write("%s" % simplejson.dumps(entries, indent=4))

    f.close()
    fo.close()

convert(input="dummyDefib.csv", output="mainApp/fixtures/items", modelName="mainApp.items")
convert(input="community_ids.csv", output="mainApp/fixtures/communities", modelName="mainApp.communities")
convert(input="types.csv", output="mainApp/fixtures/type", modelName="mainApp.type")
convert(input="data/user.csv", output="mainApp/fixtures/user", modelName="auth.user")
convert(input="data/userprofileinfo.csv", output="mainApp/fixtures/userprofileinfo", modelName="mainApp.UserProfileInfo")
#python file
