#!/usr/bin/env python3
"""
framework.css holds the framework's default settings. framework-guide.html loads
it, lets you change those settings, and downloads the result as a new file you
name -- it never writes framework.css. This script does the jobs the guide can't:

  python3 build.py serve
      Opens the guide in your browser. Browsers won't let a double-clicked page
      read framework.css, so the guide is served from a local address instead.
      Leave it running while you use the guide; Ctrl-C stops it. Edit
      framework.css by hand any time and reload the guide to see the change.

  python3 build.py
      Rebuild check. Runs the guide's own generator (the same one behind its
      Download button) on framework.css and shows what a rebuild would change.
      Writes nothing. If you haven't changed the generator, any difference
      means the guide failed to read a setting back from framework.css.

  python3 build.py --write
      Same, then rewrites framework.css with the result, after copying the old
      one to framework.css.bak. Use this after changing the generator in
      framework-guide.html (a new section, a new setting) so framework.css
      gets it too.
"""
import argparse
import difflib
import http.server
import pathlib
import shutil
import sys
import threading
import webbrowser

HERE = pathlib.Path(__file__).resolve().parent
GUIDE = "framework-guide.html"
CSS = HERE / "framework.css"
PORT = 8765  # fixed, so the guide keeps its remembered download name between sessions


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(HERE), **kwargs)

    def end_headers(self):
        # reloading the guide always picks up the latest framework.css
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *args):
        pass


def start_server(port):
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def serve():
    try:
        server = start_server(PORT)
    except OSError:
        sys.exit(f"Port {PORT} is busy -- is the guide already running in another terminal?")
    url = f"http://127.0.0.1:{PORT}/{GUIDE}"
    print(f"Guide running at {url}\nCtrl-C to stop.")
    webbrowser.open(url)
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        server.shutdown()


def generate():
    from playwright.sync_api import sync_playwright, TimeoutError

    server = start_server(0)  # any free port
    url = f"http://127.0.0.1:{server.server_address[1]}/{GUIDE}"
    errors = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto(url)
            try:
                page.wait_for_function("typeof window.__buildFullCSS === 'function'", timeout=15000)
            except TimeoutError:
                sys.exit("The guide didn't finish loading framework.css.\n" + "\n".join(errors))
            css = page.evaluate("() => window.__buildFullCSS()")
            browser.close()
    finally:
        server.shutdown()
    if errors:
        sys.exit("The guide hit errors while building:\n" + "\n".join(errors))
    return css


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", nargs="?", choices=["serve"], help="open the guide in your browser")
    ap.add_argument("--write", action="store_true", help="rewrite framework.css (old copy kept as framework.css.bak)")
    args = ap.parse_args()

    if args.command == "serve":
        return serve()
    if not CSS.exists():
        sys.exit(f"Can't find {CSS}")

    old = CSS.read_text(encoding="utf-8")
    new = generate()
    diff = list(difflib.unified_diff(old.splitlines(), new.splitlines(), "framework.css", "rebuilt", lineterm=""))
    if not diff:
        print("framework.css is up to date -- a rebuild changes nothing.")
        return
    print("\n".join(diff))
    changed = sum(1 for line in diff if line[:1] in "+-" and line[:3] not in ("+++", "---"))
    if args.write:
        shutil.copy2(CSS, CSS.with_name("framework.css.bak"))
        CSS.write_text(new, encoding="utf-8")
        print(f"\nRewrote framework.css ({changed} lines changed); the old version is in framework.css.bak.")
    else:
        print(f"\n{changed} lines would change. Nothing written -- run with --write to apply.")


if __name__ == "__main__":
    main()
