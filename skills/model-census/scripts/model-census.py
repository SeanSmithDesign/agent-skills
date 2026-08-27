#!/usr/bin/env python3
# Reads ~/.claude/projects/**/*.jsonl (main-thread transcripts) and
# ~/.claude/projects/**/subagents/agent-*.jsonl (subagent transcripts).
# Subagent type is recovered by joining the parent transcript's Agent
# tool_use (input.subagent_type) to the matching tool_result's
# "agentId: <id>" line, then matched to the subagent transcript by id.
# Output/input token counts are raw counts, not dollars.
import json, os, re, sys, glob, collections, datetime, argparse

ROOT = os.path.expanduser('~/.claude/projects')

p = argparse.ArgumentParser()
p.add_argument('--since', default=None, help='YYYY-MM-DD (local midnight), default 30 days ago')
p.add_argument('--brief', action='store_true')
args = p.parse_args()

if args.since:
    # naive -> local tz via astimezone() (py3.6+)
    SINCE = datetime.datetime.strptime(args.since, '%Y-%m-%d').astimezone()
else:
    SINCE = datetime.datetime.now().astimezone() - datetime.timedelta(days=30)

def it(path):
    with open(path,errors='ignore') as f:
        for line in f:
            try: yield json.loads(line)
            except: pass

def out_tok(u): return (u or {}).get('output_tokens',0)
def in_tok(u):
    u=u or {}; return u.get('input_tokens',0)+u.get('cache_creation_input_tokens',0)+u.get('cache_read_input_tokens',0)

def rec_ts(r):
    # returns aware datetime or None if absent/unparseable — records with
    # no timestamp are kept (not filtered) per the mtime-is-cheap-prefilter
    # design: the mtime check already admitted the file.
    ts = r.get('timestamp')
    if not ts: return None
    try:
        if ts.endswith('Z'): ts = ts[:-1] + '+00:00'
        return datetime.datetime.fromisoformat(ts)
    except Exception:
        return None

SYNTHETIC = '<synthetic>'

# pass 1: parent sessions → agentId→(subagent_type, model_param) ; main model usage
link={}
main=collections.defaultdict(lambda:[0,0,0,set()])  # (proj,model)->[turns,out,in,sessions]
tu={}
for proj in os.listdir(ROOT):
    pdir=os.path.join(ROOT,proj)
    if not os.path.isdir(pdir): continue
    for sf in glob.glob(os.path.join(pdir,'*.jsonl')):
        if datetime.datetime.fromtimestamp(os.path.getmtime(sf),datetime.timezone.utc)<SINCE: continue
        sid=os.path.basename(sf)[:-6]
        for r in it(sf):
            ts=rec_ts(r)
            if ts is not None and ts<SINCE: continue
            m=r.get('message') or {}
            c=m.get('content')
            if r.get('type')=='assistant':
                mdl=m.get('model')
                if mdl and mdl!=SYNTHETIC and not r.get('isSidechain'):
                    k=(proj,mdl); main[k][0]+=1; main[k][1]+=out_tok(m.get('usage')); main[k][2]+=in_tok(m.get('usage')); main[k][3].add(sid)
                if isinstance(c,list):
                    for b in c:
                        if b.get('type')=='tool_use' and b.get('name')=='Agent':
                            i=b.get('input',{}); tu[b['id']]=(i.get('subagent_type') or 'general-purpose(default)', i.get('model'))
            elif r.get('type')=='user' and isinstance(c,list):
                for b in c:
                    if b.get('type')=='tool_result' and b.get('tool_use_id') in tu:
                        txt=b.get('content'); txt=json.dumps(txt) if not isinstance(txt,str) else txt
                        mm=re.search(r'agentId: ([0-9a-f]+)',txt)
                        if mm: link[mm.group(1)]=tu[b['tool_use_id']]

# pass 2: subagent transcripts
sub=collections.defaultdict(lambda:[0,0,0])  # (type,param,actual)->[agents,out,in]
subproj=collections.defaultdict(lambda:[0,0])
nolink=0
for af in glob.glob(os.path.join(ROOT,'*','*','subagents','agent-*.jsonl')):
    if datetime.datetime.fromtimestamp(os.path.getmtime(af),datetime.timezone.utc)<SINCE: continue
    aid=os.path.basename(af)[6:-6]
    proj=af.split('/')[-4]
    models=collections.Counter(); o=0; i=0
    for r in it(af):
        ts=rec_ts(r)
        if ts is not None and ts<SINCE: continue
        if r.get('type')=='assistant':
            m=r.get('message') or {}
            if m.get('model'): models[m['model']]+=1
            o+=out_tok(m.get('usage')); i+=in_tok(m.get('usage'))
    del models[SYNTHETIC]
    if not models: continue
    actual=models.most_common(1)[0][0]
    t,p2=link.get(aid,('?unlinked',None))
    if aid not in link: nolink+=1
    k=(t,p2,actual); sub[k][0]+=1; sub[k][1]+=o; sub[k][2]+=i
    subproj[(proj,actual)][0]+=1; subproj[(proj,actual)][1]+=o

def fmt(n): return f"{n/1e6:.1f}M" if n>=1e6 else f"{n/1e3:.0f}k"

SINCE_STR = SINCE.date().isoformat()

def distinct_sessions(agg):
    # agg: dict[model] -> [session_set, ...]; union across all models
    u=set()
    for a in agg.values(): u|=a[0]
    return len(u)

if args.brief:
    print(f"== MAIN THREAD by model since {SINCE_STR}: model | sessions* | out tok | in tok")
    agg=collections.defaultdict(lambda:[set(),0,0])
    for (proj,mdl),v in main.items():
        a=agg[mdl]; a[0]|=v[3]; a[1]+=v[1]; a[2]+=v[2]
    for mdl,a in sorted(agg.items(),key=lambda kv:-kv[1][1]): print(f"{mdl:<22} {len(a[0]):>5} {fmt(a[1]):>7} {fmt(a[2]):>8}")
    print(f"* a session that switched models counts under each; {distinct_sessions(agg)} distinct sessions in window")

    print(f"\n== SUBAGENTS by type -> actual model since {SINCE_STR}: type | actual model | runs | out tok")
    agg2=collections.defaultdict(lambda:[0,0])
    for (t,p2,actual),v in sub.items():
        a=agg2[(t,actual)]; a[0]+=v[0]; a[1]+=v[1]
    for (t,actual),a in sorted(agg2.items(),key=lambda kv:-kv[1][1]): print(f"{t:<28} {actual:<22} {a[0]:>5} {fmt(a[1]):>7}")

    print(f"\n== FABLE by project (main + subagent) since {SINCE_STR}: project | out tok")
    fable_by_proj=collections.defaultdict(int)
    for (proj,mdl),v in main.items():
        if 'fable' in mdl.lower(): fable_by_proj[proj]+=v[1]
    for (proj,mdl),v in subproj.items():
        if 'fable' in mdl.lower(): fable_by_proj[proj]+=v[1]
    if fable_by_proj:
        for proj,o in sorted(fable_by_proj.items(),key=lambda kv:-kv[1]): print(f"{proj[-40:]:<42} {fmt(o):>7}")
    else:
        print("(none)")
    sys.exit(0)

print(f"== SUBAGENTS since {SINCE_STR}: type | model param | ACTUAL model | agents | out tok | in tok")
for k,v in sorted(sub.items(),key=lambda kv:-kv[1][1]): print(f"{k[0]:<28} {str(k[1]):<8} {k[2]:<22} {v[0]:>5} {fmt(v[1]):>7} {fmt(v[2]):>8}")
print(f"(unlinked agents: {nolink})")
print(f"\n== MAIN THREAD since {SINCE_STR}: model | sessions* | turns | out tok | in tok")
agg=collections.defaultdict(lambda:[set(),0,0,0])
for (proj,mdl),v in main.items():
    a=agg[mdl]; a[0]|=v[3]; a[1]+=v[0]; a[2]+=v[1]; a[3]+=v[2]
for mdl,a in sorted(agg.items(),key=lambda kv:-kv[1][2]): print(f"{mdl:<22} {len(a[0]):>5} {a[1]:>6} {fmt(a[2]):>7} {fmt(a[3]):>8}")
print(f"* a session that switched models counts under each; {distinct_sessions(agg)} distinct sessions in window")
print("\n== BY PROJECT (main thread) top 12: project | model | sessions | out tok")
for (proj,mdl),v in sorted(main.items(),key=lambda kv:-kv[1][1])[:12]: print(f"{proj[-40:]:<42} {mdl:<22} {len(v[3]):>4} {fmt(v[1]):>7}")
print("\n== BY PROJECT (subagents) top 12: project | actual model | agents | out tok")
for (proj,mdl),v in sorted(subproj.items(),key=lambda kv:-kv[1][1])[:12]: print(f"{proj[-40:]:<42} {mdl:<22} {v[0]:>5} {fmt(v[1]):>7}")
