from pathlib import Path
import unittest

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CODE_URL = "https://github.com/WendyBaiYunwei/PEEK"
POSTER_PATH = "assets/PEEK_NeurIPS_2026_Poster.pdf"


class ProjectPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.soup = BeautifulSoup(INDEX.read_text(encoding="utf-8"), "html.parser")

    def test_page_exposes_code_and_poster_resources(self):
        links = {link.get("href"): link.get_text(" ", strip=True) for link in self.soup.find_all("a")}

        self.assertIn(CODE_URL, links)
        self.assertIn(POSTER_PATH, links)
        self.assertRegex(links[CODE_URL].lower(), r"code|github")
        self.assertIn("poster", links[POSTER_PATH].lower())

    def test_media_assets_are_local_and_present(self):
        video = self.soup.find("video")
        self.assertIsNotNone(video)
        self.assertTrue(video.has_attr("controls"))
        self.assertTrue(video.get("aria-label", "").strip())

        video_source = video.find("source", src=True)
        self.assertEqual(video_source["src"], "PEEK.mp4")
        self.assertTrue((ROOT / video_source["src"]).is_file())

        poster_image = self.soup.find("img", src="assets/PEEK_NeurIPS_2026_Poster_preview.png")
        self.assertIsNotNone(poster_image)
        self.assertGreaterEqual(len(poster_image.get("alt", "").split()), 5)
        self.assertTrue((ROOT / poster_image["src"]).is_file())
        self.assertTrue((ROOT / POSTER_PATH).is_file())

    def test_document_has_descriptive_metadata_and_landmarks(self):
        self.assertIn("One-Step-Look-Ahead", self.soup.title.get_text())

        description = self.soup.find("meta", attrs={"name": "description"})
        self.assertIsNotNone(description)
        self.assertGreaterEqual(len(description.get("content", "")), 80)

        canonical = self.soup.find("link", rel="canonical")
        self.assertEqual(canonical["href"], "https://wendybaiyunwei.github.io/PEEK-Video/")

        for property_name in ("og:title", "og:description", "og:image"):
            self.assertIsNotNone(self.soup.find("meta", attrs={"property": property_name}))

        self.assertIsNotNone(self.soup.find("main", id="main-content"))
        for section_id in ("overview", "video", "resources"):
            self.assertIsNotNone(self.soup.find("section", id=section_id))

    def test_links_with_new_tabs_are_safely_labeled(self):
        links = self.soup.find_all("a", target="_blank")
        self.assertGreaterEqual(len(links), 2)

        for link in links:
            with self.subTest(href=link.get("href")):
                relation = set(link.get("rel", []))
                name = link.get("aria-label") or link.get_text(" ", strip=True)
                self.assertIn("noopener", relation)
                self.assertTrue(name.strip())

    def test_generic_containers_do_not_carry_aria_labels(self):
        invalid = [
            element
            for element in self.soup.find_all(["div", "span"], attrs={"aria-label": True})
            if not element.get("role")
        ]

        self.assertEqual(invalid, [])


if __name__ == "__main__":
    unittest.main()
