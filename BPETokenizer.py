from collections import defaultdict

class BPETokenizer:
	def __init__(self, text: str) -> None:
		self.raw_text: str = text
		self.vocab: dict[str, int] = {}
		self.word_freq: defaultdict[str, int] = defaultdict(int)

		self._build_word_freqs()

	def _clean_text(self, text: str) -> str:
		pass

	def _build_word_freqs(self) -> None:
		clean_text: str = self._clean_text(self.raw_text)
		words: list[str] = clean_text.split()

		for word in words:
			self.word_freq[word] += 1
