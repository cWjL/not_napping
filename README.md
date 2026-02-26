# not_napping

Tools to make your boss think you're working, when you're really doing something else.

## What it does

Simulates realistic human activity across multiple channels so you appear active:

- **Mouse** — bezier-curve movements with jitter and overshoot (not detectable circles)
- **Typing** — Markov-chain generated office prose with typos and corrections
- **Scrolling** — incremental scrolls with direction bias and read-and-return
- **App switching** — Cmd-Tab / Alt-Tab with multi-window browsing
- **File access** — creates, reads, and deletes scratch files in `~/.not_napping/scratch/`

Activity follows burst/lull timing patterns that mimic real human work rhythms.

## Install

```bash
pip install -e .
```

## Usage

```bash
# All behaviors, max 30s delay between activity bursts
not-napping -d 30

# Or run as a module
python -m not_napping -d 30

# Verbose mode — prints each action
not-napping -d 20 -v

# Disable specific behaviors
not-napping -d 30 --no-typing --no-switching

# Available flags
#   --no-mouse      --no-typing     --no-scrolling
#   --no-switching   --no-files
```

Stop with **Ctrl+C**.

## Requirements

- Python 3.8+
- pyautogui >= 0.9.53
- macOS, Linux, or Windows (not WSL)
