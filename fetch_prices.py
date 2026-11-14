"""Fetch Yahoo Finance end-of-day closes for every symbol in symbols.txt into prices.json."""
import json, re, sys, urllib.request, concurrent.futures as cf, datetime

def get(sym):
    u = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=1mo&interval=1d"
    r = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
    try:
        d = json.load(urllib.request.urlopen(r, timeout=20))["chart"]["result"][0]
    except Exception as e:
        return sym, None, str(e)
    m = d["meta"]; ts = d.get("timestamp", []); cl = d["indicators"]["quote"][0].get("close", [])
    pts = [(t, c) for t, c in zip(ts, cl) if c is not None]
    if not pts:
        return sym, None, "no data"
    close = round(pts[-1][1], 4); prev = round(pts[-2][1], 4) if len(pts) > 1 else close
    asof = datetime.datetime.fromtimestamp(pts[-1][0] + m.get("gmtoffset", 28800), datetime.timezone.utc).strftime("%Y-%m-%d")
    return sym, {"symbol": sym, "longName": m.get("longName") or m.get("shortName") or "",
                 "currency": m.get("currency", "MYR"), "close": close, "prevClose": prev, "asOf": asof,
                 "hi52": m.get("fiftyTwoWeekHigh"), "lo52": m.get("fiftyTwoWeekLow"),
                 "history": [round(c, 4) for _, c in pts[-22:]], "source": "Yahoo Finance daily close"}, None

syms = sorted({l.strip().upper() for l in open("symbols.txt")
               if re.fullmatch(r"[0-9A-Z]{4,8}\.KL", l.strip().upper())})
out, bad = {}, {}
with cf.ThreadPoolExecutor(8) as ex:
    for s, d, e in ex.map(get, syms):
        if d: out[s] = d
        else: bad[s] = e
print(len(out), "ok; failed:", bad)
if len(out) < max(1, len(syms) // 2):
    sys.exit("Too few quotes came back (Yahoo may be down); keeping the old prices.json")
json.dump({"quotes": out, "updatedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
           "source": "Yahoo Finance v8 chart API, daily close"}, open("prices.json", "w"))
