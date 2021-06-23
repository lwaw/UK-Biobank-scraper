# UK Biobank scraper

  A script that will download meta-data from the UK Biobank website (https://www.ukbiobank.ac.u).

## Description

  This tool will download meta-data for all features that are given as input. The output will be a text file contaig the meta data as json strings. The following data will be collected for each feature:

  * Name
  * Description
  * Notes
  * Participants
  * item count
  * Stability
  * Value type
  * Item type
  * Strata
  * Sexed
  * Instances (dictionary)
    * Type
    * Instance date
  * Dates (dictionary)
    * Debut date
    * Version date
  * Categories (list (dictionaries))
  * Related data field (dictionaries (list))
  * Resources (dicionary)
  * Data coding (dictionary)

### Example input

```
19-0.0
21-0.0
21-1.0
21-2.0
20078-2.0
20002-0.0
```

### Example output

```
{"column": "19-0.0", "description": "Heel ultrasound method", "notes": "Method used for the Ultrasound Bone Densitometry of heel", "participants": "324,753", "item_count": "324,753", "stability": "Complete", "value_type": "Categorical (single)", "item_type": "Data", "strata": "Primary", "sexed": "Both sexes", "instances": {"instances": "Defined (1)", "instance_date": ""}, "dates": {"debut_date": "Jan 2012", "version_date": "Jan 2012"}, "categories": [{"100018": "Bone-densitometry of heel", "706": "Physical measures", "100006": "Physical measures", "100000": "UK Biobank Assessment Centre"}], "related_data_fields": {"3081": ["Foot measured for bone density", "indicates which foot is described in Current Field"], "4092": ["Heel ultrasound method (left)", "is a successor question to Current Field"], "4095": ["Heel ultrasound method (right)", "is a successor question to Current Field"]}, "resources": {"100116": "Bone densitometry in progress", "100191": "Screenshot of automated bone densitometry", "100117": "Setting up bone densitometry", "100248": "Ultrasound heel bone densitometry using ACE"}, "data_coding": {"data_coding_id": "100260", "data_coding_types": {"1": "Direct entry", "2": "Manual entry", "6": "Not performed - equipment failure", "7": "Not performed - other reason", "3": "Not performed"}}}
```

## Getting Started

### Dependencies

  * from urllib
  * sys
  * re
  * datetime
  * json

### Executing program

```
python3 UKBiobank_scraper.py input.txt output.txt
```

* * * * *

Version: 1.0

This project is licensed under the terms of the Creative Commons
Attribution-ShareAlike 4.0 International Public License license

Copyright 2021, Laurens Edwards, All rights reserved.


* * * * *



