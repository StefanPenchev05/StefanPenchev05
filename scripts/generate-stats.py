"""Generate profile SVGs from GitHub API data; Python standard library only."""
import datetime as dt
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen
from xml.sax.saxutils import escape

OWNER = os.environ.get('PROFILE_OWNER', 'StefanPenchev05')
TOKEN = os.environ['GH_TOKEN']
ROOT = Path(__file__).resolve().parents[1]

def api(path, data=None):
    req = Request('https://api.github.com/' + path, data=json.dumps(data).encode() if data else None,
                  headers={'Authorization': 'Bearer ' + TOKEN, 'User-Agent': 'profile-svg-generator',
                           'Accept': 'application/vnd.github+json'})
    with urlopen(req, timeout=30) as response:
        result = json.load(response)
    if isinstance(result, dict) and result.get('errors'):
        raise RuntimeError(result['errors'])
    return result

def text(x, y, value, size=18, color='#b5c4d9'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{escape(str(value))}</text>'

def write(name, body, height, title, width=1000):
    out = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img"><title>{escape(title)}</title><rect x="1" y="1" width="{width-2}" height="{height-2}" rx="16" fill="#0d1729" stroke="#283e59"/><g font-family="Verdana,sans-serif">{body}</g></svg>'
    (ROOT/'assets'/name).write_text(out)

query = '''query($login:String!){user(login:$login){followers{totalCount} repositories(ownerAffiliations:OWNER,privacy:PUBLIC){totalCount} contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}'''
user = api('graphql', {'query': query, 'variables': {'login': OWNER}})['data']['user']
repos = []
page = 1
while True:
    batch = api(f'users/{OWNER}/repos?per_page=100&page={page}')
    repos.extend(batch)
    if len(batch) < 100:
        break
    page += 1
languages = {}
for repo in repos:
    if not repo['fork']:
        for language, count in api(f'repos/{OWNER}/{repo["name"]}/languages').items():
            languages[language] = languages.get(language, 0) + count
calendar = user['contributionsCollection']['contributionCalendar']
date = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
body = text(32, 40, 'GitHub / public activity', 22, '#eef4ff') + text(32, 70, 'Updated ' + date, 13)
for y, label, value in [(117,'Public repositories',user['repositories']['totalCount']), (169,'Repository stars',sum(r['stargazers_count'] for r in repos if not r['fork'])), (221,'Contributions / past year',calendar['totalContributions'])]:
    body += text(32,y,value,28,'#79deed') + text(140,y,label,16)
write('stats.svg',body,300,'Public GitHub statistics updated '+date,500)
body = text(32,40,'Repository languages',22,'#eef4ff')
total = sum(languages.values())
for index,(language,count) in enumerate(sorted(languages.items(),key=lambda x:x[1],reverse=True)[:6]):
    y = 78 + index*30
    pct = count/total*100 if total else 0
    body += text(32,y,language,14) + text(390,y,f'{pct:.1f}%',14,'#a5adff')
    body += f'<rect x="190" y="{y-10}" width="{max(1,pct*1.6):.1f}" height="7" rx="3" fill="#54d9ed"/>'
body += text(32,270,'Non-fork public repositories · share of language bytes',11)
write('languages.svg',body,300,'Public repository language usage updated '+date,500)
days = [day for week in calendar['weeks'] for day in week['contributionDays']]
longest = run = 0
for day in days:
    run = run+1 if day['contributionCount'] else 0
    longest = max(longest,run)
current = 0
eligible = days[:-1] if days and days[-1]['date'] == dt.datetime.now(dt.timezone.utc).date().isoformat() and not days[-1]['contributionCount'] else days
for day in reversed(eligible):
    if not day['contributionCount']:
        break
    current += 1
body = text(32,40,'Contribution rhythm',28,'#eef4ff') + text(32,72,f'Current streak: {current} days     Longest in this calendar: {longest} days',23,'#79deed')
colors=['#17263d','#1e5368','#297f94','#40b2c4','#79deed']
for x,week in enumerate(calendar['weeks']):
    for day in week['contributionDays']:
        weekday=(dt.date.fromisoformat(day['date']).weekday()+1)%7
        count=day['contributionCount']
        color=colors[0 if count==0 else min(4,1+(count>3)+(count>7)+(count>12))]
        body += f'<rect x="{32+x*17}" y="{100+weekday*17}" width="13" height="13" rx="3" fill="{color}"><title>{day["date"]}: {count} contributions</title></rect>'
body += text(32,250,days[0]['date']+' — '+days[-1]['date']+' · GitHub contribution calendar',20)
body += text(32,280,'Updated '+date+' · Fewer',17)
for i,color in enumerate(colors):body+=f'<rect x="{510+i*20}" y="268" width="13" height="13" rx="3" fill="{color}"/>'
body += text(620,280,'More',17)
write('activity.svg',body,310,'GitHub contribution calendar and streaks updated '+date)
