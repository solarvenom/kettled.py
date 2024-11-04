# 🫖 _kettled (kettle.d)_ 🫖
#### _A lightweight, efficient and secure scheduler._

[![repository](https://img.shields.io/badge/src-GitHub-8A2BE2)](https://github.com/solarvenom/kettled.py) [![mirror](https://img.shields.io/badge/mirror-GitLab-84e22c)](https://gitlab.com/open_source8171945/kettled.py) [![Build Status](https://img.shields.io/gitlab/pipeline-status/kettled.py)](https://github.com/solarvenom/kettled.py) [![release](https://img.shields.io/github/v/release/solarvenom/kettled.py)]() [![license](https://img.shields.io/badge/license-MIT-blue)](https://github.com/solarvenom/kettled.py/blob/main/LICENSE)
Kettled is a fast, efficient and secure daemon-based event scheduler for UNIX-systems that spawns an independent process which keeps track of your scheduled events with a nice CLI UI.

## Features

- ✨ Built with python built-in modules only. No third-party modules involved.
- ✨ An easy-to-use CLI UI to manage and monitor your scheduler daemon.

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

kettled.add(event_name="readme_event", date_time=dt.timedelta(minutes=10), callback=foo)

kettled.update(event_name="readme_event", new_date_time=dt.timedelta(minutes=30))

kettled.delete(event_name="readme_event")
```

