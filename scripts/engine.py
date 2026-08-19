#!/usr/bin/env python3
"""The Intelligence Wing engine — fetch, score, and rank niche news.

Free sources: Google News RSS, Hacker News (Algolia), Reddit RSS.
Scoring: Groq (free, if GROQ_API_KEY is set) with a keyword/recency
fallback so the engine NEVER runs dry. Stdlib only — no pip installs.

Usage:
  python3 scripts/engine.py "keyword one" "keyword two"
  python3 scripts/engine.py                     # reuses context/keywords.txt
  python3 scripts/engine.py --fixture sample-data/fixture-news.xml --no-groq
  python3 scripts/engine.py --top 5 --quiet     # for cron (Day 7)
"""
import json
import os
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYWORDS_FILE = os.path.join(ROOT, "context", "keywords.txt")
SIGNALS_FILE = os.path.join(ROOT, "context", "signals.json")
BUSINESS_FILE = os.path.join(ROOT, "context", "about-business.md")
HEADERS = {"User-Agent": "Mozilla/5.0 (BlueprintAIOS engine)"}


def fetch(url, timeout=15):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def parse_rss(xml_bytes, source):
    items = []
    root = ET.fromstring(xml_bytes)
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        if title:
            items.append({
                "title": title,
                "link": (item.findtext("link") or "").strip(),
                "published": (item.findtext("pubDate") or "").strip(),
                "source": source,
            })
    return items


def parse_atom(xml_bytes, source):
    items = []
    root = ET.fromstring(xml_bytes)
    for entry in root.iter():
        if not entry.tag.endswith("entry"):
            continue
        title, link, published = "", "", ""
        for child in entry:
            if child.tag.endswith("title"):
                title = (child.text or "").strip()
            elif child.tag.endswith("link"):
                link = child.get("href", "")
            elif child.tag.endswith("updated"):
                published = (child.text or "").strip()
        if title:
            items.append({"title": title, "link": link,
                          "published": published, "source": source})
    return items


def google_news(keyword):
    url = ("https://news.google.com/rss/search?q="
           + urllib.parse.quote(keyword) + "&hl=en-US&gl=US&ceid=US:en")
    return parse_rss(fetch(url), "Google News")[:15]


def hacker_news(keyword):
    url = ("https://hn.algolia.com/api/v1/search_by_date?tags=story&query="
           + urllib.parse.quote(keyword))
    data = json.loads(fetch(url))
    out = []
    for hit in data.get("hits", [])[:15]:
        title = hit.get("title") or ""
        if title:
            link = hit.get("url") or (
                "https://news.ycombinator.com/item?id=" + str(hit.get("objectID")))
            out.append({"title": title, "link": link,
                        "published": hit.get("created_at", ""),
                        "source": "Hacker News"})
    return out


def reddit(keyword):
    url = ("https://www.reddit.com/search.rss?q="
           + urllib.parse.quote(keyword) + "&sort=new")
    return parse_atom(fetch(url), "Reddit")[:10]


def gather(keywords, fixture=None):
    items, errors = [], []
    if fixture:
        with open(fixture, "rb") as f:
            items.extend(parse_rss(f.read(), "Fixture"))
        return items, errors
    for kw in keywords:
        for fn in (google_news, hacker_news, reddit):
            try:
                items.extend(fn(kw))
            except Exception as exc:  # a dead source must never kill the run
                errors.append("%s(%s): %s" % (fn.__name__, kw, exc))
    return items, errors


def dedupe(items):
    seen, out = set(), []
    for it in items:
        key = it["title"].lower()[:80]
        if key not in seen:
            seen.add(key)
            out.append(it)
    return out


def heuristic_score(items, keywords):
    kws = [k.lower() for k in keywords]
    for it in items:
        title = it["title"].lower()
        score = sum(3 for k in kws if k in title)
        score += sum(1 for k in kws for word in k.split() if word in title)
        it["score"] = min(10, score)
        it["tag"] = "keyword-match" if score else "weak"
    return items


def groq_score(items, keywords):
    key = os.environ.get("GROQ_API_KEY", "")
    if not key:
        return None
    business = ""
    if os.path.exists(BUSINESS_FILE):
        with open(BUSINESS_FILE, encoding="utf-8") as f:
            business = f.read()[:600]
    headlines = "\n".join(
        "%d. %s" % (i, it["title"]) for i, it in enumerate(items[:40]))
    prompt = (
        "You score news relevance for this business:\n"
        + (business or "niche keywords: " + ", ".join(keywords))
        + "\n\nScore each headline 0-10 for relevance and give a 1-3 word tag."
        "\nReturn ONLY a JSON array like"
        ' [{"i":0,"score":7,"tag":"pricing"}] — nothing else.\n\n' + headlines)
    body = json.dumps({
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
    }).encode()
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions", data=body,
        headers={"Authorization": "Bearer " + key,
                 "Content-Type": "application/json"})
    try:
        raw = json.loads(urllib.request.urlopen(req, timeout=30).read())
        text = raw["choices"][0]["message"]["content"]
        scores = json.loads(text[text.find("["):text.rfind("]") + 1])
        for row in scores:
            idx = int(row["i"])
            if 0 <= idx < len(items):
                items[idx]["score"] = int(row.get("score", 0))
                items[idx]["tag"] = str(row.get("tag", ""))[:30]
        for it in items:
            it.setdefault("score", 0)
            it.setdefault("tag", "")
        return items
    except Exception as exc:
        print("  (Groq scoring unavailable — using fallback: %s)" % exc,
              file=sys.stderr)
        return None


def load_or_save_keywords(args_keywords):
    os.makedirs(os.path.dirname(KEYWORDS_FILE), exist_ok=True)
    if args_keywords:
        with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(args_keywords) + "\n")
        return args_keywords
    if os.path.exists(KEYWORDS_FILE):
        with open(KEYWORDS_FILE, encoding="utf-8") as f:
            kws = [line.strip() for line in f if line.strip()]
        if kws:
            return kws
    sys.exit('No keywords. Run:  python3 scripts/engine.py "kw one" "kw two"')


def main(argv):
    fixture, use_groq, top, quiet, keywords = None, True, 10, False, []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--fixture":
            i += 1
            fixture = argv[i]
        elif a == "--no-groq":
            use_groq = False
        elif a == "--top":
            i += 1
            top = int(argv[i])
        elif a == "--quiet":
            quiet = True
        else:
            keywords.append(a)
        i += 1

    keywords = load_or_save_keywords(keywords)
    items, errors = gather(keywords, fixture)
    items = dedupe(items)
    if not items:
        sys.exit("No items fetched. Errors: " + "; ".join(errors))

    scored = groq_score(items, keywords) if use_groq else None
    if scored is None:
        scored = heuristic_score(items, keywords)
    ranked = sorted(scored, key=lambda x: x.get("score", 0), reverse=True)[:top]

    os.makedirs(os.path.dirname(SIGNALS_FILE), exist_ok=True)
    with open(SIGNALS_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "generated": datetime.now(timezone.utc).isoformat(),
            "keywords": keywords,
            "signals": ranked,
        }, f, indent=2)

    if not quiet:
        print("Intelligence engine — top %d of %d items "
              "(%d source errors)\n" % (len(ranked), len(items), len(errors)))
        for n, it in enumerate(ranked, 1):
            tag = " · " + it["tag"] if it.get("tag") else ""
            print("%2d. [%d] %s  (%s%s)" % (
                n, it.get("score", 0), it["title"], it["source"], tag))
        print("\nSaved to context/signals.json — "
              "ask your AIOS to run the brief skill on it.")


if __name__ == "__main__":
    main(sys.argv[1:])
