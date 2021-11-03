"""dataset module"""

from dataclasses import asdict, dataclass
import json


@dataclass
class Channel():
    """Class for channel objects"""

    channel_id: str = None
    name: str = None
    description: str = None
    picture: str = None

    def to_dict(self, filter_none=True):
        """Converts the channel object to a dictionary"""

        attribute_translations = {
            ('id', 'channel_id'),
            ('workspaceId', 'workspace_id')
        }

        channel_dict_repr = asdict(self)

        for translation in attribute_translations:
            channel_dict_repr = {translation[0] if k == translation[1]
                         else k: v for k, v in channel_dict_repr.items()}

        if filter_none:
            return {k: v for k, v in channel_dict_repr.items() if v is not None}
        return channel_dict_repr

    def to_json_str(self, filter_none=True):
        """Converts the channel object to a JSON string"""

        return json.dumps(self.to_dict(filter_none=filter_none))

    @staticmethod
    def from_dict(channels_dict):
        """Resolves a channel object from a dictionary"""

        channel = Channel()

        channel.name = channels_dict.get('name')
        channel.description = channels_dict.get('description')
        channel.picture = channels_dict.get('picture')

        return channel
