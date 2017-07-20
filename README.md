# ODS
This is Pandoc's 'filter', that write .ODS files from Pandoc-json object.
Usage:

*python odswritter.py inputfile outputfile.ods -s N*

where is - N - your integer - header level, that separate sheets. 



More information:
1) **Do not** use this filter with complex table (pandoc can not work with complex table, filter get wrong json object and write wrong result).
2) Complex table is: 
 - table with **MERGED CELLS** in row or/and column. (impossibles because of pandoc)
 - tables with bullet list, ordered list inside 
 - tables with tables inside 
3) Pandoc ignores align.
4) Pandoc replaces underline with italic. 
5) Use 'styles.ods' to set your own styles
6) **DO NOT** change styles names
7) If you need more headers just define them in 'styles.ods' and name "header" + "*N*". (Example: "header6" "header2545") 
