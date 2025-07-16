from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.conf import settings

import re
import requests
from io import BytesIO
import base64
from matplotlib import pyplot as plt
plt.switch_backend('agg')
from datetime import datetime
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import json
import math
import random

# Homepage
def index(request):
    return render(request, 'pages/index.html')

# Changelog
def changelog(request):
    return render(request, 'pages/changelog.html')

# Self-introduction
def introduction(request):
    return render(request, 'pages/introduction.html')

# Special thanks
def special_thanks(request):
    return render(request, 'pages/special_thanks.html')

# Fanmade charts
def fanmade_charts(request):
    return render(request, 'pages/fanmade_charts.html')

# Phigros fanmade charts
def fanmade_charts_phigros(request):
    charts = PhigrosFanmadeChart.objects.all()
    context = {'charts': charts}
    return render(request, 'pages/fanmade_charts_phigros.html', context)

# Phira tools index page
def phira(request):
    return render(request, 'pages/phira.html')

# Phira chart rating ranking info page
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
    return render(request, 'pages/phira_ranking.html', context)

# Phira chart file getting
def phira_download(request):
    errors = []
    if request.method == 'POST':
        chart_id = request.POST.get('chart-id')
        req = requests.get(f'https://api.phira.cn/chart/{chart_id}')
        if req.status_code != 400 and req.json() != {'errors': 'Not found'}:
            file = requests.get(req.json()['file'], headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
            response = HttpResponse(content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{chart_id}.pez"'
            response.write(file)
            return response
        else:
            errors.append('谱面不存在')
    context = {'errors': errors}
    return render(request, 'pages/phira_download.html', context)

# PhiZone info index page
def phizone(request):
    return render(request, 'pages/phizone.html')

# PhiZone chart rating ranking info page
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
    return render(request, 'pages/phizone_ranking.html', context)

# Phizone chart vote info page
def phizone_vote(request):
    # Phizone vote class
    class Vote:
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
            self.total = round(multiplier * arrangement + gameplay + visual_effects + creativity + concord + impression, 3)

    chart_info = None
    votes = None
    total = None
    errors = []
    if request.method == 'POST':
        chart_id = request.POST.get('chart-id')
        # Get chart info
        req = requests.get(f'https://api.phizone.cn/charts/{chart_id}')
        if req.status_code != 404 and req.json()['code'] != 'ResourceNotFound':
            data = req.json()['data']
            chart_info = (
                f'曲名：{data['song']['title']}',
                f'谱师：{re.sub(r'\[PZUser:(\d+):([^\s]+?):PZRT]', r'<a href="https://www.phizone.cn/users/\1">\2</a>', data['authorName'])}',
                f'难度：{data['level']} {data['difficulty']}',
                f'评分：{data['rating']:.3f}'
            )
            total = Vote(
                '总计', '', 1,
                round(data['ratingOnArrangement'], 3),
                round(data['ratingOnGameplay'], 3),
                round(data['ratingOnVisualEffects'], 3),
                round(data['ratingOnCreativity'], 3),
                round(data['ratingOnConcord'], 3),
                round(data['ratingOnImpression'], 3)
            )
            # Get chart vote info
            req = requests.get(f'https://api.phizone.cn/charts/{chart_id}/votes')
            data = req.json()['data']
            votes = []
            for vote in data:
                req = requests.get(f'https://api.phizone.cn/users/{vote['ownerId']}')
                owner = req.json()['data']['userName']
                votes.append(Vote(owner, vote['ownerId'], vote['multiplier'], vote['arrangement'], vote['gameplay'], vote['visualEffects'], vote['creativity'], vote['concord'], vote['impression']))
        else:
            errors.append('谱面不存在')
    context = {'chart_info': chart_info, 'votes': votes, 'total': total, 'errors': errors}
    return render(request, 'pages/phizone_vote.html', context)

# PhiZone B19 info
def phizone_best(request):
    # PhiZone B19 class
    class Record():
        def __init__(self, index, song, level, diff, chart_id, score, acc, perfect, early, late, bad, miss, rks):
            self.index = index
            self.song = song
            self.level = level
            self.diff = diff
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
            self.level_id = {0: 'ez', 1: 'hd', 2: 'in', 3: 'at', 4: 'sp'}[level]

    # Get record info
    def get_record_info(index, record):
        song = record['chart']['song']['title']
        level = record['chart']['levelType']
        diff = record['chart']['difficulty']
        chart_id = record['chart']['id']
        score = record['score']
        acc = round(record['accuracy'] * 100, 3)
        perfect = record['perfect']
        early = record['goodEarly']
        late = record['goodLate']
        bad = record['bad']
        miss = record['miss']
        rks = round(record['rks'], 3)
        return Record(index, song, level, diff, chart_id, score, acc, perfect, early, late, bad, miss, rks)

    rks = None
    phi3 = []
    b27 = []
    errors = []
    if request.method == 'POST':
        # Get the B27
        user_id = request.POST.get('user-id')
        rks = round(requests.get(f'https://api.phizone.cn/users/{user_id}').json()['data']['rks'], 3)
        req = requests.get(f'https://api.phizone.cn/users/{user_id}/personalBests')
        if req.status_code != 404 and req.json()['code'] != 'UserNotFound':
            data = req.json()['data']
            if data['phi3']:
                phi3 = [get_record_info(i + 1, record) for i, record in enumerate(data['phi3'])]
            if data['best27']:
                b27 = [get_record_info(i + 1, record) for i, record in enumerate(data['best27'])]
        else:
            errors.append('用户不存在')
    context = {'rks': rks, 'phi3': phi3, 'b27': b27, 'errors': errors}
    return render(request, 'pages/phizone_best.html', context)

# Notanote Tools
def notanote(request):
    return render(request, 'pages/notanote.html')

# Notanote B26 calculator
def notanote_best(request):
    # Notanote rank class
    class Record():
        def __init__(self, index, song, level, diff, score, acc, rank):
            self.index = index
            self.song = song
            self.level = level
            self.diff = diff
            self.score = score
            self.acc = acc
            self.rank = rank
            self.level_id = 'ez-plus' if self.level == 'EZ+' else self.level.lower()

    nrk = None
    b26 = []
    overflow = []
    errors = []
    if request.method == 'POST':
        # Read the save file
        file = request.FILES['save']
        with open(os.path.join(settings.MEDIA_ROOT, file.name), 'wb') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        # Decrypt the save file
        try:
            with open(os.path.join(settings.MEDIA_ROOT, file.name), 'r') as file:
                ciphertext = base64.b64decode(file.read())
            os.remove(os.path.join(settings.MEDIA_ROOT, file.name))
            key = 'secret'.encode('utf-8')
            iv = 'secret'.encode('utf-8')
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            plaintext = unpad(cipher.decrypt(ciphertext), 16)
            scores = json.loads(plaintext)
        except:
            errors.append('存档文件解密失败')

        records = []
        i = 0
        if not errors:
            try:
                with open(os.path.join(settings.STATIC_ROOT, 'notanote/song_id.json'), encoding='utf-8') as file:
                    id_dict = json.loads(file.read())
                # Traverse the data
                for chart, result in scores.items():
                    i += 1
                    song_id, level = chart.split('_', maxsplit=1)
                    if level[:2] == 'EX':
                        level = 'TL'
                    elif level == 'EZ_Plus':
                        level = 'EZ+'
                    song = id_dict[song_id]
                    diff = result['Rate']
                    good_offset_list = result['GoodOffsetList']
                    perfect = result['PerfectNum']
                    good = result['GoodNum']
                    bad = result['BadNum']
                    miss = result['MissNum']
                    note_num = perfect + good + bad + miss
                    score = round(1000000 * (perfect + good) / note_num)
                    acc = (perfect + sum([0.4 + (120 - abs(offset)) / 100 for offset in good_offset_list])) / note_num
                    rank = (math.e ** (2 * acc) - 1) / (math.e ** 2 - 1) * (diff + 5)
                    records.append(Record(None, song, level, diff, score, acc * 100, rank))
                # Sort records
                records.sort(key=lambda record: record.rank, reverse=True)
                b26 = records[:26]
                print(b26)
                for index, record in enumerate(b26):
                    record.index = index + 1
                overflow = records[26:36]
                for index, record in enumerate(overflow):
                    record.index = index + 27
                # Calculate the Nrk
                rank_m_weight_sum = 0
                i = 0
                while i < len(b26):
                    rank = b26[i].rank
                    rank_m_weight_sum = rank_m_weight_sum + rank * (1 - 0.02 * i)
                    i += 1
                nrk = round(rank_m_weight_sum / 19.5, 3)
            except:
                errors.append('查分时出现错误')
    context = {'nrk': nrk, 'b26': b26, 'overflow': overflow, 'errors': errors}
    return render(request, 'pages/notanote_best.html', context)

# Notanote best instruction
def notanote_best_instruction(request):
    return render(request, 'pages/notanote_best_instruction.html')

# Notanote single rank calculator
def notanote_rank(request):
    rank = []
    errors = []
    if request.method == 'POST':
        diff = float(request.POST.get('diff'))
        acc = float(request.POST.get('acc'))
        if 0 <= acc <= 100:
            rank = (math.e ** (2 * acc / 100) - 1) / (math.e ** 2 - 1) * (diff + 5)
        else:
            errors.append('准确率不在0~100之间')
    context = {'rank': rank, 'errors': errors}
    return render(request, 'pages/notanote_rank.html', context)

# Programming index page
def programming_index(request):
    articles = Programming.objects.all().order_by('-date')
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

# Random number generator
def randomnum(request):
    result = None
    errors = []
    if request.method == 'POST':
        min = float(request.POST.get('min'))
        max = float(request.POST.get('max'))
        decimal_places = int(request.POST.get('decimal_places'))
        if min < max:
            result = round(random.uniform(min, max), decimal_places)
        else:
            errors.append('最小值必须小于最大值')
    context = {'errors': errors, 'result': result}
    return render(request, 'pages/randomnum.html', context)

# Diary index page
def posts_index(request):
    posts = Post.objects.all().order_by('-date')
    context = {'posts': posts}
    return render(request, 'pages/posts_index.html', context)

# Diary
def posts(request, id):
    post = Post.objects.get(id=id)
    id = post.id
    title = post.title
    date = post.date
    context = {id: 'id', 'title': title, 'date': date}
    return render(request, f'pages/posts/{id}.html', context)

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
