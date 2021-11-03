import re
from typing import Any, List, Mapping, Optional, Sequence

from transformers import PreTrainedTokenizer

from ..data.entity import FeatureVectors, Vector
from ..data.transform import FeatureExtractor
from .text import TextPairWithMetadataExtractor


class TransformersTokenizerVectorizer(FeatureExtractor):
    def __init__(
        self,
        text_pair_extractor: TextPairWithMetadataExtractor,
        tokenizer: PreTrainedTokenizer,
        max_length: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.text_pair_extractor = text_pair_extractor
        self.tokenizer = tokenizer
        self.padding_values = {
            "input_ids": self.tokenizer.pad_token_id,
            "token_type_ids": self.tokenizer.pad_token_type_id,
            "attention_mask": 0,
        }
        self.max_length = max_length

    def extract_features(self, instance: Mapping[str, Any]) -> FeatureVectors:
        text, secondary_text, added_tokens = self.text_pair_extractor.extract(instance=instance)
        added_tokens = list(added_tokens)
        if len(added_tokens) > 0:
            text = " ".join(added_tokens) + " " + text

        return dict(
            (key, Vector(value, self.padding_values[key]))
            for key, value in self.tokenizer.encode_plus(
                text=text,
                text_pair=secondary_text if len(secondary_text) == 0 else None,
                add_special_tokens=True,
                max_length=self.max_length,
                return_token_type_ids=True,
            ).items()
        )

    def fit(self, instances: Sequence[Mapping[str, Any]]) -> "TransformersTokenizerVectorizer":
        for instance in instances:
            _, _, added_tokens = self.text_pair_extractor.extract(instance=instance)
            added_tokens = list(added_tokens)
            if len(added_tokens) > 0:
                self.tokenizer.add_tokens(new_tokens=added_tokens, special_tokens=False)
        return self


class TransformersTokenizerHighlightVectorizer(TransformersTokenizerVectorizer):

    _MERGE_NEARBY_OBJECTS_PAT = re.compile(r"</b>([ ._\-&]?)<b>")
    _MERGE_REPLACEMENT = "\\1"

    def __init__(
        self,
        text_pair_extractor: TextPairWithMetadataExtractor,
        tokenizer: PreTrainedTokenizer,
        max_length: Optional[int] = 500,
        max_length_secondary: int = 100,
        object_highlight_token: str = "[",
        object_closing_token: str = "]",
    ) -> None:
        super().__init__(text_pair_extractor=text_pair_extractor, tokenizer=tokenizer, max_length=max_length)
        self.max_length_secondary = max_length_secondary
        self.object_highlight_token = object_highlight_token
        self.object_closing_token = object_closing_token
        if self.max_length is not None:
            self.__single_text_length = self.max_length - self.tokenizer.num_special_tokens_to_add(pair=False)
            self.__paired_text_length = (
                self.max_length - self.max_length_secondary - self.tokenizer.num_special_tokens_to_add(pair=True)
            )
        else:
            self.__single_text_length = None
            self.__paired_text_length = None

    def extract_features(self, instance: Mapping[str, Any]) -> FeatureVectors:
        text, secondary_text, added_tokens = self.text_pair_extractor.extract(instance=instance)

        text = self._preprocess(text)
        secondary_text = self._preprocess(secondary_text)

        added_tokens = list(added_tokens)
        if len(added_tokens) > 0:
            text = " ".join(added_tokens) + " " + text

        if secondary_text.strip():
            text_length = self.__paired_text_length
            tokenized_secondary_text = self.tokenizer.tokenize(text=secondary_text)
            tokenized_secondary_text = self._crop_based_on_object(tokenized_secondary_text, self.max_length_secondary)
            indexed_secondary_text = self.tokenizer.convert_tokens_to_ids(tokens=tokenized_secondary_text)
        else:
            text_length = self.__single_text_length
            indexed_secondary_text = None

        tokenized_text = self.tokenizer.tokenize(text=text)
        if text_length is not None:
            tokenized_text = self._crop_based_on_object(tokenized_text, text_length)
        indexed_text = self.tokenizer.convert_tokens_to_ids(tokens=tokenized_text)

        # fast tokenizers don't support list of ints as input
        # (https://huggingface.co/transformers/v2.9.1/main_classes/tokenizer.html#transformers.PreTrainedTokenizer.batch_encode_plus)
        if self.tokenizer.is_fast:
            indexed_text = self.tokenizer.decode(indexed_text)
            if indexed_secondary_text is not None:
                indexed_secondary_text = self.tokenizer.decode(indexed_secondary_text)

        return dict(
            (key, Vector(value, self.padding_values[key]))
            for key, value in self.tokenizer.encode_plus(
                text=indexed_text,
                text_pair=indexed_secondary_text,
                add_special_tokens=True,
                max_length=self.max_length,
                return_token_type_ids=True,
                truncation=True,
            ).items()
        )

    def _crop_based_on_object(self, tokens: List[str], max_length: int) -> List[str]:
        if self.object_highlight_token in tokens[-max_length:]:
            return tokens[-max_length:]
        return tokens[:max_length]

    def _merge_nearby_b_highlights(self, text: str) -> str:
        return self._MERGE_NEARBY_OBJECTS_PAT.sub(self._MERGE_REPLACEMENT, text)

    def _preprocess(self, text: str) -> str:
        return (
            self._merge_nearby_b_highlights(text)
            .replace("<b>", self.object_highlight_token)
            .replace("</b>", self.object_closing_token)
        )
