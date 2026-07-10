# The Architect's Loop — how an operator thinks

The Blueprint is what you build. The Loop is how you decide what to build. Run it every week and, after a month or two, it stops being a checklist and becomes a reflex — you start spotting automations mid-week without trying.

**Survey → Design → Construct.** Three moves. That's it.

---

## Move 1 — Survey (find the candidate)

Look at your actual week and ask five questions:

1. What did I do **three or more times**? (frequency)
2. What felt **manual, boring, or copy-paste**? (drudgery)
3. What made me think *"a sharp intern could do this"*? (delegation)
4. If **500 new customers showed up tomorrow, what breaks first**? (the bottleneck)
5. What would **bring me those 500 customers**? (the growth lever)

The first three find waste. The last two find leverage. Pick **one** candidate. Not five. One.

---

## Move 2 — Design (scope exactly one)

Before you touch a tool, decide the task's fate. Three options, in order:

- **Kill it.** Ask: *"what happens if I just stop doing this?"* If the honest answer is "nothing," delete it. You don't automate waste — you remove it. This is a win, not a failure.
- **Automate it.** If it has to happen but doesn't need your judgment, automate it. Aim for the realistic split, not fantasy: roughly **60% fully automatic, 30% AI-drafts-you-approve, 10% still you**. Anyone promising 100% is selling something.
- **Assign it.** Too nuanced, too risky, too human? Hand it to a person. Not everything should be a machine.

Then, for anything you're automating, lock three things:

**The map** — write the steps on paper. Trigger (what starts it), sources (where the data lives), the shape change (how it gets transformed), the branch (where it decides), the destination (where the output goes). *If you can't explain it to a person, you can't explain it to an AI.*

**The autonomy level** — start at the lowest that works:

| Level | What happens |
|---|---|
| L1 Suggested | It suggests, you decide every time |
| L2 Drafted | It drafts, you review and send |
| L3 Supervised | It runs, you spot-check |
| L4 Hands-off | It runs end to end |

Default to the lowest. Earn each step up. *A boring workflow beats a clever agent.*

**The number** — which lever does this move: more customers, more value per customer, or less cost? Plus one specific metric (hours saved, reply rate, response time). If you can't name the number, don't build it.

---

## Move 3 — Construct (build it small, roll it out slow)

**Build small.** Smallest possible blocks, one input and one output each. Get the no-AI parts working first — fetching, formatting, routing — then add the AI where it actually earns its place. Test every block before you chain the next one. Never build the whole pipeline and pray.

**Roll out on Scaffolding.** Like teaching someone to ride a bike, take the supports off one at a time:

1. **Manual** — you run it, watch everything, fix by hand.
2. **Drafted** — it runs but only drafts; nothing goes out without you.
3. **Supervised** — it runs live, you check periodically, alerts on anything weird.
4. **Hands-off** — supports off. Go ride.

Even at 90% confidence, start with 10% of the volume. Watch a week. Widen.

**And keep the kill switch handy.** If an automation needs constant patching, produces junk, or costs more to babysit than it saves — tear it down. "I spent three weeks on this" is not a reason to keep something that doesn't work. Good architects know when to build *and* when to demolish.

---

## The three rules above everything

1. **Boring is beautiful.** The simplest, most predictable thing that works, wins.
2. **Finished vs. forever.** A no-AI script can be *done*. An AI step is never done — it evolves. Set expectations accordingly.
3. **Fail fast.** Get to your first ten mistakes as quickly and safely as you can. That's where the learning is — not in planning, not in your first ten wins.
