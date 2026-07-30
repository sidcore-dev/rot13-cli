# rot13-cli

A small, dependency-free command-line tool that applies ROT13 — or any
Caesar-style letter shift — to text.

**This has no cryptographic security value.** ROT13 is a letter-substitution
novelty, historically used on Usenet to hide spoilers, punchlines, and
puzzle answers from casual glances — not to protect anything sensitive.
Anyone (or any script) can reverse it instantly. Treat it exactly like the
classic Unix `rot13` command it clones: a text-obfuscation toy, nothing more.

## Why

Most systems don't ship a `rot13` command by default anymore, and the
`tr` one-liner for it is easy to fumble. `rot13-cli` gives you the classic
behavior back, plus a generalized `--shift` for any Caesar cipher, not
just the 13-position case.

## Install

```bash
pip install .
```

This installs a `rot13-cli` command on your PATH.

## Usage

```bash
$ rot13-cli "Hello, World!"
Uryyb, Jbeyq!

$ rot13-cli "Uryyb, Jbeyq!"
Hello, World!
```

Read from stdin or a file, and use a custom shift:

```bash
$ echo "attack at dawn" | rot13-cli
nggnpx ng qnja

$ rot13-cli --file message.txt --shift 3
$ rot13-cli --file message.txt --shift 3 --decode
```

### Options

| Flag       | Description                                                       |
|------------|------------------------------------------------------------------------|
| `text`      | Text to transform, given as arguments (default: read from stdin)      |
| `--file`    | Path to read input from instead of args/stdin                         |
| `--shift`   | Number of alphabet positions to shift (default: 13, i.e. ROT13)       |
| `--decode`  | Reverse the shift (same as negating `--shift`)                         |

### Behavior notes

- Only ASCII letters are shifted; case is preserved, and digits,
  punctuation, and whitespace pass through unchanged.
- With the default shift of 13, applying the transform twice returns the
  original text — ROT13 is its own inverse, so there's no real difference
  between "encoding" and "decoding" at that shift.
- For any other `--shift`, use `--decode` (or shift by `26 - N`) to
  reverse it.

### Exit codes

- `0` — completed successfully
- `2` — the input file couldn't be read

## Development

```bash
pip install -e .
python -m unittest discover -s tests -v
```

## License

All rights reserved. This code is public for viewing and reference only —
no license is granted to use, copy, modify, or redistribute it. See
[LICENSE](LICENSE) for details.
