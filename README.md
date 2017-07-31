# ODS
This is Pandoc's 'filter', that write .ODS files from Pandoc-json object.
Usage:

*python odswritter.py inputfile outputfile.ods -s N -r yourstyles.ods*

where is - N - integer, header level, that separate sheets. 
         - yourstyles.ods - .ods file you want to use as styles source.


More information:
1) **Do not** use this filter with complex table (pandoc can not work with complex table, filter get wrong or complex json object and write wrong result).
2) Complex tables are: 
 - tables with **MERGED CELLS** in row or/and column. (impossibles because of pandoc)
 - tables with bullet list, ordered list inside. 
 - tables with tables inside. 
 - tables with images inside.
3) Pandoc ignores align.
4) Pandoc replaces underline with italic.

More information about styles usage: 
1) Use 'styles.ods' in script directory to change default styles. **DO NOT** delete it.
2) If you create yourown styles, you should declare this ones:
 - 'tablehead' - for table's headers. Pandoc makes first row - header row usually.
 - 'tablebody' - for table content.
 - 'header1' - first level header.
 - ...
 - 'header55' - 55 level header (declare as many as you need).
 - 'text' - just simple text in text row.
 **ALWAYS USE THIS NAMES.**

