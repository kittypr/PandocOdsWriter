# Title

## Header 

Text.Pandoc.Definition defines the Pandoc data structure, which is used by pandoc to represent structured documents. This module used to live in the pandoc package, but starting with pandoc 1.7, it has been split off, so that other packages can use it without drawing in all of pandoc's dependencies, and pandoc itself can depend on packages (like citeproc-hs) that use them.
 

+----------------+--------+-------------+---------+----------------+
|                |   2016 |      Apples | price   | Price change   |
+================+========+=============+=========+================+
| Green          |      1 |        6333 | 20$     | **+4%**        |
+----------------+--------+-------------+---------+----------------+
| Macintosh      |      2 |        2347 | 16$     | **+4%**        |
+----------------+--------+-------------+---------+----------------+
| Yellow         |      7 |       32363 | 9$      | **+2%**        |
+----------------+--------+-------------+---------+----------------+
| Watermellon    | 3      | 1231        | 8$      | **+1%**        |
+----------------+--------+-------------+---------+----------------+
| Apple          | 5      | 53462       | 2$      | 0%             |
+----------------+--------+-------------+---------+----------------+

