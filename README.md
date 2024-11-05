# 🫖 _kettled (kettle.d)_ 🫖
#### _A lightweight, efficient and secure scheduler._

[![repository](https://img.shields.io/badge/src-GitHub-8A2BE2)](https://github.com/solarvenom/kettled.py) [![mirror](https://img.shields.io/badge/mirror-GitLab-84e22c)](https://gitlab.com/open_source8171945/kettled.py) [![Build Status](https://img.shields.io/gitlab/pipeline-status/kettled.py)](https://github.com/solarvenom/kettled.py) [![release](https://img.shields.io/github/v/release/solarvenom/kettled.py)]() [![license](https://img.shields.io/badge/license-MIT-blue)](https://github.com/solarvenom/kettled.py/blob/main/LICENSE)

Kettled is a fast, efficient and secure daemon-based event scheduler for UNIX-systems that spawns an independent process which keeps track of your scheduled events with a nice CLI UI.

## Features
- ✨ Built with python built-in modules only. No third-party modules involved.
- ✨ An easy-to-use CLI UI to manage and monitor your scheduler daemon.
<p align="center">
    <img src="https://github.com/solarvenom/kettled.py/blob/main/docs/kettle.gif" width="450">
</p>

## Installation
`kettled` can be installed directly from the PyPI repositories with:

```bash
pip install kettled
```

## Example: *How to use kettled*

The following example shows how `Kettled` is instantiated and how basic `events` are scheduled.

```py
import datetime as dt

from kettled import Kettled

def foo():
    print("foo")

kettled = Kettled()
kettled.init()

event_datetime = dt.datetime.now() + dt.timedelta(hours=2)

kettled.add(event_name="readme_event", date_time=event_datetime, callback=foo)

kettled.update(event_name="readme_event", new_date_time=event_datetime + dt.timedelta(minutes=30))

kettled.delete(event_name="readme_event")
```

# CLI interface usage
To launch `kettled` from the terminal simply issue `kettled start`:
```text
user@pc$ kettled start 
🫖 kettled started.
```

Check daemon status via `kettled status`:
```text
user@pc$ kettled status
🫖 kettled has been up for 27 minutes and 56 seconds.
```

You can add events from the terminal by issueing `kettled add` and inputing the event data via prompts:
```text
user@pc$ kettled add
🫖 Please enter event name: readme_event
🫖 Please enter event scheduled date: 2024-11-05 10:17:57.587410
🫖 Please enter event callback: print('this is a callback function')
```

To update a scheduled event issue `kettled update` and go through the prompts to modify event data:
```text
user@pc$ kettled update
🫖 Please enter the name of event be modified: readme_event
🫖 Please enter the new event name or leave blank to leave unchanged: updated_readme_event
🫖 Please enter the new event schdeuled date or leave blank to leave unchanged: 
🫖 Please enter the new event callback or leave blank to leave unchanged: 
```

To check all scheduled events just issue `kettled list`:
```text
user@pc$ kettled list
user@pc$ 
_______________________________________________________
| Index |      Event Name      |    Scheduled Date    |
|-----------------------------------------------------|
|   1   | updated_readme_event | 2024-11-05T10:17:57  |
|_______|______________________|______________________|
```

Finally, to stop the kettled deamon simply issue `kettled stop`:
```text
user@pc$ kettled stop
🫖 kettled was terminated.
```
