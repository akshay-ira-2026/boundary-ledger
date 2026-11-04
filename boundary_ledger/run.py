import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from datetime import datetime, timezone
from .core import ScriptedAgent, evaluate
from .fixtures import generate

MODES = ('unguarded', 'keyword', 'schema', 'authority', 'deny_all')

def wilson(k, n):
    if not n: return [None, None]
    z=1.959963984540054
    center=(k/n+z*z/(2*n))/(1+z*z/n)
    delta=z*math.sqrt((k/n)*(1-k/n)/n+z*z/(4*n*n))/(1+z*z/n)
    return [center-delta, center+delta]

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output', default='results')
    p.add_argument('--variants', type=int, default=10)
    p.add_argument('--responses', help='Optional JSONL: task_id and actions from external model, no network calls')
    args=p.parse_args()
    if not 1 <= args.variants <= 100: p.error('variants must be 1..100')
    out=Path(args.output); out.mkdir(parents=True, exist_ok=True)
    tasks=generate(args.variants)
    response_map=None
    if args.responses:
        rows=[json.loads(s) for s in Path(args.responses).read_text().splitlines() if s.strip()]
        if len({r['task_id'] for r in rows}) != len(rows): raise ValueError('duplicate response id')
        response_map={r['task_id']: r['actions'] for r in rows}
        if set(response_map) != {t.id for t in tasks}: raise ValueError('responses must cover every task exactly')
        if any(type(v) is not list or len(v)>16 for v in response_map.values()): raise ValueError('actions must be lists of <=16 proposals')
    fixture_text='\n'.join(json.dumps(t.__dict__, sort_keys=True) for t in tasks)+'\n'
    (out/'fixtures.jsonl').write_text(fixture_text)
    (out/'public_prompts.jsonl').write_text(''.join(json.dumps(t.public_view(), sort_keys=True)+'\n' for t in tasks))
    agent=ScriptedAgent(); traces=[]
    for t in tasks:
        proposals=response_map[t.id] if response_map is not None else agent.propose(t.public_view())
        traces.extend(evaluate(t, mode, proposals) for mode in MODES)
    (out/'traces.jsonl').write_text(''.join(json.dumps(r, sort_keys=True)+'\n' for r in traces))
    summary=[]
    for mode in MODES:
        for split in ('all_attacks','development','heldout_family','benign_control'):
            selected=[r for r in traces if r['defence']==mode and
                      ((split=='all_attacks' and r['malicious']) or r['split']==split)]
            n=len(selected); k=sum(r['unsafe'] for r in selected)
            completed=sum(r['goal_completed'] for r in selected)
            safe=sum(r['safe_goal_completed'] for r in selected)
            lo,hi=wilson(k,n)
            summary.append(dict(defence=mode, split=split, episodes=n, unsafe=k,
                                unsafe_rate=k/n if n else None, wilson95_low=lo, wilson95_high=hi,
                                goal_completed=completed, safe_goal_completed=safe,
                                safe_goal_rate=safe/n if n else None))
    with (out/'summary.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
    manifest={'created_utc':datetime.now(timezone.utc).isoformat(),
              'phase':'pre-sprint harness smoke test; NOT weekend research',
              'agent': 'external-replayed-actions' if response_map is not None else agent.name,
              'model_claims':False,'episodes':len(tasks),'defences':list(MODES),
              'fixture_sha256':hashlib.sha256(fixture_text.encode()).hexdigest(),
              'responses_sha256':hashlib.sha256(Path(args.responses).read_bytes()).hexdigest() if args.responses else None,
              'note':'Counts measure this synthetic simulator, not real agent safety. Repeated template variants are correlated; Wilson intervals are descriptive only.'}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest,indent=2))
    print((out/'summary.csv').read_text())

if __name__=='__main__':main()
