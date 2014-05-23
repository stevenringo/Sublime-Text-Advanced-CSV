# Sublime Text 3 CSV Plugin

A plugin to manage CSV files, forked from Eric Martel's Sublime-Text-2-CSV-Plugin at ericmartel/Sublime-Text-2-CSV-Plugin.

It's often easiest to work with CSV data when the columns are properly lined up.  This plugin provides a command to line up all the columns using spaces ('Justify columns') and to collapse them back again ('Collapse columns').

It also includes features to insert and delete columns and to sort data by column, with or without a header row, and respecting numeric order and lexigraphical order as appropriate.  All cells in a column may be block selected, allowing 

The plugin includes a feature to clean up empty trailing commas from rows, which are often left when opening a CSV file in Excel.

These features work in both justified and collapsed modes.

Finally, the plugin has full support for RFC 4180 quoting.

## Install

The files can be obtained on github:

    $ https://github.com/wadetb/Sublime-Text-3-CSV-Plugin

## Key bindings

Key                 | Action
------------------- | ----------------
`Ctrl+Comma, Up`    | Sort ascending
`Ctrl+Comma, Down`  | Sort descending
`Ctrl+Comma, i`     | Insert column
`Ctrl+Comma, d`     | Delete column
`Ctrl+Comma, s`     | Select column
`Ctrl+Comma, Space` | Justify columns
`Ctrl+Comma, Comma` | Content Cell

# License

All of Sublime Text 3 CSV Plugin is licensed under the MIT license.

Copyright (c) 2014 Wade Brainerd <wadeb@wadeb.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Further, portions of the code taken from Eric Martel's Sublime Text 2 plugin are licensed as follows:

All of Sublime Text 2 CSV Plugin is licensed under the MIT license.

Copyright (c) 2012 Eric Martel <emartel@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.