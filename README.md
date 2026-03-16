# Python File Organizer

A CLI tool that automatically organizes files in a directory by their type. Files are sorted into categorized folders like Images, Documents, Videos, Music, Archives, Code, and more.

## Features

- **Auto-sort** files into folders by extension
- **Dry-run mode** to preview changes before moving anything
- **Watch mode** to automatically organize new files as they appear
- **Undo** the last organization with a single command
- **Custom rules** via YAML config file
- **Rich output** with colored terminal logging
- **Conflict handling** — duplicate filenames get a numeric suffix

## Installation

```bash
git clone https://github.com/qorexdev/python-file-organizer.git
cd python-file-organizer
pip install -e .
```

Or install dependencies directly:

```bash
pip install -r requirements.txt
```

## Usage

### Basic — organize current directory

```bash
organize
```

### Organize a specific directory

```bash
organize ~/Downloads
```

### Preview changes without moving files

```bash
organize ~/Downloads --dry-run
```

### Verbose output

```bash
organize ~/Downloads --verbose
```

### Watch mode — auto-organize new files

```bash
organize ~/Downloads --watch
```

### Undo the last organization

```bash
organize ~/Downloads --undo
```

### Use a custom config

```bash
organize ~/Downloads --config config.yaml
```

### Combine flags

```bash
organize ~/Downloads --dry-run --verbose --config my_rules.yaml
```

## CLI Reference

```
Usage: organize [OPTIONS] [PATH]

  Organize files in a directory by type.

Options:
  -d, --dry-run          Preview changes without moving files.
  -v, --verbose          Show detailed output.
  -w, --watch            Watch directory and auto-organize new files.
  -u, --undo             Undo the last organization.
  -c, --config PATH      Path to YAML config file.
  --version              Show the version and exit.
  --help                 Show this message and exit.
```

## Default Categories

| Folder       | Extensions                                          |
|:-------------|:----------------------------------------------------|
| Images       | jpg, jpeg, png, gif, bmp, svg, webp, ico, tiff, ... |
| Documents    | pdf, doc, docx, xls, xlsx, ppt, pptx, txt, csv, ... |
| Videos       | mp4, avi, mkv, mov, wmv, flv, webm, ...             |
| Music        | mp3, wav, flac, aac, ogg, wma, m4a, ...             |
| Archives     | zip, rar, 7z, tar, gz, bz2, xz, ...                 |
| Code         | py, js, ts, java, c, cpp, go, rs, html, css, ...    |
| Executables  | exe, msi, dmg, app, deb, rpm, apk                   |
| Fonts        | ttf, otf, woff, woff2, eot                           |
| 3D Models    | obj, stl, fbx, blend, 3ds                            |

## Custom Config

Create a `config.yaml` to add or extend categories. See `config.example.yaml` for reference:

```yaml
categories:
  Design:
    - .psd
    - .ai
    - .sketch
  Ebooks:
    - .epub
    - .mobi
```

## License

MIT
