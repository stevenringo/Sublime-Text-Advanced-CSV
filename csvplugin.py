# Originally written by Eric Martel (emartel@gmail.com / www.ericmartel.com)
# Improved by Wade Brainerd (wadetb@gmail.com / www.wadeb.com)

# TODO
# + GetColumnIndexFromCursor doesn't handle quotes etc.
# + Restore selection after operation.

import sublime
import sublime_plugin

class SortDirection:
    Ascending = 1
    Descending = 2

class CSVValue:
    def __init__(self, text):
        self.text = text

    def AsFloat(self):
        try:
            return True, float(self.text)
        except ValueError:
            return False, None

    def Compare(self, other):
        a_is_float, a_float = self.AsFloat()
        b_is_float, b_float = other.AsFloat()

        if a_is_float and b_is_float:
            return a_float - b_float

        if self.text > other.text:
            return 1
        if self.text < other.text:
            return -1
        return 0

    def __lt__(self, other): return self.Compare(other) < 0
    def __eq__(self, other): return self.Compare(other) == 0

class CSVMatrix:
    def __init__(self):
        self.rows = []
        self.num_columns = 0
        self.valid = False
        self.delimiter = ','

    def AddRow(self, row):
        self.rows.append(row)

    def Finalize(self):
        if not len(self.rows):
            return

        self.num_columns = 0
        for row in self.rows:
            if len(row) > self.num_columns:
                self.num_columns = len(row)

        self.valid = True

    def GetCellValue(row, column_index):
        try:
            return row[column_index]
        except IndexError:
            return CSVValue('')

    def SortByColumn(self, column_index, direction, use_header):
        class Compare:
            def __init__(self, row): self.value = CSVMatrix.GetCellValue(row, column_index)
            def __lt__(self, other): return self.value < other.value
            def __eq__(self, other): return self.value == other.value

        reverse = direction == SortDirection.Descending

        if use_header:
            self.rows[1:] = sorted(self.rows[1:], key=lambda row: Compare(row), reverse=reverse)
        else:
            self.rows.sort(key=lambda row: Compare(row), reverse=reverse)

    def InsertColumn(self, column_index):
        for row in self.rows:
            if column_index <= len(row):
                row.insert(column_index, CSVValue(''))

    def DeleteColumn(self, column_index):
        for row in self.rows:
            if column_index < len(row):
                row.pop(column_index)

    def QuoteText(self, text):
        if self.delimiter in text or '"' in text:
            return '"' + text.replace('"', '""') + '"'
        else:
            return text

    def GetColumnWidths(self):
        column_widths = [0] * self.num_columns

        for row in self.rows:
            for column_index, value in enumerate(row):
                text = self.QuoteText(value.text)
                width = len(text)

                if width > column_widths[column_index]:
                    column_widths[column_index] = width

        return column_widths

    def Format(self):
        output = ''

        for row in self.rows:
            row_text = ''

            for column_index, value in enumerate(row):
                quoted_text = self.QuoteText(value.text)

                row_text += quoted_text

                if column_index < len(row) - 1:
                    row_text += self.delimiter

            output += row_text + '\n'

        return output

    def FormatCompacted(self):
        output = ''

        for row in self.rows:
            row_text = ''

            for column_index, value in enumerate(row):
                quoted_trimmed_text = self.QuoteText(value.text).strip()

                row_text += quoted_trimmed_text

                if column_index < len(row) - 1:
                    row_text += self.delimiter

            output += row_text + '\n'

        return output

    def FormatExpanded(self):
        column_widths = self.GetColumnWidths()

        output = ''

        for row in self.rows:
            row_text = ''

            for column_index, value in enumerate(row):
                quoted_text = self.QuoteText(value.text)

                column_width = column_widths[column_index]

                quoted_padded_text = quoted_text.ljust(column_width)

                row_text += quoted_padded_text

                if column_index < len(row) - 1:
                    row_text += self.delimiter

            output += row_text + '\n'

        return output

    # not done through regex for clarity and control
    # not done using csv module to have better control over what happens with the quotes
    def ParseRow(self, row):
        columns = []
        currentword = ''
        insidequotes = False

        for char_index, char in enumerate(row):
            if char == '"':
                if char_index < len(row) - 1 and row[char_index + 1] == '"':
                    currentword += '"'
                    continue

            if insidequotes:
                if char == '"':
                    insidequotes = False
                else:
                    currentword += char

            else:
                if char == '"':
                    insidequotes = True

                elif char == self.delimiter:
                    columns.append(CSVValue(currentword))
                    currentword = ''

                else:
                    currentword += char

        columns.append(CSVValue(currentword))

        return columns

    def FromText(text):
        matrix = CSVMatrix()

        for line in text.split("\n"):
            if len(line.strip()):
                row = matrix.ParseRow(line)

                matrix.AddRow(row)

        matrix.Finalize()

        return matrix

    def FromView(view):
        text = view.substr(sublime.Region(0, view.size()))

        return CSVMatrix.FromText(text)

def GetColumnIndexFromCursor(view):
    selection = view.sel()[0]
    # find which column we're working on
    wordrange = view.word(selection)
    linerange = view.line(selection)
    wordbegin = min(wordrange.a, wordrange.b)
    linebegin = min(linerange.a, linerange.b)
    leadingtowordregion = sublime.Region(linebegin, wordbegin)
    leadingtoword = view.substr(leadingtowordregion)
    column_index = leadingtoword.count(',')
    return column_index

class CsvSetOutputCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        if(args['output'] != None):
            self.view.replace(edit, sublime.Region(0, self.view.size()), args['output']);

class CsvSortByColCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.view = self.window.active_view()

        self.matrix = CSVMatrix.FromView(self.view)
        if not self.matrix.valid:
            sublime.error_message(__name__ + ": The buffer doesn't appear to be a CSV file")
            return

        self.column_index = GetColumnIndexFromCursor(self.view)

        self.window.show_quick_panel(['Ascending', 'Descending'], self.on_select_direction_done)

    def on_select_direction_done(self, picked):
        if picked >= 0:
            directions = [SortDirection.Ascending, SortDirection.Descending]
            self.direction = directions[picked]

            sublime.set_timeout(lambda: self.window.show_quick_panel(['Use header row', 'Don\'t use header row'], self.on_select_header_done), 10)

    def on_select_header_done(self, picked):
        if picked >= 0:
            use_header = picked == 0

            self.matrix.SortByColumn(self.column_index, self.direction, use_header)
            
            output = self.matrix.Format()

            self.view.run_command('csv_set_output', {'output': output});

class CsvInsertColCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        matrix = CSVMatrix.FromView(self.view)
        if not matrix.valid:
            sublime.error_message(__name__ + ": The buffer doesn't appear to be a CSV file")
            return

        column_index = GetColumnIndexFromCursor(self.view)

        matrix.InsertColumn(column_index)

        output = matrix.Format()

        self.view.replace(edit, sublime.Region(0, self.view.size()), output);

class CsvDeleteColCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        matrix = CSVMatrix.FromView(self.view)
        if not matrix.valid:
            sublime.error_message(__name__ + ": The buffer doesn't appear to be a CSV file")
            return

        column_index = GetColumnIndexFromCursor(self.view)

        matrix.DeleteColumn(column_index)

        output = matrix.Format()

        self.view.replace(edit, sublime.Region(0, self.view.size()), output);

class CsvFormatCompactCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        matrix = CSVMatrix.FromView(view)
        if not matrix.valid:
            sublime.error_message(__name__ + ": The buffer doesn't appear to be a CSV file")
            return

        output = matrix.FormatCompacted()

        view.run_command('csv_set_output', {'output': output});

class CsvFormatExpandCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        matrix = CSVMatrix.FromView(view)
        if not matrix.valid:
            sublime.error_message(__name__ + ": The buffer doesn't appear to be a CSV file")
            return

        output = matrix.FormatExpanded()

        view.run_command('csv_set_output', {'output': output});
