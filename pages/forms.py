from django import forms
import re, json

# Command input
class CommandForm(forms.Form):
    command = forms.CharField(label='指令', required=True)

# ID input
class IdForm(forms.Form):
    id = forms.CharField(label='ID', required=True)

# Notanote B26 calculator
class NanBestForm(forms.Form):
    with open('static/pages/notanote/notanote_chart_info.json', encoding='utf-8') as file:
        data = json.loads(file.read())
        initial = ''
        for item in list(data.items()):
            song = item[0]
            for chart in list(item[1].items()):
                level = chart[0]
                difficulty = chart[1]
                initial += f'{song},,,{level},,,-,,,0\r\n'
        intial = initial.rstrip()
    ranks = forms.CharField(widget=forms.Textarea(attrs={'rows': 30, 'cols': 50}), label='', initial=initial, required=True)

# Notanote B21 calculator (v1.7.0)
class NanBestForm_v1_7_0(forms.Form):
    with open('static/pages/notanote/notanote_chart_info_v1.7.0.json', encoding='utf-8') as file:
        data = json.loads(file.read())
        initial = ''
        for item in list(data.items()):
            song = item[0]
            for chart in list(item[1].items()):
                level = chart[0]
                difficulty = chart[1]
                initial += f'{song},,,{level},,,-,,,0\r\n'
        intial = initial.rstrip()
    ranks = forms.CharField(widget=forms.Textarea(attrs={'rows': 30, 'cols': 50}), label='', initial=initial, required=True)

# Notanote single rank calculator
class NanRankCalcForm(forms.Form):
    difficulty = forms.FloatField(label='', required=True)
    acc = forms.FloatField(label='', required=True)

# Random number
class RandomNumForm(forms.Form):
    min = forms.FloatField(label='', initial=0, required=True)
    max = forms.FloatField(label='', initial=10, required=True)
    decimal_places = forms.IntegerField(label='', initial=1, required=True)
