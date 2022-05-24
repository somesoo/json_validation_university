# json_validation_university

What it is about?
In a bigger project I was creating a script that generates to extra files, and then I automated it with Jenkins and GitLab to automaticly do some actions and create MR with new files that it has created.

to run script you need to type:

on linux: ```python3 runScript.py -- json_file canIDs.json --schema canIDsSchema.json --header_file text1.txt --visual_file text2.txt```

where `text1.txt` is the output headder file name

where `text2.txt` is the output file name for visualisation

and the output shoud be `nothing` if everything was completed, or `1` if there were some errors with address duplication or `line number` if .json file did not pass the validation

