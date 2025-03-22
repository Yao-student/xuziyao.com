from django import forms
import re, json

# Command input
class CommandForm(forms.Form):
    command = forms.CharField(label='指令', required=False)

# ID input
class IdForm(forms.Form):
    id = forms.CharField(label='ID', required=False)

# Notanote B21 calculator
class NanBestForm(forms.Form):
    with open('static/pages/notanote/nan_chart_info.json', encoding='utf-8') as file:
        chart_list = json.loads(file.read())
        initial = ''.join([f'{chart['song']},,,{chart['class']},,,{chart['difficulty']},,,0\r\n' for chart in chart_list]).rstrip()
    ranks = forms.CharField(widget=forms.Textarea(attrs={'rows': 30, 'cols': 50}), label='', initial=initial, required=False)

# Notanote single rank calculator
class NanRankCalcForm(forms.Form):
    difficulty = forms.FloatField(label='', required=False)
    acc = forms.FloatField(label='', required=False)

# Random number
class RandomNumForm(forms.Form):
    min = forms.FloatField(label='', initial=0, required=False)
    max = forms.FloatField(label='', initial=10, required=False)
    decimal_places = forms.IntegerField(label='', initial=1, required=False)