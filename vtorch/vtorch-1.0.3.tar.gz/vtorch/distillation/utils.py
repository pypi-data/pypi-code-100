import math
from functools import partial
from typing import Optional, Tuple

import torch
from torch import nn
from transformers import PreTrainedModel
from transformers.modeling_bert import BertSelfAttention


def forward(
    self: BertSelfAttention,
    hidden_states: torch.Tensor,
    attention_mask: Optional[torch.Tensor] = None,
    head_mask: Optional[torch.Tensor] = None,
    encoder_hidden_states: Optional[torch.Tensor] = None,
    encoder_attention_mask: Optional[torch.Tensor] = None,
) -> Tuple[torch.Tensor, ...]:
    mixed_query_layer = self.query(hidden_states)

    # If this is instantiated as a cross-attention module, the keys
    # and values come from an encoder; the attention mask needs to be
    # such that the encoder's padding tokens are not attended to.
    if encoder_hidden_states is not None:
        mixed_key_layer = self.key(encoder_hidden_states)
        mixed_value_layer = self.value(encoder_hidden_states)
        attention_mask = encoder_attention_mask
    else:
        mixed_key_layer = self.key(hidden_states)
        mixed_value_layer = self.value(hidden_states)

    query_layer = self.transpose_for_scores(mixed_query_layer)
    key_layer = self.transpose_for_scores(mixed_key_layer)
    value_layer = self.transpose_for_scores(mixed_value_layer)

    # Take the dot product between "query" and "key" to get the raw attention scores.
    attention_scores = torch.matmul(query_layer, key_layer.transpose(-1, -2))
    attention_scores = attention_scores / math.sqrt(self.attention_head_size)
    if attention_mask is not None:
        # Apply the attention mask is (precomputed for all layers in BertModel forward() function)
        attention_scores = attention_scores + attention_mask

    # Normalize the attention scores to probabilities.
    attention_probs = nn.Softmax(dim=-1)(attention_scores)

    # This is actually dropping out entire tokens to attend to, which might
    # seem a bit unusual, but is taken from the original Transformer paper.
    attention_probs = self.dropout(attention_probs)

    # Mask heads if we want to
    if head_mask is not None:
        attention_probs = attention_probs * head_mask

    context_layer = torch.matmul(attention_probs, value_layer)

    context_layer = context_layer.permute(0, 2, 1, 3).contiguous()
    new_context_layer_shape = context_layer.size()[:-2] + (self.all_head_size,)
    context_layer = context_layer.view(*new_context_layer_shape)

    outputs = (context_layer, attention_scores) if self.output_attentions else (context_layer,)
    return outputs  # type: ignore


def patch_self_attention_forward(model: PreTrainedModel) -> None:
    """
    Function to patch model's self_attention forward method to receive the `attention_scores` instead of
    `attention_probs` in the output. There is assumption that we will use BertModel architecture.
    """
    if hasattr(model, "encoder"):
        encoder = model.encoder
    else:
        raise AttributeError("The encoder can't be found in the model by 'encoder' attribute")

    if hasattr(encoder, "layer") and isinstance(encoder.layer, nn.ModuleList):
        layers = encoder.layer
    else:
        raise AttributeError("Transformer layers can't be found in the encoder by 'layer' attribute")

    if not hasattr(next(iter(layers)), "attention"):
        raise AttributeError("Attention block can't be found in transformer layers by 'attention' attribute")
    elif not hasattr(next(iter(layers)).attention, "self"):
        raise AttributeError("MultiHeadSelfAttention block can't be found in attention block by 'self' attribute")
    else:
        for layer in layers:
            layer.attention.self.forward = partial(forward, layer.attention.self)
