﻿from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *

import re
import requests
from decimal import Decimal
from io import BytesIO
import base64
from matplotlib import pyplot as plt
from datetime import datetime
from PIL import Image
import random

plt.switch_backend('agg')

# Calculate a expression with decimal numbers accurately with module 'decimal'
def decimalize(expr):
    return eval(re.sub(r'\d+(\.\d+)?', lambda matchobj: f'Decimal(\'{matchobj.group()}\')', expr))

# Homepage
def index(request):
    return render(request, 'pages/index.html')

# Self-introduction
def introduction(request):
    return render(request, 'pages/introduction.html')

# Phira tools index page
def phira(request):
    return render(request, 'pages/phira.html')

# Phira chart rating ranking info page
def prranking(request):
    figure = ''
    error = None
    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
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
                title = ' 6thPecJam'
            else:
                error = '指令错误'
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
                parameter = f'&rating={decimalize(f'{lowest} / 5')},{decimalize(f'{highest} / 5')}'
                title += f'{lowest}~{highest}分第{start}~{end}名'
            else:
                error = '指令错误'
            if not error:
                # Read the data
                names, ratings = [], []
                page = decimalize(f'({start} - 1) // 30')
                while True:
                    page += 1
                    req = requests.get(f'{api_url}&page={page}&order=-rating{parameter}', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
                    result = req.json()['results'][start - 1:end]
                    for chart in result:
                        names.append(f'(ID:{chart['id']})   {chart['name']} {chart['level']} {Decimal(f'{chart['difficulty']}').quantize(Decimal('0.0'))}')
                        ratings.append(decimalize(f'{chart['rating']} * 5').quantize(Decimal('0.000'))) if chart['rating'] else ratings.append(0)
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
                plt.xlim(left=ratings[0] - Decimal('0.02'), right=decimalize(f'{ratings[-1]} + ({ratings[-1]} - {ratings[0]}) / 5')) if ratings[0] >= 1 else None
                plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'
                plt.title(f'{time} Phira{title}谱面评分排名', fontsize=20)
                plt.bar_label(bar_chart1, label_type='edge')
                buffer = BytesIO()
                plt.savefig(buffer, format='png', bbox_inches='tight')
                buffer.seek(0)
                plt.close()
                figure = f"<img src='data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('ascii')}' />"
    else:
        form = CommandForm()
    context = {'form': form, 'figure': figure, 'error': error}
    return render(request, 'pages/prranking.html', context)

# Phira chart file getting
def prgetfile(request):
    error = None
    if request.method == 'POST':
        form = IdForm(request.POST)
        if form.is_valid():
            chart_id = request.POST.get('id')
            req = requests.get(f'https://api.phira.cn/chart/{chart_id}')
            if req.status_code != 400 and req.json() != {'error': 'Not found'}:
                file = requests.get(req.json()['file'], headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
                response = HttpResponse(content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{chart_id}.zip"'
                response.write(file)
                return response
            else:
                error = '谱面不存在'
    else:
        form = IdForm()
    context = {'form': form, 'error': error}
    return render(request, 'pages/prgetfile.html', context)

# PhiZone info index page
def phizone(request):
    return render(request, 'pages/phizone.html')

# PhiZone chart rating ranking info page
def pzranking(request):
    figure = ''
    error = None
    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
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
            # PecJam charts
            elif re.match(r'^\dpj (rg|nl)', command):
                # 7thPecJam RG charts
                if re.match(r'^7pj rg', command):
                    api_url = 'https://api.phizone.cn/events/divisions/a550e9cb-a1de-4885-bd08-6e85792ff1bc/entries/charts'
                    title = ' 7thPecJam RG赛道'
                # 7thPecJam NL charts
                elif re.match(r'^7pj nl', command):
                    api_url = 'https://api.phizone.cn/events/divisions/c7bd5d87-bbef-4ca4-b31e-fb6bb8e7e718/entries/charts'
                    title = ' 7thPecJam NL赛道'
                else:
                    error = '指令错误'
            else:
                error = '指令错误'
            # Position limited
            if re.match(r'^(all|\dpj (rg|nl)) \d+,\d+$', command):
                start, end = re.search(r'\d+,\d+$', command).group().split(',')
                start, end = int(start), int(end)
                if start >= end or start < 1:
                    error = '最高排名大于最低排名或排名超出范围'
                title += f'第{start}~{end}名'
            # Position and rating limited
            elif re.match(r'^(all|stable|ranked|unranked|\dpj (rg|nl)) \d+(\.\d+)?-\d+(\.\d+)? \d+,\d+$', command):
                lowest, highest = re.search(r'\d+(\.\d+)?-\d+(\.\d+)?(?= \d+,\d+$)', command).group().split('-')
                lowest, highest = float(lowest), float(highest)
                if lowest >= highest or not 0 <= lowest <= 5 or not 0 <= highest <= 5:
                    error = '最低评分大于最高评分或评分超出0~5'
                start, end = re.search(r'\d+,\d+$', command).group().split(',')
                start, end = int(start), int(end)
                parameter = f'&minrating={lowest}&maxrating={highest}'
                title += f'{lowest}~{highest}分第{start}~{end}名'
            else:
                error = '指令错误'
            if not error:
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
                            ratings.append(Decimal(f'{chart['rating']}').quantize(Decimal('0.000')))
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
                plt.xlim(left=ratings[0] - Decimal('0.02'), right=decimalize(f'{ratings[-1]} + ({ratings[-1]} - {ratings[0]}) / 14')) if ratings[0] >= 1 else None
                plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'
                plt.title(f'{time} PhiZone{title}谱面评分排名', fontsize=20)
                plt.bar_label(bar_chart, label_type='edge')
                buffer = BytesIO()
                plt.savefig(buffer, format='png', bbox_inches='tight')
                buffer.seek(0)
                plt.close()
                figure = f"<img src='data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('ascii')}' />"
    else:
        form = CommandForm()
    context = {'form': form, 'figure': figure, 'error': error}
    return render(request, 'pages/pzranking.html', context)

# Phizone chart vote info page
def pzvote(request):
    # Phizone vote class
    class PzVote:
        def __init__(self, owner, owner_id, multiplier, arrangement, gameplay, visual_effects, creativity, concord, impression):
            self.owner = owner
            self.owner_id = owner_id
            self.multiplier = multiplier
            self.arrangement = arrangement
            self.gameplay = gameplay
            self.visual_effects = visual_effects
            self.creativity = creativity
            self.concord = concord
            self.impression = impression
            self.total = decimalize(f'{multiplier} * {arrangement + gameplay + visual_effects + creativity + concord + impression}')

    chart_info = None
    votes = None
    total = None
    error = None
    if request.method == 'POST':
        form = IdForm(request.POST)
        if form.is_valid():
            chart_id = request.POST.get('id')
            # Get chart info
            req = requests.get(f'https://api.phizone.cn/charts/{chart_id}')
            if req.status_code != 404 and req.json()['code'] != 'ResourceNotFound':
                data = req.json()['data']
                chart_info = (
                    f'曲名：{data['song']['title']}',
                    f'谱师：{re.sub(r'\[PZUser:(\d+):([^\s]+?):PZRT]', r'<a href="https://www.phizone.cn/users/\1">\2</a>', data['authorName'])}',
                    f'难度：{data['level']} {data['difficulty']}',
                    f'评分：{decimalize(str(data['rating'])).quantize(Decimal('0.000'))}'
                )
                total = PzVote(
                    '总计', '', 1,
                    decimalize(f'{data['ratingOnArrangement']}').quantize(Decimal('0.000')),
                    decimalize(f'{data['ratingOnGameplay']}').quantize(Decimal('0.000')),
                    decimalize(f'{data['ratingOnVisualEffects']}').quantize(Decimal('0.000')),
                    decimalize(f'{data['ratingOnCreativity']}').quantize(Decimal('0.000')),
                    decimalize(f'{data['ratingOnConcord']}').quantize(Decimal('0.000')),
                    decimalize(f'{data['ratingOnImpression']}').quantize(Decimal('0.000'))
                )
                # Get chart vote info
                req = requests.get(f'https://api.phizone.cn/charts/{chart_id}/votes')
                data = req.json()['data']
                votes = []
                for vote in data:
                    req = requests.get(f'https://api.phizone.cn/users/{vote['ownerId']}')
                    owner = req.json()['data']['userName']
                    votes.append(PzVote(owner, vote['ownerId'], vote['multiplier'], vote['arrangement'], vote['gameplay'], vote['visualEffects'], vote['creativity'], vote['concord'], vote['impression']))
            else:
                error = '谱面不存在'
    else:
        form = IdForm()
    context = {'form': form, 'chart_info': chart_info, 'votes': votes, 'total': total, 'error': error}
    return render(request, 'pages/pzvote.html', context)

# PhiZone B19 info
def pzbest(request):
    # PhiZone B19 class
    class PzBest():
        def __init__(self, index, song, difficulty, chart_id, score, acc, perfect, early, late, bad, miss, rks):
            self.index = index
            self.song = song
            self.difficulty = difficulty
            self.chart_id = chart_id
            self.score = score
            self.acc = acc
            self.perfect = perfect
            self.good = early + late
            self.early = early
            self.late = late
            self.bad = bad
            self.miss = miss
            self.rks = rks
    
    def get_best_info(index, record):
        song = record['chart']['song']['title']
        difficulty = f'{record['chart']['level']} {record['chart']['difficulty']}'
        chart_id = record['chart']['id']
        score = record['score']
        acc = decimalize(f'{record['accuracy']} * 100').quantize(Decimal('0.000'))
        perfect = record['perfect']
        early = record['goodEarly']
        late = record['goodLate']
        bad = record['bad']
        miss = record['miss']
        rks = decimalize(str(record['rks'])).quantize(Decimal('0.000'))
        return PzBest(index, song, difficulty, chart_id, score, acc, perfect, early, late, bad, miss, rks)

    rks = None
    b0 = None
    b19 = []
    error = None
    if request.method == 'POST':
        form = IdForm(request.POST)
        if form.is_valid():
            user_id = request.POST.get('id')
            rks = decimalize(str(requests.get(f'https://api.phizone.cn/users/{user_id}').json()['data']['rks'])).quantize(Decimal('0.000'))
            req = requests.get(f'https://api.phizone.cn/users/{user_id}/personalBests')
            if req.status_code != 404 and req.json()['code'] != 'UserNotFound':
                data = req.json()['data']
                if data['phi1']:
                    b0 = get_best_info(0, data['phi1'])
                if data['best19']:
                    b19 = [get_best_info(i + 1, record) for i, record in enumerate(data['best19'])]
            else:
                error = '用户不存在'
    else:
        form = IdForm()
    context = {'form': form, 'rks': rks, 'b0': b0, 'b19': b19, 'error': error}
    return render(request, 'pages/pzbest.html', context)

# Notanote Tools
def notanote(request):
    return render(request, 'pages/notanote.html')

# Notanote B21 calculator
def nanbest(request):
    # Notanote rank class
    class Rank():
        def __init__(self, index, song, level, difficulty, acc, rank):
            self.index = index
            self.song = song
            self.level = level
            self.difficulty = difficulty
            self.acc = acc
            self.rank = rank
    
    b21 = []
    overflow = []
    nrk = None
    errors = []
    if request.method == 'POST':
        form = NanBestForm(request.POST)
        if form.is_valid():
            info = request.POST.get('ranks').strip().split('\r\n')
            rank_list = []
            try:
                for chart in info:
                    song, level, difficulty, acc = chart.split(',,,')
                    try:
                        difficulty, acc = float(difficulty), float(acc)
                    except ValueError:
                       errors.append(f'{song} {level}的准确率不是数字。')
                    finally:
                        pass
                    # Calculate ranks of every songs
                    if 0 < acc <= 100:
                        rank = decimalize(f'({acc} / 100) ** 1.75 / (2 - {acc} / 100) * ({difficulty} + 5)')
                        rank_list.append(Rank(0, song, level, difficulty, acc, rank.quantize(Decimal('0.000'))))
                    elif acc == 0:
                        pass
                    else:
                        errors.append(f'{song} {level}的准确率不在0~100之间。')
            except:
                errors.append('信息错误。')
            else:
                if not errors:
                    # Calculate the Nrk
                    sorted_ranks = sorted(rank_list, key=lambda rank: rank.rank, reverse=True)
                    b21 = sorted_ranks[:21]
                    for index, rank in enumerate(b21):
                        rank.index = index + 1
                    overflow = sorted_ranks[21:31]
                    for index, rank in enumerate(overflow):
                        rank.index = index + 22
                    # Get the sum of several ranks
                    def get_rank_sum(start, end):
                        if start >= len(b21):
                            return 0
                        if end > len(b21):
                            end = -1
                        addends = list(map(lambda rank: rank.rank, b21[start:end]))
                        sum = 0
                        for addend in addends:
                            sum += Decimal(str(addend))
                        return sum
                    nrk = decimalize(f'0.1 * {b21[0].rank} + 0.08 * {get_rank_sum(1, 5)} + 0.07 * {get_rank_sum(5, 9)} + 0.05 * {get_rank_sum(9, 13)} + 0.03 * {get_rank_sum(13, 17)} + 0.02 * {get_rank_sum(17, 21)}').quantize(Decimal('0.000'))
            finally:
                pass
    else:
        form = NanBestForm()
    context = {'form': form, 'b21': b21, 'overflow': overflow, 'nrk': nrk, 'errors': errors}
    return render(request, 'pages/nanbest.html', context)

# Notanote single rank calculator
def nanrankcalc(request):
    rank = []
    errors = []
    if request.method == 'POST':
        form = NanRankCalcForm(request.POST)
        if form.is_valid():
            difficulty = float(request.POST.get('difficulty'))
            acc = float(request.POST.get('acc'))
            if 0 <= acc <= 100:
                rank = decimalize(f'({acc} / 100) ** 1.75 / (2 - {acc} / 100) * ({difficulty} + 5)').quantize(Decimal('0.000'))
            else:
                errors.append('准确率不在0~100之间。')
    else:
        form = NanRankCalcForm()
    context = {'form': form, 'rank': rank, 'errors': errors}
    return render(request, 'pages/nanrankcalc.html', context)

# Notanote chart constants
def nanconstants(request):
    return render(request, 'pages/nanconstants.html')

# Random number generator
def random_num(request):
    random_num = None
    errors = []
    if request.method == 'POST':
        form = RandomNumForm(request.POST)
        if form.is_valid():
            min = float(request.POST.get('min'))
            max = float(request.POST.get('max'))
            decimal_places = int(request.POST.get('decimal_places'))
            if min < max:
                random_num = Decimal(f'{random.uniform(min, max)}').quantize(Decimal(f'{10 ** -decimal_places}'))
            else:
                errors.append('最小值必须小于最大值。')
    else:
        form = RandomNumForm()
    context = {'form': form, 'errors': errors,'random_num': random_num}
    return render(request, 'pages/randomnum.html', context)

# Diary index page
def diaries_index(request):
    diaries = Diary.objects.all()
    context = {'diaries': diaries}
    return render(request, 'pages/diaries_index.html', context)

# Diary
def diaries(request, id):
    diary = Diary.objects.get(id=id)
    id = diary.id
    title = diary.title
    date = diary.date
    context = {id: 'id', 'title': title, 'date': date}
    return render(request, f'pages/diaries/{id}.html', context)

# Programming index page
def programming_index(request):
    articles = Programming.objects.all()
    context = {'articles': articles}
    return render(request, 'pages/programming_index.html', context)

# Programming
def programming(request, id):
    article = Programming.objects.get(id=id)
    id = article.id
    title = article.title
    date = article.date
    context = {id: 'id', 'title': title, 'date': date}
    return render(request, f'pages/programming/{id}.html', context)

# The 400 page
def bad_request(request):
    return render(request, '400.html')

# The 403 page
def forbidden(request):
    return render(request, '403.html')

# The 404 page
def not_found(request):
    return render(request, '404.html')

# The 500 page
def internal_server_error(request):
    return render(request, '500.html')

# The 502 page
def bad_gatway(request):
    return render(request, '502.html')
