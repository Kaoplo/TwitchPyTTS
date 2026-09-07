import unittest

from src.tts.voice_models import voice_paths, voice_download_urls


class VoiceModelsTests(unittest.TestCase):
    def test_voice_paths(self):
        onnx_path, json_path = voice_paths("en_US-lessac-medium", "voices")
        self.assertEqual(onnx_path, "voices/en_US-lessac-medium.onnx")
        self.assertEqual(json_path, "voices/en_US-lessac-medium.onnx.json")

    def test_voice_download_urls(self):
        onnx_url, json_url = voice_download_urls("en_US-lessac-medium")
        self.assertEqual(
            onnx_url,
            "https://huggingface.co/rhasspy/piper-voices/resolve/main/"
            "en/en_US/lessac/medium/en_US-lessac-medium.onnx",
        )
        self.assertEqual(json_url, onnx_url + ".json")

    def test_voice_download_urls_different_locale(self):
        onnx_url, _ = voice_download_urls("de_DE-thorsten-low")
        self.assertEqual(
            onnx_url,
            "https://huggingface.co/rhasspy/piper-voices/resolve/main/"
            "de/de_DE/thorsten/low/de_DE-thorsten-low.onnx",
        )


if __name__ == "__main__":
    unittest.main()
