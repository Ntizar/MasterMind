# Bicimad Calendar Sync Script

## Overview
`/hermes-home/scripts/bicimad-calendar-sync.py` creates 10 daily events in the "Mastermind 🤖" iCloud calendar for BiciMad station 298 monitoring (every 3 minutes from 07:45 to 08:18 Madrid time).

## How it works
1. Connects to iCloud CalDAV using hardcoded credentials (fallback from `ICLOUD_APP` env var)
2. Finds the "Mastermind 🤖" calendar by display name
3. Creates 10 VEVENT entries for today with 3-minute intervals
4. Skips events that already exist (checks by summary + date)
5. Returns count of created/skipped events

## Cron integration
- Job: `BiciMad Calendar Sync - Mastermind 🤖` (job_id: `d689240b09b5`)
- Schedule: `1 0 * * *` (00:01 Madrid, creates events for the next day)
- Mode: `no_agent=true` with `script` field pointing to the Python file
- Credentials hardcoded in script (fallback from `ICLOUD_APP` env var)

## Known limitations
- iCloud CalDAV is write-reliable but read-broken — events created successfully may not be listable via caldav API
- Always verify events in iOS/Calendar.app, not via caldav queries

## Events created
| Time (Madrid) | Summary |
|---|---|
| 07:45-07:48 | BiciMad 298 - Marques de Viana |
| 07:48-07:51 | BiciMad 298 - Marques de Viana |
| 07:51-07:54 | BiciMad 298 - Marques de Viana |
| 07:54-08:00 | BiciMad 298 - Marques de Viana |
| 08:00-08:03 | BiciMad 298 - Marques de Viana |
| 08:03-08:06 | BiciMad 298 - Marques de Viana |
| 08:06-08:09 | BiciMad 298 - Marques de Viana |
| 08:09-08:12 | BiciMad 298 - Marques de Viana |
| 08:12-08:15 | BiciMad 298 - Marques de Viana |
| 08:15-08:18 | BiciMad 298 - Marques de Viana |
