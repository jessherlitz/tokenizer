from collections import defaultdict

class BPETokenizer:
	def __init__(self, text: str) -> None:
		self.raw_text: str = text
		self.vocab: dict[str, int] = {}
		self.word_freq: defaultdict[str, int] = defaultdict(int)
		self.splits: defaultdict[tuple[str, ...], int] = defaultdict(int)
		self.merges: list[tuple[str, str]] = []
		self._build_word_freqs()
		self._build_char_splits()
		self._build_initial_vocab()

	##

	def _clean_text(self, text: str) -> str:
		pass

	def _build_word_freqs(self) -> None:
		clean_text: str = self._clean_text(self.raw_text)
		words: list[str] = clean_text.split()

		for word in words:
			self.word_freq[word] += 1

	def _build_char_splits(self) -> None:
		for word, freq in self.word_freq.items():
			w: list[str] = list(word)
			w[-1] = w[-1] + '</w>'
			self.splits[tuple(w)] = freq

	def _count_pairs(self) -> dict[tuple, int]:
		pairs_count: defaultdict[tuple[str, str], int] = defaultdict(int)

		for w, freq in self.splits.items():
			for i in range(len(w) - 1):
				sub_word = (w[i], w[i + 1])
				pairs_count[sub_word] += freq

		return pairs_count

	def train(self, num_merges: int) -> None:
		for i in range(num_merges):
			pairs_count = self._count_pairs()
			if not pairs_count:
				break
			best_pair = max(pairs_count, key=pairs_count.get)
			self.merges.append(best_pair)
			self._merge(best_pair)
			self.vocab[best_pair[0] + best_pair[1]] = len(self.vocab)

	def _merge(self, pair: tuple[str, str]) -> None:
		new_splits: defaultdict[tuple[str, ...], int] = defaultdict(int)

		for entry, freq in self.splits.items():
			new_tokens: list[str] = []
			i: int = 0
			while i < len(entry):
				if i < len(entry) - 1 and entry[i] == pair[0] and entry[i + 1] == pair[1]:
					new_tokens.append(pair[0] + pair[1])
					i += 2
				else:
					new_tokens.append(entry[i])
					i += 1
			new_splits[tuple(new_tokens)] = freq
		self.splits = new_splits


	def _build_initial_vocab(self) -> None:
		token_id: int = 0
		for entry in self.splits.keys():
			for token in entry:
				if token not in self.vocab:
					self.vocab[token] = token_id
					token_id += 1


































