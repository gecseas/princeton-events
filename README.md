# Princeton SEAS Events Aggregator

A lightweight, automatically-updated events board for Princeton School of Engineering and Applied Science (SEAS) departments and centers. Built and maintained by the [Graduate Engineering Council (GEC)](https://gec.princeton.edu).

---

## How it works

1. **GitHub Actions** runs the scraper every Monday and Thursday at 3 AM ET.
2. The scraper fetches events pages from each department/center and writes the results to `data/events.json`.
3. **GitHub Pages** serves `index.html`, which reads `data/events.json` and renders a filterable, sortable table.

No server. No database. No hosting cost.

---

## Repo structure

```
princeton-events/
├── index.html               # The public-facing events page
├── data/
│   └── events.json          # Auto-generated. Do not edit by hand.
├── scrapers/
│   ├── __init__.py
│   ├── run_all.py           # Entry point — runs all scrapers
│   ├── utils.py             # Shared fetch/parse helpers
│   ├── acee.py              # Andlinger Center
│   ├── citp.py              # Center for IT Policy
│   ├── cbe.py               # Chemical & Biological Engineering
│   ├── cee.py               # Civil & Environmental Engineering
│   ├── cs.py                # Computer Science
│   ├── ece.py               # Electrical & Computer Engineering
│   ├── mae.py               # Mechanical & Aerospace Engineering
│   ├── orfe.py              # Operations Research & Financial Engineering
│   └── pmi.py               # Princeton Materials Institute
├── requirements.txt
├── .github/
│   └── workflows/
│       └── scrape.yml       # GitHub Actions schedule
└── README.md
```

---

## Setup (one-time, for new maintainers)

### 1. Enable GitHub Pages
Go to **Settings → Pages** in this repo. Set source to **Deploy from branch**, branch `main`, folder `/ (root)`. Your site will be live at `https://gecseas.github.io/princeton-events/`.

### 2. Enable GitHub Actions email alerts
Go to your GitHub **account Settings → Notifications** and make sure "Actions" email notifications are on. You'll receive an email if the scraper fails.

### 3. Run locally (optional, for testing)
```bash
git clone https://github.com/gecseas/princeton-events.git
cd princeton-events
pip install -r requirements.txt
python -m scrapers.run_all
# Open index.html in your browser to see the result
```

---

## Adding a new department

1. Create `scrapers/my_dept.py` with a `scrape()` function that returns a list of event dicts.
2. Each dict must have at minimum: `title`, `date` (YYYY-MM-DD), `link`.
3. Optional fields: `time`, `location`, `speaker`, `description`, `tags`.
4. Import and add your module to the `SCRAPERS` list in `scrapers/run_all.py`.

Use an existing scraper (e.g. `cee.py`) as a template — they're all under 50 lines.

---

## Fixing a broken scraper

When a department redesigns their website, their scraper may stop finding events. You'll know because:
- GitHub Actions sends a failure email, **or**
- `data/events.json` shows the department in the `"failures"` list, **or**
- The events table shows a yellow warning banner.

To fix:
1. Open the department's events page in your browser and inspect the HTML (right-click → Inspect).
2. Find the CSS selectors that wrap each event's title, date, and location.
3. Update the selectors in the corresponding `scrapers/dept.py` file.
4. Test locally with `python -m scrapers.run_all` and confirm events appear.
5. Commit and push — the next scheduled run will use the updated scraper.

---

## Team handoff checklist

When you're rotating off the team, do the following **before you leave**:

- [ ] Add the incoming maintainer as an **Owner** of the `gecseas` GitHub organization.
- [ ] Walk them through this README (15 minutes is enough).
- [ ] Make sure they have GitHub notifications enabled so they receive failure alerts.
- [ ] Remove yourself as org Owner once they're set up.

---

## Sources

| Department / Center | Events URL |
|---|---|
| Andlinger Center for Energy & the Environment | https://acee.princeton.edu/events/ |
| Center for Information Technology Policy (CITP) | https://citp.princeton.edu/events/ |
| Chemical and Biological Engineering (CBE) | https://cbe.princeton.edu/events |
| Civil and Environmental Engineering (CEE) | https://cee.princeton.edu/events |
| Computer Science (CS) | https://www.cs.princeton.edu/events |
| DeCenter (Blockchain & Decentralization) | https://decenter.princeton.edu/events/ |
| Electrical and Computer Engineering (ECE) | https://ece.princeton.edu/events |
| Mechanical and Aerospace Engineering (MAE) | https://mae.princeton.edu/events |
| Omenn-Darling Bioengineering Institute (ODBI) | https://bioengineering.princeton.edu/events |
| Operations Research & Financial Engineering (ORFE) | https://orfe.princeton.edu/events |
| Princeton Materials Institute (PMI) | https://pmi.princeton.edu/events |

> **Note:** CEFRC, Gigascale Systems Research Center, and MIRTHE were omitted because
> they are defunct or no longer maintain active public events calendars.
> CEFRC's annual Summer School can be monitored manually at cefrc.princeton.edu.
