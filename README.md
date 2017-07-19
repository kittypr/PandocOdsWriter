# ODS
This is Pandoc's 'filter', that write .ODS files from Pandoc-json object.
Usage (with pipe only - we should send argument to filter!):

*pandoc yourFile.yourExtention -t json | python ODSwriter.py yourOutputFile.ods*

In this case, pandoc will show json to stdout.
Or you can continue to use json input:

*pandoc yourFile.yourExtention -t json | python ODSwriter.py yourOutputFile.ods | pandoc -f json -t whatYouWant -o ANOTHERoutputfile*

This filter sends the same json object it got.

More information:
1) **Do not** use the same output file in second case (pandoc will rewrite it).
2) **Do not** use this filter with complex table (pandoc can not work with complex table, filter get wrong json object and write wrong result).
3) Complex table is: 
 - table with **MERGED CELLS** in row or/and column. (impossibles because of pandoc)
 - tables with bullet list, ordered list inside 
 - tables with tables inside 
4) Pandoc ignores align.
5) Pandoc replaces underline with italic. 
6) Six levels of headers are supported 

All files begin with *"ods..."(lowcase)* - is ready library without dependenses, with little remarks for work with Python 3. **Author is Joseph Colton**
