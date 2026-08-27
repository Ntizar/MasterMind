# Stakeholder Search — Limitations & Workarounds

## The Problem

Automated stakeholder discovery (finding real names of CTOs, CIOs, etc. for a given company) **does not work** with available tools:

| Tool | Why it fails |
|------|-------------|
| **LinkedIn** | Requires login. No credentials available. Scraping blocked. |
| **Google** | Returns CAPTCHA from server IP. Cannot bypass. |
| **DuckDuckGo** | No results or empty responses. |
| **SearXNG** | Similar to DuckDuckGo — limited results. |
| **Browser tools** | LinkedIn blocks automated browsers. Google CAPTCHA. |

## Workaround: Manual Search

For each account, the salesperson should spend ~30 seconds:

### LinkedIn (manual)
```
site:linkedin.com "Company Name" CTO
site:linkedin.com "Company Name" CIO
site:linkedin.com "Company Name" "Head of"
```

### Google (manual)
```
"Company Name" "nuevo CTO"
"Company Name" "contrata" CIO
"Company Name" "speaker" technology conference
```

### Job postings (often reveal managers)
```
"Company Name" "Head of Infrastructure"
"Company Name" "SAP Manager"
"Company Name" "Data Platform Lead"
```

## What the Skill Provides Instead

The generated report includes:
- **Role titles** (CTO, Head of Infra, SAP Manager, Head of Data)
- **Angles of approach** for each role
- **Common objections** and responses
- **Timing** for outreach

The salesperson fills in the **names** manually from LinkedIn.

## Never Attempt

- ❌ Automated LinkedIn scraping (no credentials, blocked)
- ❌ Google scraping from server (CAPTCHA)
- ❌ Browser-based LinkedIn login (requires real credentials)
- ❌ Residential proxy setup (out of scope, too complex)

## Bottom Line

**Automated report generation + manual stakeholder discovery** is the only viable approach. The skill focuses on everything EXCEPT names. Names are the salesperson's job.