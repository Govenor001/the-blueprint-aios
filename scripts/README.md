# Scripts — the two engines that ship with the kit

Both are plain Python 3 (already on your Mac/Linux machine), standard
library only — nothing to install. Load your keys first:

```
set -a && . ./.env && set +a
```

## engine.py — the Intelligence Wing (Day 3)

Fetches your niche's news from Google News, Hacker News, and Reddit
(all free, no signup), scores it with Groq (free) or a built-in
fallback, and writes the ranked result to `context/signals.json` for
the `brief` skill.

```
python3 scripts/engine.py "keyword one" "keyword two"   # first run
python3 scripts/engine.py                               # reuses keywords
python3 scripts/engine.py --top 5 --quiet               # for schedules
```

Self-test without internet or keys:

```
python3 scripts/engine.py "small business bookkeeping" \
  --fixture sample-data/fixture-news.xml --no-groq
```

## bridge.py — the Command Wing (Day 6)

Connects your Telegram bot to your AIOS. Runs on your laptop; texting
your bot runs `claude -p` here and sends the answer back. Voice notes
work when `GROQ_API_KEY` is set.

```
python3 scripts/bridge.py --check    # verify token, chat id, claude CLI
python3 scripts/bridge.py            # run it (Ctrl+C to stop)
echo "test" | python3 scripts/bridge.py --send-stdin   # push to yourself
```

Safety: the bridge answers **only** your `TELEGRAM_CHAT_ID`. Until you
set it, it replies to any message with your id and does nothing else.

If either script misbehaves, run `/rescue` in Claude Code.
