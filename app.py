from flask import Flask, render_template, request, jsonify, Response
import json, os, csv, io, urllib.request, urllib.error
from datetime import datetime, date, timedelta

app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

def data_file(name): return os.path.join(DATA_DIR, f"{name}.json")
def load(name):
    f = data_file(name)
    return json.load(open(f)) if os.path.exists(f) else {}
def save(name, data):
    with open(data_file(name), 'w') as fp: json.dump(data, fp, indent=2)
def today(): return date.today().isoformat()

@app.route('/') 
def index(): return render_template('index.html')

# ── WORKOUTS ──────────────────────────────────────────────────────────────────
@app.route('/api/workouts', methods=['GET'])
def get_workouts(): return jsonify(load('workouts'))

@app.route('/api/workouts', methods=['POST'])
def add_workout():
    data = load('workouts'); entry = request.json
    entry['id'] = datetime.now().isoformat(); entry['date'] = today()
    data.setdefault(today(), []).append(entry); save('workouts', data)
    return jsonify({'ok': True, 'entry': entry})

@app.route('/api/workouts/<entry_id>', methods=['DELETE'])
def delete_workout(entry_id):
    data = load('workouts')
    for day in data: data[day] = [w for w in data[day] if w.get('id') != entry_id]
    save('workouts', data); return jsonify({'ok': True})

# ── FOOD ──────────────────────────────────────────────────────────────────────
@app.route('/api/food', methods=['GET'])
def get_food(): return jsonify(load('food'))

@app.route('/api/food', methods=['POST'])
def add_food():
    data = load('food'); entry = request.json
    entry['id'] = datetime.now().isoformat(); entry['date'] = today()
    data.setdefault(today(), []).append(entry); save('food', data)
    return jsonify({'ok': True, 'entry': entry})

@app.route('/api/food/<entry_id>', methods=['DELETE'])
def delete_food(entry_id):
    data = load('food')
    for day in data: data[day] = [f for f in data[day] if f.get('id') != entry_id]
    save('food', data); return jsonify({'ok': True})

# ── SAVED FOODS ───────────────────────────────────────────────────────────────
@app.route('/api/saved_foods', methods=['GET'])
def get_saved_foods(): return jsonify(load('saved_foods').get('items', []))

@app.route('/api/saved_foods', methods=['POST'])
def save_food_to_library():
    data = load('saved_foods'); items = data.get('items', [])
    entry = request.json; entry['id'] = datetime.now().isoformat()
    items.append(entry); save('saved_foods', {'items': items})
    return jsonify({'ok': True})

@app.route('/api/saved_foods/<food_id>', methods=['DELETE'])
def delete_saved_food(food_id):
    data = load('saved_foods')
    save('saved_foods', {'items': [f for f in data.get('items',[]) if f.get('id')!=food_id]})
    return jsonify({'ok': True})

# ── WATER ─────────────────────────────────────────────────────────────────────
@app.route('/api/water', methods=['GET'])
def get_water(): return jsonify(load('water'))

@app.route('/api/water', methods=['POST'])
def log_water():
    data = load('water'); entry = request.json
    entry['id'] = datetime.now().isoformat(); t = today()
    data.setdefault(t, {'total': 0, 'logs': []})
    data[t]['total'] = data[t].get('total', 0) + entry['amount']
    data[t]['logs'].append(entry); save('water', data)
    return jsonify({'ok': True, 'total': data[t]['total']})

# ── GOALS ─────────────────────────────────────────────────────────────────────
@app.route('/api/goals', methods=['GET'])
def get_goals(): return jsonify(load('goals'))

@app.route('/api/goals', methods=['POST'])
def save_goals():
    data = request.json; data['updated'] = today(); save('goals', data)
    return jsonify({'ok': True})

# ── MENTAL ────────────────────────────────────────────────────────────────────
@app.route('/api/mental', methods=['GET'])
def get_mental(): return jsonify(load('mental'))

@app.route('/api/mental', methods=['POST'])
def log_mental():
    data = load('mental'); entry = request.json
    entry['id'] = datetime.now().isoformat(); entry['date'] = today()
    data.setdefault(today(), []).append(entry); save('mental', data)
    return jsonify({'ok': True})

# ── STATS ─────────────────────────────────────────────────────────────────────
@app.route('/api/stats', methods=['GET'])
def get_stats(): return jsonify(load('stats'))

@app.route('/api/stats', methods=['POST'])
def log_stats():
    data = load('stats'); entry = request.json; entry['date'] = today()
    data.setdefault(today(), {}).update(entry); save('stats', data)
    return jsonify({'ok': True})

# ── PROFILE ───────────────────────────────────────────────────────────────────
@app.route('/api/profile', methods=['GET'])
def get_profile(): return jsonify(load('profile'))

@app.route('/api/profile', methods=['POST'])
def save_profile(): save('profile', request.json); return jsonify({'ok': True})

# ── PERSONAL RECORDS ──────────────────────────────────────────────────────────
@app.route('/api/prs', methods=['GET'])
def get_prs(): return jsonify(load('prs'))

@app.route('/api/prs', methods=['POST'])
def save_pr():
    data = load('prs'); entry = request.json
    exercise = entry.get('exercise','').strip()
    if not exercise: return jsonify({'ok': False}), 400
    record = {'weight': entry.get('weight',0), 'reps': entry.get('reps',1), 'date': today(), 'notes': entry.get('notes','')}
    est_1rm = record['weight'] * (1 + record['reps']/30)
    if exercise not in data: data[exercise] = {'history':[], 'best':None}
    data[exercise]['history'].append(record)
    best = data[exercise].get('best')
    is_pr = best is None or est_1rm > best.get('est_1rm',0)
    if is_pr: data[exercise]['best'] = {**record, 'est_1rm': round(est_1rm,1)}
    save('prs', data)
    return jsonify({'ok': True, 'is_pr': is_pr, 'est_1rm': round(est_1rm,1)})

# ── HABITS ────────────────────────────────────────────────────────────────────
@app.route('/api/habits', methods=['GET'])
def get_habits(): return jsonify(load('habits'))

@app.route('/api/habits/definitions', methods=['POST'])
def save_habit_defs():
    data = load('habits'); data['definitions'] = request.json.get('habits',[])
    save('habits', data); return jsonify({'ok': True})

@app.route('/api/habits/log', methods=['POST'])
def log_habit():
    data = load('habits'); entry = request.json; t = today()
    data.setdefault('logs',{}).setdefault(t,{})[entry['habit_id']] = entry['completed']
    save('habits', data); return jsonify({'ok': True})

# ── SUPPLEMENTS ───────────────────────────────────────────────────────────────
@app.route('/api/supplements', methods=['GET'])
def get_supplements(): return jsonify(load('supplements'))

@app.route('/api/supplements/definitions', methods=['POST'])
def save_supplement_defs():
    data = load('supplements'); data['definitions'] = request.json.get('supplements',[])
    save('supplements', data); return jsonify({'ok': True})

@app.route('/api/supplements/log', methods=['POST'])
def log_supplement():
    data = load('supplements'); entry = request.json
    entry['id'] = datetime.now().isoformat(); t = today()
    data.setdefault('logs',{}).setdefault(t,[]).append(entry)
    save('supplements', data); return jsonify({'ok': True})

# ── STEPS ─────────────────────────────────────────────────────────────────────
@app.route('/api/steps', methods=['GET'])
def get_steps(): return jsonify(load('steps'))

@app.route('/api/steps', methods=['POST'])
def log_steps():
    data = load('steps'); t = today()
    data[t] = {'steps': request.json.get('steps',0), 'date': t}
    save('steps', data); return jsonify({'ok': True})

# ── CHALLENGES ────────────────────────────────────────────────────────────────
CHALLENGES = [
    {'id':'pushup30','name':'30-Day Push-Up','emoji':'💪','days':30,'desc':'Daily push-ups, increasing each week',
     'schedule':[10,10,15,15,20,20,25,25,30,30,35,35,40,40,45,45,50,50,55,55,60,60,65,65,70,70,75,75,80,100],'unit':'reps'},
    {'id':'plank30','name':'30-Day Plank','emoji':'🧱','days':30,'desc':'Hold a plank longer each day',
     'schedule':[20,20,30,30,40,40,45,60,60,60,60,90,90,90,120,120,120,150,150,150,180,180,210,210,240,240,270,300,300,300],'unit':'seconds'},
    {'id':'squat30','name':'30-Day Squat','emoji':'🦵','days':30,'desc':'Build leg strength with daily squats',
     'schedule':[50,55,60,0,70,75,80,0,100,105,110,0,130,135,140,0,150,155,160,0,180,185,190,0,220,225,230,0,240,250],'unit':'reps'},
    {'id':'water30','name':'Hydration Hero','emoji':'💧','days':30,'desc':'Drink your daily water goal every single day','schedule':[],'unit':'ml'},
    {'id':'steps30','name':'10K Steps','emoji':'👟','days':30,'desc':'Walk 10,000 steps every day for 30 days','schedule':[],'unit':'steps'},
    {'id':'run5k','name':'Couch to 5K','emoji':'🏃','days':21,'desc':'Build up to running 5km without stopping',
     'schedule':[1,1,2,2,3,3,0,3,4,4,5,5,0,5,6,6,7,7,0,8,10],'unit':'min run'},
]

@app.route('/api/challenges', methods=['GET'])
def get_challenges():
    data = load('challenges'); result = []
    for ch in CHALLENGES:
        uc = data.get(ch['id'],{})
        result.append({**ch,'active':uc.get('active',False),'start_date':uc.get('start_date'),
                        'completed_days':uc.get('completed_days',[])})
    return jsonify(result)

@app.route('/api/challenges/<ch_id>/start', methods=['POST'])
def start_challenge(ch_id):
    data = load('challenges'); data.setdefault(ch_id,{})
    data[ch_id].update({'active':True,'start_date':today(),'completed_days':data[ch_id].get('completed_days',[])})
    save('challenges', data); return jsonify({'ok': True})

@app.route('/api/challenges/<ch_id>/complete_day', methods=['POST'])
def complete_challenge_day(ch_id):
    data = load('challenges'); t = today()
    data.setdefault(ch_id,{'completed_days':[]})
    if t not in data[ch_id]['completed_days']: data[ch_id]['completed_days'].append(t)
    save('challenges', data)
    return jsonify({'ok': True, 'total': len(data[ch_id]['completed_days'])})

@app.route('/api/challenges/<ch_id>/stop', methods=['POST'])
def stop_challenge(ch_id):
    data = load('challenges'); data.setdefault(ch_id,{})['active'] = False
    save('challenges', data); return jsonify({'ok': True})

# ── RECOVERY SCORE ────────────────────────────────────────────────────────────
@app.route('/api/recovery')
def recovery_score():
    t = today(); mental_today = load('mental').get(t,[]); workouts_data = load('workouts')
    sleep_score = 15
    if mental_today:
        last = mental_today[-1]; h = last.get('sleep_hours',7); q = last.get('sleep_quality','Fair')
        sleep_score = min(15, max(0,(h/8)*15)) + {'Poor':0,'Fair':5,'Good':10,'Excellent':15}.get(q,5)
    stress_score = 15
    if mental_today: stress_score = max(0, 25 - (mental_today[-1].get('stress',5)*2.5))
    yesterday = (date.today()-timedelta(days=1)).isoformat()
    hi = sum(1 for w in workouts_data.get(yesterday,[]) if w.get('intensity') in ['Hard','Max Effort'])
    load_score = 25 - min(25, hi*8)
    last7 = [(date.today()-timedelta(days=i)).isoformat() for i in range(1,8)]
    consistency = (sum(1 for d in last7 if d in workouts_data)/7)*20
    total = max(0, min(100, round(sleep_score+stress_score+load_score+consistency)))
    if total>=80:   status,color,tip='Excellent','#3ecf8e','Body primed — go hard today! 🔥'
    elif total>=60: status,color,tip='Good','#4f9cf9','Ready to train. Push moderately. 💪'
    elif total>=40: status,color,tip='Fair','#f5c842','Consider lighter training or active recovery.'
    else:           status,color,tip='Poor','#e84d3d','Rest day recommended. Sleep & recover.'
    return jsonify({'score':total,'status':status,'color':color,'tip':tip,
        'breakdown':{'sleep':round(sleep_score),'stress':round(stress_score),'load':round(load_score),'consistency':round(consistency)}})

# ── MUSCLE MAP ────────────────────────────────────────────────────────────────
MUSCLE_MAP = {
    'Upper Body':['chest','front_shoulders','triceps','biceps','upper_back'],
    'Lower Body':['quads','hamstrings','glutes','calves'],
    'Full Body':['chest','quads','hamstrings','glutes','upper_back','core'],
    'Cardio':['calves','quads','hamstrings','core'],
    'Core':['core','obliques'],
    'HIIT':['core','quads','chest','calves','front_shoulders'],
    'Flexibility':['lower_back','hamstrings','hip_flexors'],
    'Sports':['quads','hamstrings','calves','core','obliques'],
}

@app.route('/api/muscle_map')
def muscle_map():
    workouts = load('workouts'); muscle_intensity = {}; today_d = date.today()
    for i in range(7):
        d = (today_d-timedelta(days=i)).isoformat()
        decay = 1.0-(i*0.12)
        for w in workouts.get(d,[]):
            mult = {'Light':0.5,'Moderate':1.0,'Hard':1.5,'Max Effort':2.0}.get(w.get('intensity','Moderate'),1.0)
            for m in MUSCLE_MAP.get(w.get('type',''),[]):
                muscle_intensity[m] = muscle_intensity.get(m,0)+(mult*decay)
    mx = max(muscle_intensity.values()) if muscle_intensity else 1
    return jsonify({k:round(v/mx,2) for k,v in muscle_intensity.items()})

# ── ACHIEVEMENTS ──────────────────────────────────────────────────────────────
@app.route('/api/achievements')
def get_achievements():
    workouts=load('workouts'); food=load('food'); water=load('water')
    mental=load('mental'); stats=load('stats'); prs=load('prs')
    total_workouts=sum(len(v) for v in workouts.values()); total_prs=len(prs)
    streak=0; check=date.today()
    for _ in range(365):
        if check.isoformat() in workouts: streak+=1; check-=timedelta(days=1)
        else: break
    achievements=[
        {'id':'first_workout','name':'First Step','emoji':'👟','desc':'Log your first workout','unlocked':total_workouts>=1,'points':10},
        {'id':'ten_workouts','name':'Getting Serious','emoji':'💪','desc':'Log 10 workouts','unlocked':total_workouts>=10,'points':25},
        {'id':'fifty_workouts','name':'Iron Will','emoji':'🏋️','desc':'Log 50 workouts','unlocked':total_workouts>=50,'points':75},
        {'id':'century','name':'Century Club','emoji':'💯','desc':'Log 100 workouts','unlocked':total_workouts>=100,'points':150},
        {'id':'streak3','name':'On a Roll','emoji':'🔥','desc':'3-day workout streak','unlocked':streak>=3,'points':20},
        {'id':'streak7','name':'Week Warrior','emoji':'⚡','desc':'7-day streak','unlocked':streak>=7,'points':50},
        {'id':'streak30','name':'Iron Monk','emoji':'🏆','desc':'30-day streak','unlocked':streak>=30,'points':200},
        {'id':'first_pr','name':'Record Breaker','emoji':'📈','desc':'Set your first PR','unlocked':total_prs>=1,'points':15},
        {'id':'five_prs','name':'PR Machine','emoji':'🥇','desc':'Track 5 PRs','unlocked':total_prs>=5,'points':40},
        {'id':'hydrated7','name':'Water Master','emoji':'💧','desc':'Log water 7 days','unlocked':len(water)>=7,'points':30},
        {'id':'mind_matters','name':'Mind Matters','emoji':'🧠','desc':'5 mental check-ins','unlocked':len(mental)>=5,'points':25},
        {'id':'all_rounder','name':'All-Rounder','emoji':'🌟','desc':'Log workout+food+water same day','unlocked':bool(set(workouts.keys())&set(food.keys())&set(water.keys())),'points':35},
        {'id':'body_tracker','name':'Body Aware','emoji':'📏','desc':'Log stats 3 times','unlocked':len(stats)>=3,'points':20},
        {'id':'food_aware','name':'Food Aware','emoji':'🥗','desc':'Log 20 food entries','unlocked':sum(len(v) for v in food.values())>=20,'points':25},
        {'id':'challenger','name':'Challenger','emoji':'🔥','desc':'Start a 30-day challenge','unlocked':bool(load('challenges')),'points':15},
    ]
    earned = sum(a['points'] for a in achievements if a['unlocked'])
    return jsonify({'achievements':achievements,'streak':streak,'total_workouts':total_workouts,'points':earned})

# ── AI COACH ──────────────────────────────────────────────────────────────────
@app.route('/api/coach', methods=['POST'])
def ai_coach():
    body=request.json; api_key=body.get('api_key','').strip()
    user_msg=body.get('message','').strip(); history=body.get('history',[])
    if not api_key: return jsonify({'error':'Add your Anthropic API key in the AI Coach settings.'}),400
    if not user_msg: return jsonify({'error':'No message'}),400

    t=today(); food_today=load('food').get(t,[])
    workouts_today=load('workouts').get(t,[]); water_today=load('water').get(t,{})
    mental_today=load('mental').get(t,[]); goals=load('goals'); profile=load('profile')
    stats_data=load('stats'); prs=load('prs')
    calories_in=sum(f.get('calories',0) for f in food_today)
    protein=sum(f.get('protein',0) for f in food_today)
    last_stat=list(stats_data.values())[-1] if stats_data else {}
    pr_summary=', '.join(f"{k}: {v['best']['weight']}kg×{v['best']['reps']}reps" for k,v in list(prs.items())[:5]) if prs else 'None yet'

    system_prompt=f"""You are FitCoach, an expert AI personal trainer and nutritionist inside the FitLife app. You are motivating, specific, and highly personalized.

USER: {profile.get('name','Athlete')}, age {profile.get('age','?')}, {profile.get('gender','?')}, {profile.get('height','?')}cm, {last_stat.get('weight',profile.get('weight','?'))}kg, {profile.get('activity','Moderate')}
FOCUS: {goals.get('focus','Overall Fitness')}
TODAY ({t}): {calories_in}/{goals.get('daily_calories',2000)} kcal | {protein}g protein | {water_today.get('total',0)}/{goals.get('daily_water',2500)}ml water | {len(workouts_today)} workouts
MOOD: {mental_today[-1].get('mood_score','?') if mental_today else 'not logged'}/5
PRs: {pr_summary}

Be specific, motivating, practical. Reference their data. Keep it 2-4 paragraphs. End with one actionable next step."""

    messages=[{'role':h['role'],'content':h['content']} for h in history[-8:]]
    messages.append({'role':'user','content':user_msg})

    payload=json.dumps({'model':'claude-haiku-4-5-20251001','max_tokens':600,'system':system_prompt,'messages':messages}).encode()
    req=urllib.request.Request('https://api.anthropic.com/v1/messages',data=payload,
        headers={'Content-Type':'application/json','x-api-key':api_key,'anthropic-version':'2023-06-01'},method='POST')
    try:
        with urllib.request.urlopen(req,timeout=30) as resp:
            result=json.loads(resp.read())
            return jsonify({'ok':True,'reply':result['content'][0]['text']})
    except urllib.error.HTTPError as e:
        err=json.loads(e.read()).get('error',{}).get('message',str(e))
        return jsonify({'error':err}),e.code
    except Exception as e: return jsonify({'error':str(e)}),500

# ── PLANNER ───────────────────────────────────────────────────────────────────
@app.route('/api/planner',methods=['GET'])
def get_planner(): return jsonify(load('planner'))

@app.route('/api/planner',methods=['POST'])
def save_planner(): save('planner',request.json); return jsonify({'ok':True})

# ── SUMMARY ───────────────────────────────────────────────────────────────────
@app.route('/api/summary')
def summary():
    t=today(); food_data=load('food').get(t,[]); water_data=load('water').get(t,{})
    workout_data=load('workouts').get(t,[]); mental_data=load('mental').get(t,[])
    goals=load('goals'); profile=load('profile')
    calories_in=sum(f.get('calories',0) for f in food_data)
    protein=sum(f.get('protein',0) for f in food_data)
    carbs=sum(f.get('carbs',0) for f in food_data)
    fat=sum(f.get('fat',0) for f in food_data)
    fiber=sum(f.get('fiber',0) for f in food_data)
    water_total=water_data.get('total',0)
    calories_burned=sum(w.get('calories_burned',0) for w in workout_data)
    moods=[m.get('mood_score',0) for m in mental_data if 'mood_score' in m]
    avg_mood=round(sum(moods)/len(moods),1) if moods else None
    workouts_all=load('workouts'); streak=0; check=date.today()
    for _ in range(365):
        if check.isoformat() in workouts_all: streak+=1; check-=timedelta(days=1)
        else: break
    return jsonify({'date':t,'calories_in':calories_in,'calories_out':calories_burned,
        'net_calories':calories_in-calories_burned,'protein':protein,'carbs':carbs,'fat':fat,'fiber':fiber,
        'water':water_total,'workouts':len(workout_data),'avg_mood':avg_mood,
        'goal_calories':goals.get('daily_calories',2000),'goal_water':goals.get('daily_water',2500),
        'goal_protein':goals.get('daily_protein',150),'focus':goals.get('focus','Overall Fitness'),
        'name':profile.get('name','Athlete'),'streak':streak})

# ── HISTORY ───────────────────────────────────────────────────────────────────
@app.route('/api/history')
def history():
    workouts=load('workouts'); food=load('food'); water=load('water')
    mental=load('mental'); stats=load('stats')
    all_days=sorted(set(list(workouts.keys())+list(food.keys())+list(water.keys())),reverse=True)
    result=[]
    for day in all_days[:60]:
        food_day=food.get(day,[])
        result.append({'date':day,'calories':sum(f.get('calories',0) for f in food_day),
            'workouts':len(workouts.get(day,[])),'water':water.get(day,{}).get('total',0),
            'mood':mental.get(day,[{}])[-1].get('mood_score') if mental.get(day) else None,
            'weight':stats.get(day,{}).get('weight')})
    return jsonify(result)

# ── EXPORT ────────────────────────────────────────────────────────────────────
@app.route('/api/export')
def export_csv():
    data=json.loads(history().get_data()); output=io.StringIO()
    w=csv.DictWriter(output,fieldnames=['date','calories','workouts','water','mood','weight'])
    w.writeheader(); w.writerows(data)
    return Response(output.getvalue(),mimetype='text/csv',
        headers={'Content-Disposition':'attachment; filename=fitlife_export.csv'})

if __name__ == '__main__':
    print("\n" + "="*52)
    print("  ⚡  FITLIFE v2 — AI-Powered Fitness Tracker  ⚡")
    print("="*52)
    print("\n👉  Open your browser: http://localhost:5000\n")
    app.run(debug=False, port=5000)
