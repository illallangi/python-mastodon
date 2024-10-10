## v0.3.3 (2024-10-10)

### Refactor

- **diffsync**: moved models to diffsyncmodels

## v0.3.2 (2024-10-07)

### Fix

- **client**: updated client to return datetime and date objects when appropriate

## v0.3.1 (2024-10-06)

### Fix

- **status**: replaced status: int with content: str

## v0.3.0 (2024-10-06)

### Feat

- **mastodonadapter**: added adapter and status model

### Fix

- **mastodon**: added id and url to all output
- **mastodon-tools**: fixed column width when stdout is redirected
- **status**: replaced uri with url

## v0.2.0 (2024-10-06)

### Feat

- **diffsync**: added adapter and model classes

### Refactor

- **client**: move client code into a class and mixins

## v0.1.0 (2024-10-05)

### Feat

- **all**: initial release
