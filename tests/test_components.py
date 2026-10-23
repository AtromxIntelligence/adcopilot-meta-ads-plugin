"""The skills, the commands and the README: what the model reads and what the
directory's reviewer reads. Held here because a slip in any of them reaches a
customer or the connector and nothing else would notice: front matter that
parses (a plain value holding a colon and a space does not, in YAML), only
tools the connector really has, by bare name, and only the ones each skill is
meant to use; the connector's first call with this plugin's name and version
in its `source`; the approval and today-and-later paragraphs; the README.

Stdlib only; reads no environment variable. Run with
`python3 -m unittest discover -s tests -v` from the repository root.
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

VERSION = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text("utf-8"))["version"]
NAME = "adcopilot-meta-ads"
SOURCE = "claude-plugin/%s/%s" % (NAME, VERSION)

TODAY_AND_LATER = "Today AdCopilot works through its Google connection: it checks your Meta Pixel in Google Tag Manager, reports Facebook and Instagram traffic and key events in Google Analytics (GA4), finds UTM mistakes, guides conversion setup, plans campaigns, drafts ad copy and does budget pacing math. It does not read your Meta ad account yet: direct access comes when Meta approves AdCopilot's API access, and no date is promised."

APPROVAL = "Every change is proposed first, with what it changes and how to undo it, and is made only after the customer's explicit yes in this conversation, to the change exactly as stated. A yes given earlier is asked for again. Tag Manager changes are staged in the AdCopilot workspace and never published: publishing is the customer's own click in Tag Manager. Nothing is ever deleted."

TRADEMARK = ("Not affiliated with or endorsed by Meta Platforms, Inc. Meta, Facebook and Instagram "
             "are trademarks of Meta Platforms, Inc.")

# Each skill, and the connector tools it must name, and no others.
SKILL_TOOLS = {
    "meta-ads-tracking": [
        "get_org_context",
        "gtm_list_accounts",
        "gtm_list_containers",
        "gtm_list_workspaces",
        "gtm_list_tags",
        "gtm_list_triggers",
        "gtm_list_version_headers",
        "gtm_list_built_in_variables",
        "gtm_enable_built_in_variable",
        "gtm_create_trigger",
        "gtm_create_tag",
    ],
    "meta-ads-traffic": [
        "get_org_context",
        "ga4_list_account_summaries",
        "ga4_get_metadata",
        "ga4_run_report",
        "ga4_list_conversion_events",
    ],
    "meta-ads-plan": [
        "get_org_context",
    ],
    "meta-ads-budget": [],
}
COMMANDS = ["setup", "check", "plan"]

# The writes the connector has, by name prefix, and the only ones any skill
# here may use: Tag Manager changes, staged and never published.
WRITE_PREFIXES = ("add_", "attach_", "create_", "link_", "pause_", "remove_",
                  "save_", "set_", "update_", "ga4_create_", "ga4_update_",
                  "ga4_provision_", "gsc_submit_", "gsc_request_",
                  "gtm_create_", "gtm_update_", "gtm_enable_")
STAGED_WRITES = {"gtm_create_tag", "gtm_create_trigger", "gtm_enable_built_in_variable"}

# Switched off in production at the version this plugin is written against.
SWITCHED_OFF = ["shopping_product_issues", "lsa_leads", "lsa_rate_lead"]

# A backticked snake_case word that starts like one of these is a tool name.
TOOL_PREFIXES = ("gsc_", "ga4_", "gtm_", "add_", "analyze_", "attach_",
                 "create_", "get_", "link_", "list_", "pause_", "remove_",
                 "save_", "set_", "update_")


def connector_tools():
    lines = (ROOT / "tests" / "connector_tools.txt").read_text("utf-8").splitlines()
    return {l.strip() for l in lines if l.strip() and not l.startswith("#")}


def read(path):
    return Path(path).read_text(encoding="utf-8")


def text_files():
    """Every text file in the plugin folder."""
    found = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if path.suffix in (".png", ".pyc"):
            continue
        found.append(path)
    return found


def skill_files():
    return sorted((ROOT / "skills").glob("*/SKILL.md"))


def command_files():
    return sorted((ROOT / "commands").glob("*.md"))


def squash(text):
    """Whitespace folded, so a paragraph wrapped differently is the same text."""
    return " ".join(text.split())


def front_matter(path):
    """(fields, body) of a file that opens with a block of `key: value`
    lines. Fails on a value YAML would read differently from the model: a
    list, a block scalar, or a plain scalar holding a colon or a hash."""
    text = read(path)
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise AssertionError("%s has no front matter" % path)
    fields = {}
    for line in match.group(1).split("\n"):
        key, sep, value = line.partition(":")
        if not sep or not re.match(r"^[a-z][a-z-]*$", key):
            raise AssertionError("%s: front matter line is not key: value: %r" % (path, line))
        value = value.strip()
        if value[:1] in "\"'":
            if len(value) < 2 or value[-1] != value[0]:
                raise AssertionError("%s: unbalanced quote in %s" % (path, key))
            value = value[1:-1]
        else:
            if value[:1] in "[{|>-&*!%@`#":
                raise AssertionError("%s: %s starts like a YAML list, block or tag" % (path, key))
            if ": " in value or " #" in value or value.endswith(":"):
                raise AssertionError("%s: %s holds a colon or hash YAML would split" % (path, key))
        fields[key] = value
    return fields, text[match.end():]


class FrontMatter(unittest.TestCase):

    def test_every_skill_and_command_parses_and_carries_its_name(self):
        self.assertEqual([p.parent.name for p in skill_files()], sorted(SKILL_TOOLS))
        self.assertEqual([p.stem for p in command_files()], sorted(COMMANDS))
        for path in skill_files() + command_files():
            fields, _ = front_matter(path)
            expected = path.parent.name if path.name == "SKILL.md" else path.stem
            self.assertEqual(fields.get("name"), expected, path)
            description = fields.get("description")
            self.assertTrue(isinstance(description, str) and description.strip(), path)
            self.assertLessEqual(len(description), 700, path)
            if path.name == "SKILL.md":
                self.assertIn("Use when ", description, path)
            self.assertEqual(set(fields), {"name", "description"}, path)


class ToolNames(unittest.TestCase):

    def test_every_tool_a_skill_or_command_names_is_the_connectors(self):
        tools = connector_tools()
        self.assertGreater(len(tools), 100)
        for path in skill_files() + command_files() + [ROOT / "README.md"]:
            for token in re.findall(r"`([a-z][a-z0-9_]*)`", read(path)):
                if token.startswith(TOOL_PREFIXES):
                    self.assertIn(token, tools, "%s names %s, not a connector tool" % (path, token))

    def test_each_skill_names_exactly_the_tools_it_is_meant_to(self):
        for path in skill_files():
            named = {t for t in re.findall(r"`([a-z][a-z0-9_]*)`", read(path))
                     if t in connector_tools()}
            self.assertEqual(named, set(SKILL_TOOLS[path.parent.name]), path)

    def test_no_tool_is_named_by_the_prefix_the_client_adds(self):
        # The prefix belongs to whichever AdCopilot plugin loaded first.
        marker = "mcp__" + "plugin_"
        for path in text_files():
            self.assertNotIn(marker, read(path), path)

    def test_nothing_switched_off_is_named(self):
        for path in text_files():
            if path.name == "test_components.py":
                continue
            text = read(path)
            for name in SWITCHED_OFF:
                self.assertNotIn(name, text, "%s names %s" % (path, name))

    def test_every_write_is_a_staged_tag_manager_change(self):
        for name, tools in SKILL_TOOLS.items():
            for tool in tools:
                if tool.startswith(WRITE_PREFIXES):
                    self.assertIn(tool, STAGED_WRITES, "%s uses the write tool %s" % (name, tool))
            if STAGED_WRITES & set(tools):
                text = squash(read(ROOT / "skills" / name / "SKILL.md"))
                self.assertIn("never published", text)
                self.assertIn("AdCopilot workspace", text)


class FirstCall(unittest.TestCase):

    def test_the_connectors_first_call_carries_this_plugins_name_and_version(self):
        for path in skill_files() + command_files():
            text = read(path)
            if "get_org_context" not in text:
                continue
            self.assertIn('source: "%s"' % SOURCE, text, path)
            self.assertIn('source: "claude-scheduled"', text, path)
            # Never the bare marker, and never a version with no name: the
            # server would read either as the main plugin.
            self.assertEqual(re.findall(r"claude-plugin(?!/)", text), [], path)
            for found in re.findall(r"claude-plugin/[^\s\"'`]*", text):
                self.assertEqual(found, SOURCE, path)

    def test_a_skill_that_calls_no_tool_names_no_source(self):
        text = read(ROOT / "skills" / "meta-ads-budget" / "SKILL.md")
        self.assertNotIn("get_org_context", text)
        self.assertNotIn("claude-plugin", text)

    def test_every_tool_using_skill_makes_that_call_first(self):
        for path in skill_files():
            if path.parent.name == "meta-ads-budget":
                continue
            text = squash(read(path))
            self.assertIn("Call `get_org_context` before any other AdCopilot tool", text, path)
            self.assertIn("this plugin schedules nothing itself", text, path)
            self.assertIn("`next_step` and `playbook` are about the account", text, path)
            self.assertIn("exactly as the server returned it", text, path)
            self.assertIn("never a link from memory", text, path)

    def test_nothing_here_schedules_anything(self):
        for path in skill_files() + command_files():
            text = read(path).lower()
            self.assertNotIn("/schedule", text, path)
            self.assertNotIn("every weekday", text, path)


class Paragraphs(unittest.TestCase):

    def test_every_skill_holds_the_approval_paragraph(self):
        for path in skill_files():
            self.assertIn(squash(APPROVAL), squash(read(path)), path)

    def test_every_skill_and_setup_say_what_works_today_and_what_does_not(self):
        for path in skill_files() + [ROOT / "commands" / "setup.md"]:
            self.assertIn(squash(TODAY_AND_LATER), squash(read(path)), path)

    def test_the_paragraph_says_plainly_what_is_not_there_and_promises_no_date(self):
        self.assertIn("does not read your Meta ad account", TODAY_AND_LATER)
        self.assertIn("no date is promised", TODAY_AND_LATER)

    def test_the_skills_say_it_is_claudes_own_work_where_it_is(self):
        for name in ("meta-ads-plan", "meta-ads-budget"):
            self.assertIn("AdCopilot reads no Meta data for this",
                          read(ROOT / "skills" / name / "SKILL.md"))

    def test_checked_facts_carry_the_day_they_were_checked(self):
        for path in skill_files():
            for day in re.findall(r"checked (\d+ [A-Z][a-z]+ \d{4})", read(path)):
                self.assertEqual(day, "23 October 2026", path)


class Readme(unittest.TestCase):

    def setUp(self):
        self.text = read(ROOT / "README.md")

    def test_it_holds_the_trademark_line_and_the_maker(self):
        text = squash(self.text)
        self.assertIn("Made by Atromx Intelligence (https://adcopilot.cloud).", text)
        self.assertIn(squash(TRADEMARK), text)
        self.assertIn("not related to other products named AdCopilot", text)
        self.assertIn(squash(TODAY_AND_LATER), text)

    def test_it_is_long_enough_outside_its_code_fences(self):
        outside = re.sub(r"```.*?```", " ", self.text, flags=re.S)
        words = len(outside.split())
        self.assertGreaterEqual(words, 600)
        self.assertLessEqual(words, 1200)

    def test_it_says_one_connector_one_sign_in(self):
        text = squash(self.text)
        self.assertIn("one connector and one sign-in, whichever AdCopilot plugins you add", text)
        self.assertIn("run `/mcp` and sign in once", text)

    def test_it_has_the_sections_the_directory_and_a_customer_look_for(self):
        for heading in ("## Install", "## Already use another AdCopilot plugin?",
                        "## What you get", "## What it will not do", "## Data",
                        "## Support", "## Version", "## Licence", "## What CI runs"):
            self.assertIn("\n" + heading + "\n", self.text, heading)
        self.assertIn("Free plan available; paid plans on https://adcopilot.cloud/pricing",
                      self.text)

    def test_the_version_paragraph_matches_the_manifest(self):
        found = re.search(
            r"\*\*(\d+\.\d+\.\d+) \((\d{4}-\d{2}-\d{2}), written against AdCopilot "
            r"(v\d+\.\d+\.\d+), live since (\d{4}-\d{2}-\d{2})\)\*\*", self.text)
        self.assertIsNotNone(found)
        self.assertEqual(found.group(1), VERSION)

    def test_the_install_lines_name_this_repo_and_this_plugin(self):
        self.assertIn("/plugin marketplace add AtromxIntelligence/adcopilot-meta-ads-plugin", self.text)
        self.assertIn("/plugin install %s@adcopilot-meta-ads-plugin" % NAME, self.text)


if __name__ == "__main__":
    unittest.main()
