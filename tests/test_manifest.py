"""plugin.json, marketplace.json and .mcp.json: what the directory reads first.
The connector file is the same text in every AdCopilot plugin, so two of them
installed together point at one connector and one sign-in.

Stdlib only; reads no environment variable. Run with
`python3 -m unittest discover -s tests -v` from the repository root.
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NAME = "adcopilot-meta-ads"
REPO = "adcopilot-meta-ads-plugin"
DISPLAY_NAME = "AdCopilot for Meta Ads (Facebook & Instagram Ads)"
OWNER = "Meta"
SUPPORT_TAIL = "Made by Atromx Intelligence, not by Meta."

# Key order as the reference plugin writes it.
FIELDS = [
    "name", "version", "description", "author", "homepage", "documentationUrl",
    "privacyPolicyUrl", "termsOfServiceUrl", "supportUrl", "repository",
    "license", "keywords", "displayName", "icon",
]

# The connector file: the same text in every AdCopilot plugin. Same key, so the
# Connectors tab names it the same everywhere; same address spelling, because
# Claude matches a connector by its address.
MCP_TEXT = '{"mcpServers":{"adcopilot":{"type":"http","url":"https://mcp.adcopilot.cloud/mcp"}}}'
MCP = {"mcpServers": {"adcopilot": {"type": "http",
                                    "url": "https://mcp.adcopilot.cloud/mcp"}}}


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


class PluginJson(unittest.TestCase):

    def setUp(self):
        self.plugin = load(".claude-plugin/plugin.json")

    def test_the_field_set_and_order_are_the_references(self):
        self.assertEqual(list(self.plugin), FIELDS)

    def test_name_is_the_permanent_one_and_obeys_the_directorys_rule(self):
        self.assertEqual(self.plugin["name"], NAME)
        self.assertRegex(self.plugin["name"], r"^[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?$")

    def test_display_name_is_exactly_the_decided_one(self):
        self.assertEqual(self.plugin["displayName"], DISPLAY_NAME)

    def test_version_is_semver(self):
        self.assertRegex(self.plugin["version"], r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")

    def test_author_is_atromx_intelligence(self):
        self.assertEqual(self.plugin["author"],
                         {"name": "Atromx Intelligence", "url": "https://adcopilot.cloud"})

    def test_urls_are_the_checked_ones(self):
        p = self.plugin
        self.assertEqual(p["homepage"], "https://adcopilot.cloud")
        # /docs answers with a redirect to /docs/, so the slash is the address.
        self.assertEqual(p["documentationUrl"], "https://adcopilot.cloud/docs/")
        self.assertEqual(p["privacyPolicyUrl"], "https://adcopilot.cloud/privacy")
        self.assertEqual(p["termsOfServiceUrl"], "https://adcopilot.cloud/terms")
        self.assertEqual(p["supportUrl"],
                         "https://github.com/AtromxIntelligence/%s/issues" % REPO)
        self.assertEqual(p["repository"], "https://github.com/AtromxIntelligence/%s" % REPO)

    def test_every_url_is_https(self):
        urls = [self.plugin[k] for k in self.plugin if k.endswith("Url")]
        urls += [self.plugin["homepage"], self.plugin["repository"],
                 self.plugin["author"]["url"]]
        self.assertGreater(len(urls), 6)
        for url in urls:
            self.assertTrue(url.startswith("https://"), url)

    def test_license_is_mit(self):
        self.assertEqual(self.plugin["license"], "MIT")
        text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("MIT License"))
        self.assertIn("Copyright (c) 2026 Atromx Intelligence Private Limited", text)

    def test_keywords_are_few_and_kebab_case(self):
        words = self.plugin["keywords"]
        self.assertTrue(1 <= len(words) <= 15, len(words))
        self.assertEqual(len(words), len(set(words)))
        for word in words:
            self.assertRegex(word, r"^[a-z0-9]+(-[a-z0-9]+)*$")

    def test_description_leads_with_the_search_words_and_ends_with_the_maker(self):
        text = self.plugin["description"]
        self.assertLessEqual(len(text), 650, len(text))
        self.assertTrue(text.endswith(SUPPORT_TAIL), text[-80:])
        self.assertTrue(text.startswith("Meta Ads, Facebook Ads and Instagram Ads help in your AI client"), text[:60])
        self.assertIn("Direct access to your Meta ad account comes when Meta approves "
                      "AdCopilot's API access; there is no date yet.", text)
        self.assertIn("Every change is proposed first and made only on your yes.", text)

    def test_icon_is_our_own_png(self):
        icon = self.plugin["icon"]
        self.assertEqual(icon, "./.claude-plugin/icon.png")
        data = (ROOT / icon).read_bytes()
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        self.assertFalse((ROOT / ".claude-plugin" / "icon.svg").exists())


class MarketplaceJson(unittest.TestCase):

    def test_it_names_this_plugin_with_the_repo_as_its_source(self):
        market = load(".claude-plugin/marketplace.json")
        self.assertEqual(market["name"], REPO)
        self.assertEqual(market["owner"],
                         {"name": "Atromx Intelligence", "url": "https://adcopilot.cloud"})
        self.assertTrue(market["description"])
        self.assertEqual(len(market["plugins"]), 1)
        entry = market["plugins"][0]
        self.assertEqual(entry["name"], NAME)
        self.assertEqual(entry["source"], "./")
        self.assertTrue(entry["description"])
        self.assertEqual(entry["category"], "Marketing")
        # Listing fields live in plugin.json, not in a marketplace entry.
        self.assertEqual(sorted(entry), ["category", "description", "name", "source"])


class ConnectorFile(unittest.TestCase):

    def test_mcp_json_is_the_one_connector_every_adcopilot_plugin_carries(self):
        raw = (ROOT / ".mcp.json").read_text(encoding="utf-8")
        self.assertEqual(json.loads(raw), MCP)
        self.assertEqual(raw.strip(), MCP_TEXT)

    def test_nothing_in_it_launches_a_package_or_holds_a_credential(self):
        server = load(".mcp.json")["mcpServers"]["adcopilot"]
        self.assertEqual(sorted(server), ["type", "url"])
        self.assertEqual(server["type"], "http")


if __name__ == "__main__":
    unittest.main()
