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
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

When opening a new terminal, activate the venv first:

```bash
source .venv/bin/activate
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

## Heads up

When you start `not_napping`, it will immediately begin controlling your mouse, keyboard, and switching between windows. **Don't be alarmed** — this is expected behavior. You'll see:

- Your mouse cursor moving on its own
- A TextEdit (macOS), Notepad (Windows), or default text editor window open and receive typed text
- Random scrolling in the active window
- Apps switching via Cmd-Tab / Alt-Tab
- Scratch files appearing in `~/.not_napping/scratch/`

Make sure you're ready to step away before running it. Use **Ctrl+C** to stop at any time.

## Accessibility permissions

Your OS may require you to grant accessibility/input control permissions before `not_napping` can operate:

- **macOS** — Go to System Settings > Privacy & Security > Accessibility and enable your terminal app (e.g., Terminal, iTerm2). You may also need to allow it under Input Monitoring.
- **Linux** — On Wayland, tools like pyautogui have limited support. X11 is recommended. No special permissions are typically needed on X11.
- **Windows** — Generally works out of the box. If running as a non-admin user and targeting elevated windows, you may need to run your terminal as Administrator.

If you see errors about input control or the mouse/keyboard not responding, check these permissions first.

## Process disguise

The process automatically masks itself in Activity Monitor / task managers. After startup it renames itself to `python3` and clears its command-line arguments, so it looks like any other Python script — no `not_napping` visible anywhere in the process list.

## Requirements

- Python 3.8+
- pyautogui >= 0.9.53
- setproctitle >= 1.3
- macOS, Linux, or Windows (not WSL)
