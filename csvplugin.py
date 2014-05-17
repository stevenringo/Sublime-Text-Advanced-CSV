# Written by Eric Martel (emartel@gmail.com / www.ericmartel.com)

import sublime
import sublime_plugin

import threading
import os
import json

class SortDirection:
    Ascending = 1
    Descending = 2

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

    def SortByColumn(self, column_index, sortdirection):
        if sortdirection == SortDirection.Ascending:
            self.rows.sort(key=lambda row: row[column_index])
        else:
            self.rows.sort(key=lambda row: row[column_index], reverse=True)

    def FormatCompact(self, trailing_delimiters):
        output = ''

        for row in self.rows:
            for column_index in range(self.num_columns):
                if column_index < len(row):
                    column = row[column_index]

                    if column.find(self.delimiter) != -1 or column.find('"') != -1:
                        output += '"'
                        output += column.replace('"', '""')
                        output += '"'

                    else:
                        output += column

                if column_index < len(row) - 1 or trailing_delimiters:
                    output += self.delimiter

            output += '\n'

        return output

    # not done through regex for clarity and control
    # not done using csv module to have better control over what happens with the quotes
    def ParseRow(self, row, trim_whitespace):
        columns = []
        currentword = ''
        insidequotes = False
        pending_double_quote = False

        for char in row:
            if insidequotes:
                if char == '"':
                    if pending_double_quote:
                        currentword += '"'
                    insidequotes = False

                else:
                    currentword += char
                    pending_double_quote = False

            else:
                if char == '"':
                    insidequotes = True
                    pending_double_quote = True

                elif char == self.delimiter:
                    if trim_whitespace:
                        currentword = currentword.strip()
                    columns.append(currentword)
                    currentword = ''
                    continue

                else:
                    currentword += char

        # add the last word
        if trim_whitespace:
            currentword = currentword.strip()
        columns.append(currentword)

        return columns

    def FromText(text):
        matrix = CSVMatrix()

        for line in text.split("\n"):
            if len(line.strip()):
                row = matrix.ParseRow(line, True)

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

class CsvSortAscCurrentColCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        matrix = CSVMatrix.FromView(self.view)
        if not matrix.valid:
            sublime.error_message(__name__ + ": The buffer doesn't appear to be a CSV file")
            return

        column_index = GetColumnIndexFromCursor(self.view)

        matrix.SortByColumn(column_index, SortDirection.Ascending)

        output = matrix.FormatCompact(False)
        self.view.replace(edit, sublime.Region(0, self.view.size()), output);

class CsvSortDescCurrentColCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        matrix = CSVMatrix.FromView(self.view)
        if not matrix.valid:
            sublime.error_message(__name__ + ": The buffer doesn't appear to be a CSV file")
            return

        column_index = GetColumnIndexFromCursor(self.view)

        matrix.SortByColumn(column_index, SortDirection.Descending)
        
        output = matrix.FormatCompact(False)
        self.view.replace(edit, sublime.Region(0, self.view.size()), output);

class CsvSortAscPromptColCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.view = self.window.active_view()
        self.matrix = CSVMatrix.FromView(self.view)
        if not self.matrix.valid:
            sublime.error_message(__name__ + ": The buffer doesn't appear to be a CSV file")
            return

        self.window.show_quick_panel(self.matrix.rows[0], self.on_select_done)

    def on_select_done(self, picked):
        if picked >= 0:
            column_index = picked

            self.matrix.SortByColumn(column_index, SortDirection.Ascending)
            
            output = self.matrix.FormatCompact(False)

            self.view.run_command('csv_set_output', {'output': output});

class CsvSortDescPromptColCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.view = self.window.active_view()
        self.matrix = CSVMatrix.FromView(self.view)
        if not self.matrix.valid:
            sublime.error_message(__name__ + ": The buffer doesn't appear to be a CSV file")
            return

        self.window.show_quick_panel(self.matrix.rows[0], self.on_select_done)

    def on_select_done(self, picked):
        if picked >= 0:
            column_index = picked

            self.matrix.SortByColumn(column_index, SortDirection.Descending)
           
            output = self.matrix.FormatCompact(False)

            self.view.run_command('csv_set_output', {'output': output});

class CsvFormatCompactCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        matrix = CSVMatrix.FromView(view)
        if not matrix.valid:
            sublime.error_message(__name__ + ": The buffer doesn't appear to be a CSV file")
            return

        output = matrix.FormatCompact(False)

        view.run_command('csv_set_output', {'output': output});
