"""What the plugin directory's scanner and reviewer look for. The plugin is
instructions only: nothing in it reads a credential, launches a package,
downloads and runs anything, names a price, or claims to be the platform's own
product. Patterns are built by joining pieces, so this file never matches
itself. Stdlib only; reads no environment variable.
"""

import json
import os
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OWNERS = ["Meta", "Facebook", "Instagram", "Google"]
# The README's trademark disclaimer says "endorsed by <owner>"; it is taken
# out before the "by <owner>" check.
DISCLAIMER = ("Not affiliated with or endorsed by Meta Platforms, Inc. Meta, Facebook and Instagram "
              "are trademarks of Meta Platforms, Inc.")
PRICE_SENTENCE = ("Free plan available; paid plans on https://adcopilot.cloud/pricing")

CREDENTIAL_READS = [
    "os" + r"\.environ",
    "get" + r"env\(",
    "process" + r"\.env",
    r"\$\{[^}]*(?:TO" + "KEN|SEC" + "RET|K" + "EY|PASS" + r"WORD)[^}]*\}",
    "Author" + "ization:",
    "Bear" + "er ",
]
LAUNCHERS = [r"\bnp" + r"x\b", r"\bbun" + r"x\b", r"\bpnpm" + r" dlx\b",
             r"\byarn" + r" dlx\b", r"\buv" + r"x\b", r"\bpipx" + r" run\b",
             r"\buv" + r" run\b"]
DOWNLOAD_AND_RUN = r"(?:cu" + "rl|wg" + r"et)[^|;\n]*\|\s*(?:sudo\s+)?(?:ba)?sh"
REFUSED_NAMES = [".DS_" + "Store", "Thumbs" + ".db", "desktop" + ".ini", "__MAC" + "OSX",
                 ".git" + "modules", ".git" + "attributes"]
REFUSED_SUFFIXES = (".mc" + "pb", ".d" + "xt")
CLAIMED_STATUS = "offi" + "cial"


def files():
    """Every file in the plugin folder, tracked or not yet committed."""
    try:
        out = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            cwd=ROOT, capture_output=True, check=True).stdout
        names = [n for n in out.decode("utf-8").split("\0") if n]
    except (OSError, subprocess.CalledProcessError):
        names = []
        for dirpath, dirs, found in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
            names += [os.path.relpath(os.path.join(dirpath, f), ROOT) for f in found]
    return sorted(n for n in set(names) if (ROOT / n).exists() or (ROOT / n).is_symlink())


def text_of(name):
    path = ROOT / name
    if path.suffix in (".png", ".pyc"):
        return ""
    return path.read_text(encoding="utf-8")


class Hygiene(unittest.TestCase):

    def test_there_are_files_to_check(self):
        self.assertGreater(len(files()), 10)

    def test_no_file_reads_a_credential(self):
        for name in files():
            text = text_of(name)
            for pattern in CREDENTIAL_READS:
                self.assertIsNone(re.search(pattern, text), "%s matches %s" % (name, pattern))

    def test_no_package_launcher_anywhere(self):
        for name in files():
            text = text_of(name)
            for pattern in LAUNCHERS:
                self.assertIsNone(re.search(pattern, text), "%s matches %s" % (name, pattern))

    def test_no_download_and_execute_pattern(self):
        for name in files():
            self.assertIsNone(re.search(DOWNLOAD_AND_RUN, text_of(name)), name)

    def test_no_file_the_directory_refuses(self):
        for name in files():
            path = Path(name)
            self.assertNotIn(path.name, REFUSED_NAMES, name)
            for part in path.parts:
                self.assertNotIn(part, REFUSED_NAMES, name)
            self.assertFalse(path.name.endswith(REFUSED_SUFFIXES), name)
            self.assertFalse((ROOT / name).is_symlink(), "%s is a symlink" % name)
            self.assertNotEqual(path.parts[0], "bin", name)
            self.assertNotEqual(path.name, "CLAUDE.md", name)
        self.assertFalse((ROOT / "hooks").exists())
        self.assertFalse((ROOT / "agents").exists())
        self.assertFalse((ROOT / "package.json").exists())

    def test_the_plugin_has_no_other_folder_than_the_ones_it_needs(self):
        top = {Path(n).parts[0] for n in files() if len(Path(n).parts) > 1}
        self.assertEqual(top, {".claude-plugin", ".github", "commands", "skills", "tests"})

    def test_the_price_sentence_is_the_only_word_about_price(self):
        for name in files():
            text = text_of(name).replace(PRICE_SENTENCE, "")
            self.assertIsNone(re.search(r"\$\s?\d", text), "%s names a price" % name)
            self.assertNotIn("/" + "mo", text.replace("/mcp", ""), name)

    def test_nothing_claims_to_be_the_platforms_own_product(self):
        by_owner = re.compile(r"\bby (?:%s)\b" % "|".join(OWNERS))
        for name in files():
            text = text_of(name)
            self.assertNotIn(CLAIMED_STATUS, text.lower(), name)
            if name.startswith("tests/"):
                continue  # the tests quote the rule itself
            text = " ".join(text.replace(DISCLAIMER, "").split())
            for found in by_owner.finditer(text):
                before = text[max(0, found.start() - 4):found.start()]
                self.assertEqual(before, "not ", "%s: %r" % (name, text[found.start() - 30:found.end()]))

    def test_the_icon_is_the_one_png_and_nothing_else_is_an_image(self):
        images = [n for n in files() if Path(n).suffix.lower() in
                  (".png", ".svg", ".jpg", ".jpeg", ".gif", ".webp", ".ico")]
        icon = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text("utf-8"))["icon"]
        self.assertEqual(images, [icon[2:] if icon.startswith("./") else icon])


if __name__ == "__main__":
    unittest.main()
