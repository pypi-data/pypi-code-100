import re
from collections import deque
from typing import Any, Iterable, List, Mapping, Optional, Sequence, Tuple

from transformers import PreTrainedTokenizer

from vtorch.data.entity import FeatureVectors, Vector
from vtorch.huggingface.text import TextPairWithMetadataExtractor
from vtorch.huggingface.transform import TransformersTokenizerVectorizer
from vtorch.youscan.text import YSMentionCategoricalMetaExtractor


class CutTextTransformersTokenizerVectorizer(TransformersTokenizerVectorizer):
    def __init__(
        self,
        text_pair_extractor: TextPairWithMetadataExtractor,
        tokenizer: PreTrainedTokenizer,
        highlight_regex: str,
        max_length: Optional[int] = None,
    ) -> None:
        super().__init__(text_pair_extractor=text_pair_extractor, tokenizer=tokenizer, max_length=max_length)
        self.highlight_pattern = re.compile(highlight_regex)

    def extract_features(self, instance: Mapping[str, Any]) -> FeatureVectors:
        text, _, _ = self.text_pair_extractor.extract(instance=instance)
        input_ids = self._keep_highlighted_in_window(text)
        attention_mask = [1] * len(input_ids)
        token_type_ids = [1] * len(input_ids)

        return {
            "input_ids": Vector(input_ids, self.padding_values["input_ids"]),
            "token_type_ids": Vector(token_type_ids, self.padding_values["token_type_ids"]),
            "attention_mask": Vector(attention_mask, self.padding_values["attention_mask"]),
        }

    def _keep_highlighted_in_window(self, text: str, build_with_special: bool = True) -> List[int]:
        _input_ids: List[int] = self.tokenizer.convert_tokens_to_ids(self.tokenizer.tokenize(text))
        input_ids = self.tokenizer.build_inputs_with_special_tokens(_input_ids)
        num_additional_tokens = len(input_ids) - len(_input_ids)

        if self.max_length is None:
            raise ValueError(
                "set self.max_length with initialization. This class can't be used with self.max_length = None"
            )

        if len(input_ids) > self.max_length:  # type: ignore
            search = self.highlight_pattern.search(text)
            if search is not None:
                start_id, end_id = search.span()
                left, highlight, right = text[:start_id], text[start_id:end_id], text[end_id:]
                tokenized_highlight = self.tokenizer.tokenize(highlight)
                tokenized_left_right = self.tokenizer.tokenize(left), deque(self.tokenizer.tokenize(right))

                final_tokens = deque(tokenized_highlight)
                for i, tokens in enumerate(tokenized_left_right):
                    enough_tokens = len(final_tokens) + num_additional_tokens >= self.max_length  # type: ignore
                    if enough_tokens or not any(tokenized_left_right):
                        break
                    if i % 2 and tokens:
                        final_tokens.append(tokens.popleft())  # tokens: right
                    elif tokens:
                        final_tokens.appendleft(tokens.pop())  # tokens: left

                _input_ids = self.tokenizer.convert_tokens_to_ids(list(final_tokens))

            _input_ids = _input_ids[: self.max_length - num_additional_tokens]  # type: ignore
            input_ids = self.tokenizer.build_inputs_with_special_tokens(_input_ids)

        return input_ids if build_with_special else _input_ids  # type: ignore

    def fit(self, instances: Sequence[Mapping[str, Any]]) -> "TransformersTokenizerVectorizer":
        return self


class CutPairTextTransformersTokenizerVectorizer(CutTextTransformersTokenizerVectorizer):
    def __init__(
        self,
        text_pair_extractor: TextPairWithMetadataExtractor,
        tokenizer: PreTrainedTokenizer,
        highlight_regex: str,
        max_length_secondary: int,
        max_length: Optional[int] = None,
    ) -> None:
        super().__init__(
            text_pair_extractor=text_pair_extractor,
            tokenizer=tokenizer,
            highlight_regex=highlight_regex,
            max_length=max_length,
        )
        self.max_length_secondary = max_length_secondary

    def extract_features(self, instance: Mapping[str, Any]) -> FeatureVectors:
        text, secondary_text, _ = self.text_pair_extractor.extract(instance=instance)
        if not secondary_text:
            input_ids = self._keep_highlighted_in_window(text)
        else:
            _input_ids = self._keep_highlighted_in_window(text, build_with_special=False)
            secondary_ids = self.tokenizer.convert_tokens_to_ids(self.tokenizer.tokenize(secondary_text))[
                : self.max_length_secondary - 1
            ]  # -1 for cls token
            input_ids = self.tokenizer.build_inputs_with_special_tokens(secondary_ids, _input_ids)

        attention_mask = [1] * len(input_ids)

        return {
            "input_ids": Vector(input_ids, self.padding_values["input_ids"]),
            "attention_mask": Vector(attention_mask, self.padding_values["attention_mask"]),
        }


class YSMentionMetaAsTokensVectorizer(TransformersTokenizerVectorizer):

    _MERGE_NEARBY_OBJECTS_PAT = re.compile(r"</b>([ ._\-&]?)<b>")
    _MERGE_REPLACEMENT = "\\1"

    def __init__(
        self,
        text_pair_extractor: YSMentionCategoricalMetaExtractor,
        tokenizer: PreTrainedTokenizer,
        max_length: Optional[int] = None,
        max_length_secondary: Optional[int] = None,
        author_type_feature: bool = False,
        channel_type_feature: bool = False,
        object_start_token: str = "[",
        object_end_token: str = "]",
        text_tokens_type_id: int = 1,
        title_tokens_type_id: int = 0,
    ) -> None:
        super().__init__(text_pair_extractor, tokenizer, max_length)
        self.author_type_feature = author_type_feature
        self.channel_type_feature = channel_type_feature
        self.object_start_token = object_start_token
        self.object_end_token = object_end_token
        self.max_length_secondary = max_length_secondary
        self.text_tokens_type_id = text_tokens_type_id
        self.title_tokens_type_id = title_tokens_type_id

    def extract_features(self, instance: Mapping[str, Any]) -> FeatureVectors:
        features = self.text_pair_extractor.extract(instance=instance)
        text, title = self._process_features(features)
        input_ids, token_type_ids, attention_mask = self._convert_string_to_ids(text=text, title=title)

        return {
            "input_ids": Vector(input_ids, self.padding_values["input_ids"]),
            "token_type_ids": Vector(token_type_ids, self.padding_values["token_type_ids"]),
            "attention_mask": Vector(attention_mask, self.padding_values["attention_mask"]),
        }

    def fit(self, instances: Sequence[Mapping[str, Any]]) -> "TransformersTokenizerVectorizer":
        for instance in instances:
            _, _, added_tokens = self.text_pair_extractor.extract(instance=instance)

            special_tokens = self._form_special_tokens_list(list(added_tokens))

            if special_tokens:
                self.tokenizer.add_tokens(new_tokens=special_tokens, special_tokens=False)
        return self

    def _form_special_tokens_list(self, added_tokens: List[str]) -> List[str]:

        post_type, resource_type, author_type, channel_type, has_image_url_tag = added_tokens

        post_type_token: str = self._to_special_token(post_type)
        resource_type_token: str = self._to_special_token(resource_type)
        special_tokens = [post_type_token, resource_type_token]

        if self.author_type_feature:
            special_tokens.append(self._to_special_token(author_type))
        if self.channel_type_feature:
            special_tokens.append(self._to_special_token(channel_type))

        if has_image_url_tag:
            special_tokens.append(self._to_special_token(has_image_url_tag))

        return special_tokens

    def _process_features(self, features: Tuple[str, str, Iterable[str]]) -> Tuple[str, str]:

        text, title, (post_type, resource_type, author_type, channel_type, has_image_url_tag) = features

        text = self._merge_nearby_b_highlights(text)
        title = self._merge_nearby_b_highlights(title) if "comment" in post_type.lower() else ""

        special_tokens = self._form_special_tokens_list(
            [post_type, resource_type, author_type, channel_type, has_image_url_tag]
        )

        text = f"{' '.join(special_tokens)} {text}"

        text = self._preprocess(text)
        title = self._preprocess(title)

        return text, title

    def _convert_string_to_ids(self, text: str, title: str) -> Tuple[List[int], List[int], List[int]]:

        pair = bool(text and title)

        if self.max_length is None:
            raise ValueError(
                "set self.max_length with initialization. This class can't be used with self.max_length = None"
            )

        text_tokens = self.tokenizer.tokenize(text) if text else []
        title_tokens = self.tokenizer.tokenize(title) if title else []

        sequence_length = len(text_tokens) + len(title_tokens) + self.tokenizer.num_special_tokens_to_add(pair=pair)
        corrected_max_padding_length_for_secondary_text = (
            sequence_length if self.max_length > sequence_length else self.max_length_secondary  # type: ignore
        )
        title_tokens = self._crop_based_on_object(title_tokens, corrected_max_padding_length_for_secondary_text)
        text_tokens = self._crop_based_on_object(
            text_tokens,
            self.max_length - len(title_tokens) - self.tokenizer.num_special_tokens_to_add(pair=pair),  # type: ignore
        )

        title_ids = self.tokenizer.convert_tokens_to_ids(title_tokens) if title_tokens else []
        text_ids = self.tokenizer.convert_tokens_to_ids(text_tokens) if text_tokens else []

        _input_ids = [ids for ids in [text_ids, title_ids] if ids]
        input_ids = self.tokenizer.build_inputs_with_special_tokens(*_input_ids)

        token_type_ids = [self.text_tokens_type_id] * len(text_tokens) + [self.title_tokens_type_id] * (
            len(input_ids) - len(text_tokens)
        )

        attention_mask = [1] * len(input_ids)

        return input_ids, token_type_ids, attention_mask

    def _crop_based_on_object(self, tokens: List[str], max_length: int) -> List[str]:
        if self.object_start_token in tokens[-max_length:]:
            return tokens[-max_length:]
        return tokens[:max_length]

    def _merge_nearby_b_highlights(self, text: str) -> str:
        return self._MERGE_NEARBY_OBJECTS_PAT.sub(self._MERGE_REPLACEMENT, text)

    def _preprocess(self, text: str) -> str:
        return text.replace("<b>", self.object_start_token).replace("</b>", self.object_end_token)

    @staticmethod
    def _to_special_token(token: str) -> str:
        return f"[{token}]"
