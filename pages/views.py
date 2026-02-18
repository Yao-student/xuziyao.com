from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
from django.conf import settings

import re
import requests
from io import BytesIO
import base64
from matplotlib import pyplot as plt
plt.switch_backend('agg')
from datetime import datetime
import json
import random

# Index
def index(request):
    latest_posts = Post.objects.all().order_by('-date')[:5]
    context = {'latest_posts': latest_posts}
    return render(request, 'pages/index.html', context)

# Changelog
def changelog(request):
    return render(request, 'pages/changelog.html')

# Self-introduction
def introduction(request):
    return render(request, 'pages/introduction.html')

# Special Thanks
def special_thanks(request):
    return render(request, 'pages/special_thanks.html')

# Fanmade Charts
def fanmade_charts(request):
    return render(request, 'pages/fanmade_charts/index.html')

# Phigros Fanmade Charts
def fanmade_charts_phigros(request):
    charts = PhigrosFanmadeChart.objects.all()
    context = {'charts': charts}
    return render(request, 'pages/fanmade_charts/phigros.html', context)

# Phira Tools
def phira(request):
    return render(request, 'pages/phira/index.html')

# Phira Chart Ranking
def phira_ranking(request):
    figure = ''
    errors = []
    if request.method == 'POST':
        # Recognize the command
        command = request.POST.get('command')
        parameter = ''
        # All charts
        if re.match(r'^all', command):
            api_url = 'https://api.phira.cn/chart?'
            title = ''
        # Stable charts
        elif re.match(r'^stable', command):
            api_url = 'https://api.phira.cn/chart?stable=stb'
            title = '上架'
        # Ranked charts
        elif re.match(r'^ranked', command):
            api_url = 'https://api.phira.cn/chart?stable=ranked'
            title = '计分'
        # Unranked charts
        elif re.match(r'^unranked', command):
            api_url = 'https://api.phira.cn/chart?stable=unranked'
            title = '不计分'
        # 6thPecJam charts
        elif re.match(r'^6pj', command):
            api_url = 'https://api.phira.cn/chart?tags=6thPecJam'
            title = '6thPecJam '
        else:
            errors.append('指令错误')
        # Position limited
        if re.match(r'^(all|stable|ranked|unranked|6pj) \d+,\d+$', command):
            start, end = re.search(r'\d+,\d+$', command).group().split(',')
            start, end = int(start), int(end)
            parameter = ''
            title += f'第{start}~{end}名'
        # Position and rating limited
        elif re.match(r'^(all|stable|ranked|unranked|6pj) \d+(\.\d+)?-\d+(\.\d+)? \d+,\d+$', command):
            lowest, highest = re.search(r'\d+(\.\d+)?-\d+(\.\d+)?(?= \d+,\d+$)', command).group().split('-')
            lowest, highest = float(lowest), float(highest)
            start, end = re.search(r'\d+,\d+$', command).group().split(',')
            start, end = int(start), int(end)
            parameter = f'&rating={lowest / 5},{highest / 5}'
            title += f'{lowest}~{highest}分第{start}~{end}名'
        else:
            errors.append('指令错误')
        if not errors:
            # Read the data
            names, ratings = [], []
            page = (start - 1) // 30
            while True:
                page += 1
                req = requests.get(f'{api_url}&page={page}&order=-rating{parameter}', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
                result = req.json()['results'][start - 1:end]
                for chart in result:
                    names.append(f'(ID:{chart['id']})   {chart['name']} {chart['level']} {chart['difficulty']:.1f}')
                    ratings.append(round(chart['rating'] * 5, 3)) if chart['rating'] else ratings.append(0)
                if len(names) >= end:
                    break
            # Sort charts
            names = names[start - 1:end][::-1]
            ratings = ratings[start - 1:end][::-1]
            time = datetime.strftime(datetime.today(), '%m-%d %H:%M')
            # Generate the figure
            if len(names) < 20:
                size = (15, 5)
            elif len(names) < 60:
                size = (15, 10)
            else:
                size = (15, 20)
            plt.figure(figsize=size)
            bar_chart1 = plt.barh(names, ratings, color=['deepskyblue', 'lightskyblue', 'steelblue', 'dodgerblue', 'lightsteelblue', 'royalblue'])
            plt.xlim(left=ratings[0] - 0.02, right=ratings[-1] + (ratings[-1] - ratings[0]) / 5) if ratings[0] >= 1 else None
            plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'
            plt.title(f'{time} Phira {title}谱面评分排名', fontsize=20)
            plt.bar_label(bar_chart1, label_type='edge')
            buffer = BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)
            plt.close()
            figure = f"<img src=\"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('ascii')}\" style=\"max-width: 100%;border-radius: .3rem;\" />"
    context = {'figure': figure, 'errors': errors}
    return render(request, 'pages/phira/ranking.html', context)

# Phira Chart File Download
def phira_download(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        file_url = data['file-url']
        file = requests.get(file_url).content
        response = HttpResponse(content_type='application/octet-stream')
        response.write(file)
        return response
    return render(request, 'pages/phira/download.html')

# PhiZone Tools
def phizone(request):
    return render(request, 'pages/phizone/index.html')

# PhiZone Chart Ranking
def phizone_ranking(request):
    figure = ''
    errors = []
    if request.method == 'POST':
        # Recognize the command
        command = request.POST.get('command')
        parameter = ''
        # All charts
        if re.match(r'^all', command):
            api_url = 'https://api.phizone.cn/charts'
            title = ''
        # Ranked charts
        elif re.match(r'^ranked', command):
            api_url = 'https://api.phizone.cn/charts?isranked=true'
            title = '计分'
        # Unranked charts
        elif re.match(r'^unranked', command):
            api_url = 'https://api.phizone.cn/charts?isranked=false'
            title = '不计分'
        # 7thPecJam RG charts
        if re.match(r'^7pj rg', command):
            api_url = 'https://api.phizone.cn/events/divisions/a550e9cb-a1de-4885-bd08-6e85792ff1bc/entries/charts'
            title = '7thPecJam RG赛道'
        # 7thPecJam NL charts
        elif re.match(r'^7pj nl', command):
            api_url = 'https://api.phizone.cn/events/divisions/c7bd5d87-bbef-4ca4-b31e-fb6bb8e7e718/entries/charts'
            title = '7thPecJam NL赛道'
        else:
            errors.append('指令错误')
        # Position limited
        if re.match(r'^(all|stable|ranked|unranked|7pj (rg|nl)) \d+,\d+$', command):
            start, end = re.search(r'\d+,\d+$', command).group().split(',')
            start, end = int(start), int(end)
            if start >= end or start < 1:
                errors.append('最高排名大于最低排名或排名超出范围')
            title += f'第{start}~{end}名'
        # Position and rating limited
        elif re.match(r'^(all|stable|ranked|unranked|7pj (rg|nl)) \d+(\.\d+)?-\d+(\.\d+)? \d+,\d+$', command):
            lowest, highest = re.search(r'\d+(\.\d+)?-\d+(\.\d+)?(?= \d+,\d+$)', command).group().split('-')
            lowest, highest = float(lowest), float(highest)
            if lowest >= highest or not 0 <= lowest <= 5 or not 0 <= highest <= 5:
                errors.append('最低评分大于最高评分或评分超出0~5')
            start, end = re.search(r'\d+,\d+$', command).group().split(',')
            start, end = int(start), int(end)
            parameter = f'&minrating={lowest}&maxrating={highest}'
            title += f'{lowest}~{highest}分第{start}~{end}名'
        else:
            errors.append('指令错误')
        if not errors:
            names, ratings = [], []
            page = 0
            # Read the data
            while True:
                page += 1
                req = requests.get(f'{api_url}?page={page}&order=rating{parameter}')
                data = req.json()['data']
                if data:
                    for chart in data:
                        names.append(f'(ID:{chart['id'][:8]}…)   {chart['song']['title']} {chart['level']} {chart['difficulty']}')
                        ratings.append(round(chart['rating'], 3))
                else:
                    break
            names = names[-int(start):-int(end) - 1:-1][::-1]
            ratings = ratings[-int(start):-int(end) - 1:-1][::-1]
            time = datetime.strftime(datetime.today(), '%m-%d %H:%M')
            # Generate the figure
            if len(names) < 20:
                size = (15, 5)
            elif len(names) < 60:
                size = (15, 10)
            else:
                size = (15, 20)
            plt.figure(figsize=size)
            bar_chart = plt.barh(names, ratings, color=['deepskyblue', 'lightskyblue', 'steelblue', 'dodgerblue', 'lightsteelblue', 'royalblue'])
            plt.xlim(left=ratings[0] - 0.02, right=ratings[-1] + (ratings[-1] - ratings[0]) / 14) if ratings[0] >= 1 else None
            plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'
            plt.title(f'{time} PhiZone{title} 谱面评分排名', fontsize=20)
            plt.bar_label(bar_chart, label_type='edge')
            buffer = BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)
            plt.close()
            figure = f"<img src=\"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('ascii')}\" style=\"max-width: 100%;border-radius: .3rem;\" />"
    context = {'figure': figure, 'errors': errors}
    return render(request, 'pages/phizone/ranking.html', context)

# Phizone Chart Vote Info
def phizone_vote(request):
    return render(request, 'pages/phizone/vote.html')

# Notanote Tools
def notanote(request):
    return render(request, 'pages/notanote/index.html')

# Notanote B31 calculator
def notanote_best(request):
    if request.method == 'POST':
        return JsonResponse({'secretKey': 'secret', 'iv': 'secret'})
    else:
        return render(request, 'pages/notanote/best.html')

# Notanote B26 Calculator instruction
def notanote_best_instruction(request):
    return render(request, 'pages/notanote/best_instruction.html')

# Notanote Rank Calculator
def notanote_rank(request):
    return render(request, 'pages/notanote/rank.html')

# Notanote PC Download
def notanote_pcdownload(request):
    return render(request, 'pages/notanote/pcdownload.html')

# Notanote Wiki Test
def notanote_wikitest(request):
    return render(request, 'pages/notanote/wikitest.html')

# Random Number Generator
def randomnum(request):
    return render(request, 'pages/randomnum.html')

# Posts
def posts_index(request):
    posts = Post.objects.all().order_by('-date')
    context = {'posts': posts}
    return render(request, 'pages/posts/index.html', context)

# Posts single post
def posts(request, id):
    post = Post.objects.get(id=id)
    id = post.id
    title = post.title
    date = post.date
    tags = post.tags.split(',') if post.tags else []
    context = {'id': id, 'title': title, 'date': date, 'tags': tags}
    return render(request, f'pages/posts/{id}.html', context)

# 400
def bad_request(request):
    return render(request, '400.html')

# 403
def forbidden(request):
    return render(request, '403.html')

# 404
def not_found(request):
    return render(request, '404.html')

# 500
def internal_server_error(request):
    return render(request, '500.html')

# 502
def bad_gateway(request):
    return render(request, '502.html')
