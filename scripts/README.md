# Scripts — the two engines that ship with the kit

Both are plain Python 3 on the AIOS server. The installer already creates the
services and schedules. Load optional keys from the private environment file:

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

Connects your Telegram bot to your AIOS. It runs as the server's Command Wing;
texting your bot runs `claude -p` there and sends the answer back. Voice notes
work when `GROQ_API_KEY` is set.

```
python3 scripts/bridge.py --check    # verify token, chat id, claude CLI
python3 scripts/bridge.py            # run it (Ctrl+C to stop)
echo "test" | python3 scripts/bridge.py --send-stdin   # push to yourself
```

Safety: the bridge answers **only** your `TELEGRAM_CHAT_ID`. Until you
set it, it replies to any message with your id and does nothing else.

If either script misbehaves, run `/rescue` in Claude Code.

## usage_report.py — measure the route honestly

After the bridge or a skill has run, inspect structured activity without inventing
token counts or provider billing:

```
python3 scripts/usage_report.py
```

The report counts skill starts and finishes and groups them by resolved model. Cost
stays `UNAVAILABLE` unless the provider supplies billing data.
