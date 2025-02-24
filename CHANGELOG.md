# Change Log
All notable changes to this project will be documented in this file.

## [1.1.0] - 2025-02-24

### Added
- Persistent storage for events has been implemented. Kettled now "remembers" events in-between sessions.
- A recurrency mechanism has been implemented for events has been implemented in case an event is meant to run recurrently. It is set via the `recurrency` field when creating/updating an event and can be one of the enumerables from [RECURRENCY_OPTIONS_ENUM](https://github.com/solarvenom/kettled.py/blob/main/src/kettled/constants/enums/recurrency_options_enum.py) and defaults to `not_recurring`.
- A fallback mechanism has been implemented to deal with events that expired while Kettled was down. It is set via the `fallback_directive` field when creating/updating an event and can be one of the enumerables from [FALLBACK_DIRECTIVES_ENUM](https://github.com/solarvenom/kettled.py/blob/main/src/kettled/constants/enums/fallback_options_enum.py) and defaults to `execute_as_soon_as_possible`.
- Event datetime can now be also set by passing one of the enumerables from [RELATIVE_DATETIME_OPTIONS_ENUM](https://github.com/solarvenom/kettled.py/blob/main/src/kettled/constants/enums/relative_datetime_options_enum.py) into the `date_time` field when creating/updating an event to set event `date_time` relative to current time.

### Changed
- Kettled is not compatible with Python `v3.9` and onwards.
- Kettled now starts by default in persitent mode with SQLite.
- To run an in-memory only session Kettled now requires to be explicitly started as `kettled start in-memory-only`