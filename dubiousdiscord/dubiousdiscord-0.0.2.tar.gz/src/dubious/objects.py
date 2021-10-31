
from __future__ import annotations

from dataclasses import Field, dataclass, fields
from typing import Any, Optional, Union, get_args, get_origin, get_type_hints

from dubious.enums import commandOptionTypes as cmdOptions

class Snowflake:
    def __init__(self, r: str):
        self.id = int(r)
        self.timestamp = (self.id >> 22) + 1420070400000
        self.workerID = (self.id & 0x3E0000) >> 17
        self.processID = (self.id & 0x1F000) >> 12
        self.increment = self.id & 0xFFF
    
    def __repr__(self):
        return str(self.id)
    
    def __str__(self) -> str:
        return repr(self)
    
    def __hash__(self):
        return self.id
    
    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            return False
        return o.id == self.id

def dig(typ: type):
    orig: type = get_origin(typ)
    args = get_args(typ)
    if not orig:
        return typ
    elif orig == list:
        if len(args) == 1:
            return dig(*args)
        else:
            raise TypeError(f"For type {typ}: Encountered a list with multiple type arguments.")
    elif type(None) in args:
        return dig(args[0])
    elif orig == tuple or orig == dict:
        return orig
    raise TypeError(f"For type {typ}: Encountered an unrecognized type")

def flatten(typ: type):
    if get_origin(typ):
        return flatten(get_origin(typ))
    else:
        return typ

class HasOptions:
    options: list[InteractionCommandDataOption]
    def getOptions(self, resolvedObjects: InteractionCommandDataResolved):
        collected: dict[str, Any] = {}
        if not self.options: return collected
        for option in self.options:
            if isinstance(option.value, Snowflake):
                cast = casting[option.type]
                collected[option.name] = resolvedObjects.castUsing(option.value, cast)
            elif not option.type in (cmdOptions.subCommand, cmdOptions.subCommandGroup):
                collected[option.name] = option.value
            else:
                print("subcommands suck")
        return collected

@dataclass
class Payload:
    op: int
    t: Optional[str]
    s: int
    d: dict

class DataCastingException(Exception):
    def __init__(self, dataType: str, dataField: str, exception: Exception):
        super().__init__(f"Error casting {dataType} (field {dataField}): {exception}")

@dataclass
class Data:
    @classmethod
    def new(cls, *args, **kwargs):
        fieldNames = {field.name for field in fields(cls)}
        #print(f"field names for {cls.__name__}: {fieldNames}")
        present = {k: kwargs[k] for k in kwargs if k in fieldNames}
        #ignored = {k: kwargs[k] for k in kwargs if not k in fieldNames}
        #print(f"fields ignored for {cls.__name__}: {ignored.keys()}")
        return cls(*args, **present)

    def __post_init__(self):
        #print(f"+++++ post_init for {self.__class__.__name__} started +++++\n")
        hints = get_type_hints(self.__class__)
        for field in fields(self):
            try:
                self._castField(field, hints)
            except Exception as e:
                raise DataCastingException(self.__class__.__name__, field.name, e)
        #print(f"----- post_init for {self.__class__.__name__} finished -----\n")

    def _castField(self, field: Field, hints: dict[str, Any]):
        value = self.__getattribute__(field.name)
        typeHint = hints[field.name] # the base type hint
        realType = dig(typeHint) # the actual type to make the value
        if realType == Any: return # When Any is used, the casting has to be handled with an overridden __post_init__
        cast = realType.new if issubclass(realType, Data) else realType

        if value is None: return
        #print(f"field `{field.name}`:\nhint: {typeHint}\nreal: {realType}\ndata: {value}\n")

        if typeHint == list or get_origin(typeHint) == list:
            if not isinstance(value, list):
                raise TypeError(f"Expected a list but recieved {type(value)}.")
            l: list[realType] = []
            for r in value:
                #print(f"adding to list: {r}")
                l.append(cast(**r) if isinstance(r, dict) else cast(r))
            self.__setattr__(field.name, l)
        
        elif typeHint == dict or get_origin(typeHint) == dict:
            if not isinstance(value, dict):
                raise TypeError(f"Expected a dict but recieved {type(value)}.")
            keyType, valType = get_args(typeHint)
            keyCast = dig(keyType)
            if issubclass(keyCast, Data): keyCast = keyCast.new
            valCast = dig(valType)
            if issubclass(valCast, Data): valCast = valCast.new
            d: dict[keyType, valType] = {}
            for k in value:
                r = value[k]
                d[keyCast(**k) if isinstance(k, dict) else keyCast(k)] = valCast(**r) if isinstance(r, dict) else valCast(r)
            self.__setattr__(field.name, d)

        elif not isinstance(value, realType):
            self.__setattr__(field.name, cast(**value) if isinstance(value, dict) else cast(value))

@dataclass
class HasID(Data):
    id: Snowflake

# https://discord.com/developers/docs/topics/gateway#activity-object-activity-structure
@dataclass
class Activity(Data):
    # guaranteed
    name: str
    type: int
    created_at: int

    # not guaranteed
    url: Optional[str] = None
    timestamps: ActivityTimestamps = None
    application_id: Snowflake = None
    details: Optional[str] = None
    state: Optional[str] = None
    emoji: Optional[ActivityEmoji] = None
    party: ActivityParty = None
    assets: ActivityAssets = None
    secrets: ActivitySecrets = None
    instance: bool = None
    flags: int = None
    buttons: list[ActivityButton] = None

# https://discord.com/developers/docs/topics/gateway#activity-object-activity-buttons
@dataclass
class ActivityButton(Data):
    # guaranteed
    label: str
    url: str

# https://discord.com/developers/docs/topics/gateway#activity-object-activity-assets
@dataclass
class ActivityAssets(Data):
    # not guaranteed
    large_image: str = None
    large_text: str = None
    small_image: str = None
    small_text: str = None

# https://discord.com/developers/docs/topics/gateway#activity-object-activity-emoji
@dataclass
class ActivityEmoji(Data):
    # guaranteed
    name: str

    # not guaranteed
    id: Snowflake = None
    animated: bool = None

# https://discord.com/developers/docs/topics/gateway#activity-object-activity-party
@dataclass
class ActivityParty(Data):
    # not guaranteed
    id: str = None
    size: tuple[int, int] = None

# https://discord.com/developers/docs/topics/gateway#activity-object-activity-secrets
@dataclass
class ActivitySecrets(Data):
    # not guaranteed
    join: str = None
    spectate: str = None
    match: str = None

# https://discord.com/developers/docs/topics/gateway#activity-object-activity-timestamps
@dataclass
class ActivityTimestamps(Data):
    # not guaranteed
    start: int = None
    end: int = None

# https://discord.com/developers/docs/resources/channel#allowed-mentions-object-allowed-mentions-structure
@dataclass
class AllowedMentions(Data):
    parse: list[str] # contains any or none of "roles", "users", "everyone"

    roles: list[Snowflake]
    users: list[Snowflake]
    replied_user: bool

# https://discord.com/developers/docs/resources/application#application-object-application-structure
@dataclass
class Application(HasID):
    name: str
    icon: str
    description: str
    bot_public: bool
    bot_require_code_grant: bool
    summary: str
    verify_key: str
    team: dict

    rpc_origins: Optional[list[str]] = None
    terms_of_service_url: Optional[str] = None
    privacy_policy_url: Optional[str] = None
    owner: Optional[User] = None
    guild_id: Optional[Snowflake] = None
    primary_sku_id: Optional[Snowflake] = None
    slug: Optional[str] = None
    cover_image: Optional[str] = None
    flags: int = None

# https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-structure
@dataclass
class ApplicationCommand(HasID):
    # guaranteed
    application_id: Snowflake
    name: str
    description: str
    version: Snowflake

    # not guaranteed
    guild_id: Snowflake = None
    options: list[ApplicationCommandOption] = None
    default_permission: bool = None
    default_member_permissions: int = None
    type: int = 1

# https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
@dataclass
class ApplicationCommandOption(Data):
    # guaranteed
    type: int
    name: str
    description: str

    # not guaranteed
    required: bool = None
    choices: list[ApplicationCommandOptionChoice] = None
    options: list[ApplicationCommandOption] = None

# https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-choice-structure
@dataclass
class ApplicationCommandOptionChoice(Data):
    # guaranteed
    name: str
    value: Union[str, int, float]

# https://discord.com/developers/docs/resources/channel#attachment-object-attachment-structure
@dataclass
class Attachment(HasID):
    # guaranteed
    filename: str
    size: int
    url: str
    proxy_url: str

    # not guaranteed
    content_type: str = None
    height: Optional[int] = None
    width: Optional[int] = None
    ephemeral: bool = None

# https://discord.com/developers/docs/resources/audit-log#audit-log-object-audit-log-structure
@dataclass
class AuditLog(Data):
    audit_log_entries: list[AuditLogEntry]
    integrations: list[Integration]
    threads: list[Channel]
    users: list[User]
    webhooks: list[Webhook]

# https://discord.com/developers/docs/resources/audit-log#audit-log-entry-object
@dataclass
class AuditLogEntry(HasID):
    target_id: Optional[str]
    user_id: Optional[Snowflake]
    action_type: int
    
    changes: list[AuditLogEntryChange] = None
    options: AuditLogEntryOptions = None
    reason: str = None

# https://discord.com/developers/docs/resources/audit-log#audit-log-change-object-audit-log-change-structure
@dataclass
class AuditLogEntryChange(Data):
    key: str

    new_value: Any = None
    old_value: Any = None

# https://discord.com/developers/docs/resources/audit-log#audit-log-entry-object-optional-audit-entry-info
@dataclass
class AuditLogEntryOptions(Data):
    channel_id: Snowflake = None
    count: str = None
    delete_member_days: str = None
    id: Snowflake = None
    members_removed: str = None
    message_id: Snowflake = None
    role_name: str = None

# https://discord.com/developers/docs/resources/channel#channel-object-channel-structure
@dataclass
class Channel(HasID):
    # guaranteed
    type: int
    
    # not guaranteed
    guild_id: Snowflake = None
    position: int = None
    permission_overwrites: list[Overwrite] = None
    name: str = None
    topic: Optional[str] = None
    nsfw: bool = None
    last_message_id: Optional[Snowflake] = None
    bitrate: int = None
    user_limit: int = None
    rate_limit_per_user: int = None
    recipients: list[User] = None
    icon: Optional[str] = None
    owner_id: Snowflake = None
    application_id: Snowflake = None
    parent_id: Optional[Snowflake] = None
    last_pin_timestamp: Optional[str] = None
    rtc_region: Optional[str] = None
    video_quality_mode: int = None
    message_count: int = None
    member_count: int = None
    thread_metadata: ThreadMetadata = None
    member: ThreadMember = None
    default_auto_archive_duration: int = None
    permissions: str = None

    mention: str = None
    def __post_init__(self):
        super().__post_init__()
        self.mention = f"<#{self.id}>"

# https://discord.com/developers/docs/resources/channel#channel-mention-object-channel-mention-structure
@dataclass
class ChannelMention(HasID):
    # guaranteed
    guild_id: Snowflake
    type: int
    name: str

# https://discord.com/developers/docs/topics/gateway#client-status-object
@dataclass
class ClientStatus(Data):
    # not guaranteed
    desktop: str = None
    mobile: str = None
    web: str = None

# https://discord.com/developers/docs/resources/channel#embed-object-embed-structure
@dataclass
class Embed(Data):
    # not guaranteed
    title: str = None
    type: str = None
    description: str = None
    url: str = None
    timestamp: str = None
    color: int = None
    footer: EmbedFooter = None
    image: EmbedMedia = None
    thumbnail: EmbedMedia = None
    video: EmbedMedia = None
    provider: EmbedProvider = None
    author: EmbedAuthor = None
    fields: list[EmbedField] = None

# https://discord.com/developers/docs/resources/channel#embed-object-embed-author-structure
@dataclass
class EmbedAuthor(Data):
    # not guaranteed
    name: str = None
    url: str = None
    icon_url: str = None
    proxy_icon_url: str = None

# https://discord.com/developers/docs/resources/channel#embed-object-embed-field-structure
@dataclass
class EmbedField(Data):
    # guaranteed
    name: str
    value: str

    # not guaranteed
    inline: bool = None

# https://discord.com/developers/docs/resources/channel#embed-object-embed-footer-structure
@dataclass
class EmbedFooter(Data):
    # guaranteed
    text: str

    # not guaranteed
    icon_url: str = None
    proxy_icon_url: str = None

# https://discord.com/developers/docs/resources/channel#embed-object-embed-image-structure
# https://discord.com/developers/docs/resources/channel#embed-object-embed-thumbnail-structure
# https://discord.com/developers/docs/resources/channel#embed-object-embed-video-structure
@dataclass
class EmbedMedia(Data):
    # not guaranteed
    url: str = None
    proxy_url: str = None
    height: int = None
    width: int = None

# https://discord.com/developers/docs/resources/channel#embed-object-embed-provider-structure
@dataclass
class EmbedProvider(Data):
    # not guaranteed
    name: str = None
    url: str = None

# https://discord.com/developers/docs/resources/emoji#emoji-object-emoji-structure
@dataclass
class Emoji(Data):
    id: Optional[str] = None
    name: Optional[str] = None

    roles: list[Snowflake] = None
    user: User = None
    require_colons: bool = None
    managed: bool = None
    animated: bool = None
    available: bool = None

# https://discord.com/developers/docs/resources/guild#guild-object-guild-structure
@dataclass
class Guild(HasID):
    # guaranteed
    name: str
    icon: Optional[str]
    splash: Optional[str]
    discovery_splash: Optional[str]
    owner_id: Snowflake
    afk_channel_id: Optional[Snowflake]
    afk_timeout: int
    verification_level: int
    default_message_notifications: int
    explicit_content_filter: int
    roles: list[Role]
    emojis: list[Emoji]
    features: list[str]
    mfa_level: int
    application_id: Optional[Snowflake]
    system_channel_id: Optional[Snowflake]
    system_channel_flags: int
    rules_channel_id: Optional[Snowflake]
    vanity_url_code: Optional[str]
    description: Optional[str]
    banner: Optional[str]
    premium_tier: int
    preferred_locale: str
    public_updates_channel_id: Optional[Snowflake]
    nsfw_level: int

    # guaranteed in GUILD_CREATE
    widget_enabled: bool = None
    widget_channel_id: Optional[Snowflake] = None
    joined_at: str = None
    large: bool = None
    unavailable: bool = None
    member_count: int = None
    voice_states: list[VoiceState] = None
    members: list[Member] = None
    channels: list[Channel] = None
    presences: list[PresenceUpdate] = None
    stage_instances: list[StageInstance] = None
    
    application_command_counts: dict[int, int] = None
    premium_progress_bar_enabled: bool = None
    guild_hashes: GuildHashes = None
    guild_scheduled_events: list = None
    embedded_activities: list = None
    application_command_count: int = None
    lazy: bool = None
    threads: list[Channel] = None
    nsfw: bool = None
    stickers: list = None

    # not guaranteed
    icon_hash: Optional[str] = None
    region: Optional[str] = None
    max_presences: Optional[int] = None
    max_members: int = None
    premium_subscription_count: int = None
    max_video_channel_users: int = None
    approximate_member_count: int = None
    approximate_presence_count: int = None
    welcome_screen: WelcomeScreen = None

@dataclass
class GuildHash(Data):
    omitted: bool
    hash: str

@dataclass
class GuildHashes(Data):
    version: int
    roles: GuildHash
    metadata: GuildHash
    channels: GuildHash

# https://discord.com/developers/docs/topics/gateway#hello-hello-structure
@dataclass
class Hello(Data):
    heartbeat_interval: int

# https://discord.com/developers/docs/resources/guild#integration-object-integration-structure
@dataclass
class Integration(HasID):
    name: str
    type: str
    enabled: bool

    syncing: bool = None
    role_id: Snowflake = None
    enable_emoticons: bool = None
    expire_behavior: int = None
    expire_grace_period: int = None
    user: User = None
    account: IntegrationAccount = None
    synced_at: str = None
    subscriber_count: int = None
    revoked: bool = None
    application: IntegrationApplication = None

# https://discord.com/developers/docs/resources/guild#integration-account-object-integration-account-structure
@dataclass
class IntegrationAccount(HasID):
    name: str

# https://discord.com/developers/docs/resources/guild#integration-application-object-integration-application-structure
@dataclass
class IntegrationApplication(HasID):
    name: str
    icon: Optional[str]
    description: str
    summary: str

    bot: User = None

# https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-structure
@dataclass
class Interaction(HasID):
    # guaranteed
    application_id: Snowflake
    type: int
    token: str
    version: int

    # not guaranteed
    data: InteractionData = None
    guild_id: Snowflake = None
    channel_id: Snowflake = None
    member: Member = None
    user: User = None
    message: Message = None

# https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-data-structure
@dataclass
class InteractionData(Data, HasOptions):
    # guaranteed for application command
    id: Snowflake = None
    name: str = None
    type: int = None

    
    # not guaranteed for application command
    resolved: InteractionCommandDataResolved = None
    options: list[InteractionCommandDataOption] = None

    # not guaranteed for component
    custom_id: str = None
    component_type: int = None
    values: list[SelectOption] = None
    target_id: Snowflake = None

# https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-interaction-data-option-structure
@dataclass
class InteractionCommandDataOption(Data, HasOptions):
    # guaranteed
    name: str
    type: int

    # not guaranteed
    value: Any = None
    options: list[InteractionCommandDataOption] = None
    
    def __post_init__(self):
        super().__post_init__()

        if self.type in casting:
            cast = casting[self.type]
            if issubclass(cast, Data):
                self.value = Snowflake(self.value)
            else:
                self.value = cast(self.value)

# https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-resolved-data-structure
@dataclass
class InteractionCommandDataResolved(Data):
    # not guaranteed
    users: dict[Snowflake, User] = None
    members: dict[Snowflake, Member] = None
    roles: dict[Snowflake, Role] = None
    channels: dict[Snowflake, Channel] = None

    def __post_init__(self):
        super().__post_init__()

    def castUsing(self, thingID: Snowflake, cast: type[Data]):
        if issubclass(cast, User) and thingID in self.users: return self.users.get(thingID)
        if issubclass(cast, User) and thingID in self.members: return self.members.get(thingID).user
        if issubclass(cast, Member): return self.members.get(thingID)
        if issubclass(cast, Role): return self.roles.get(thingID)
        if issubclass(cast, Channel): return self.channels.get(thingID)

# https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-interaction-response-structure
@dataclass
class InteractionResponse(Data):
    type: int

    data: InteractionResponseData = None

# https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-interaction-callback-data-structure
@dataclass
class InteractionResponseData(Data):
    tts: bool
    content: str
    embeds: list[Embed]
    allowed_mentions: AllowedMentions
    flags: int
    components: list[MessageComponent]

# https://discord.com/developers/docs/resources/guild#guild-member-object-guild-member-structure
@dataclass
class Member(Data):
    roles: list[Snowflake]
    joined_at: str

    deaf: bool = None
    mute: bool = None
    user: User = None
    nick: Optional[str] = None
    premium_since: str = None
    pending: bool = None
    is_pending: bool = None
    permissions: str = None
    hoisted_role: Role = None
    avatar: str = None

# https://discord.com/developers/docs/resources/channel#message-object-message-structure
@dataclass
class Message(HasID):
    # guaranteed
    channel_id: Snowflake
    author: User
    content: str
    timestamp: str
    edited_timestamp: str
    tts: bool
    mention_everyone: bool
    mentions: list[User]
    mention_roles: list[Role]
    attachments: list[Attachment]
    embeds: list[Embed]
    pinned: bool
    type: int

    # not guaranteed
    guild_id: Snowflake = None
    member: Member = None
    mention_channels: list[ChannelMention] = None
    reactions: list[Reaction] = None
    webhook_id: Snowflake = None
    activity: MessageActivity = None
    application: Application = None
    application_id: Snowflake = None
    message_reference: MessageReference = None
    flags: int = None
    stickers: list[Sticker] = None
    referenced_message: Optional[Message] = None
    interaction: MessageInteraction = None
    thread: Channel = None
    components: list[MessageComponent] = None

# https://discord.com/developers/docs/resources/channel#message-object-message-activity-structure
@dataclass
class MessageActivity(Data):
    # guaranteed
    type: int

    # not guaranteed
    party_id: str = None

# https://discord.com/developers/docs/interactions/message-components#component-object-component-structure
@dataclass
class MessageComponent(Data):
    # guaranteed
    type: int

    # not guaranteed
    style: int = None
    label: str = None
    emoji: Emoji = None
    custom_id: str = None
    url: str = None
    options: list[SelectOption] = None
    disabled: bool = None
    placeholder: str = None
    min_values: int = None
    max_values: int = None
    
    components: list[MessageComponent] = None

# https://discord.com/developers/docs/interactions/receiving-and-responding#message-interaction-object-message-interaction-structure
@dataclass
class MessageInteraction(HasID):
    type: int
    name: str
    user: User

# https://discord.com/developers/docs/resources/channel#message-reference-object-message-reference-structure
@dataclass
class MessageReference(Data):
    # not guaranteed
    message_id: Snowflake = None
    channel_id: Snowflake = None
    guild_id: Snowflake = None
    fail_if_not_exists: bool = None

# https://discord.com/developers/docs/resources/channel#overwrite-object
@dataclass
class Overwrite(HasID):
    type: int
    allow: str
    deny: str

# https://discord.com/developers/docs/topics/gateway#ready
@dataclass
class PartialApplication(HasID):
    flags: int

# https://discord.com/developers/docs/topics/gateway#presence-update-presence-update-event-fields
@dataclass
class PresenceUpdate(Data):
    # guaranteed
    user: User
    guild_id: Snowflake
    status: str
    activities: list[Activity]
    client_status: ClientStatus

# https://discord.com/developers/docs/resources/channel#reaction-object-reaction-structure
@dataclass
class Reaction(Data):
    # guaranteed
    count: int
    me: bool
    emoji: Emoji

# https://discord.com/developers/docs/topics/gateway#ready
@dataclass
class Ready(Data):
    v: int
    user: User
    guilds: list[UnavailableGuild]
    session_id: str
    application: PartialApplication

    #user_settings: dict
    #relationships: list
    #private_channels: list
    #presences: dict
    #guild_join_requests: list
    #geo_ordered_rtc_regions: list
    #_trace: list[str]

    #shard: Optional[tuple[int, int]]=None

# https://discord.com/developers/docs/topics/permissions#role-object-role-structure
@dataclass
class Role(HasID):
    name: str
    color: int
    hoist: bool
    position: int
    permissions: str
    managed: bool
    mentionable: bool

    tags: RoleTags = None
    unicode_emoji: Optional[str] = None
    icon: Optional[Emoji] = None

# https://discord.com/developers/docs/topics/permissions#role-object-role-tags-structure
@dataclass
class RoleTags(Data):
    bot_id: Snowflake
    integration_id: Snowflake = None
    premium_subscriber: bool = None

# https://discord.com/developers/docs/interactions/message-components#select-menu-object-select-option-structure
@dataclass
class SelectOption(Data):
    # guaranteed
    label: str
    value: str

    # not guaranteed
    description: str = None
    emoji: Emoji = None
    default: bool = None

# https://discord.com/developers/docs/resources/stage-instance#stage-instance-object-stage-instance-structure
@dataclass
class StageInstance(HasID):
    # guaranteed
    guild_id: Snowflake
    channel_id: Snowflake
    topic: str
    privacy_level: int
    discoverable_disabled: bool

# https://discord.com/developers/docs/resources/sticker#sticker-object-sticker-structure
@dataclass
class Sticker(HasID):
    # guaranteed
    name: str
    description: str
    tags: str
    format_type: int

    # not guaranteed
    pack_id: Snowflake = None
    available: bool = None
    guild_id: Snowflake = None
    user: User = None
    sort_value: int = None

# https://discord.com/developers/docs/resources/channel#thread-member-object-thread-member-structure
@dataclass
class ThreadMember(Data):
    # guaranteed
    join_timestamp: str
    flags: int

    # not guaranteed
    id: Snowflake = None
    user_id: Snowflake = None

# https://discord.com/developers/docs/resources/channel#thread-metadata-object-thread-metadata-structure
@dataclass
class ThreadMetadata(Data):
    # guaranteed
    archived: bool
    auto_archive_duration: int
    archive_timestamp: str

    # not guaranteed
    locked: bool = None

# https://discord.com/developers/docs/resources/guild#unavailable-guild-object
@dataclass
class UnavailableGuild(HasID):
    unavailable: bool = None

# https://discord.com/developers/docs/resources/user#user-object-user-structure
@dataclass
class User(HasID):
    username: str
    discriminator: str

    avatar: Optional[str] = None
    bot: bool = None
    system: bool = None
    mfa_enabled: bool = None
    locale: str = None
    verified: bool = None
    email: Optional[str] = None
    flags: int = None
    premium_type: int = None
    public_flags: int = None

    mention: str = None
    def __post_init__(self):
        super().__post_init__()
        self.mention = f"<@{self.id}>"

# https://discord.com/developers/docs/resources/voice#voice-state-object-voice-state-structure
@dataclass
class VoiceState(Data):
    channel_id: Optional[Snowflake]
    user_id: Snowflake
    session_id: str
    deaf: bool
    mute: bool
    self_deaf: bool
    self_mute: bool
    suppress: bool
    request_to_speak_timestamp: str

    guild_id: Snowflake = None
    member: Member = None
    self_stream: bool = None
    self_video: bool = None

# https://discord.com/developers/docs/resources/webhook#webhook-object-webhook-structure
@dataclass
class Webhook(HasID):
    type: int
    channel_id: Optional[Snowflake]
    name: Optional[str]
    avatar: Optional[str]
    application_id: Optional[Snowflake]

    guild_id: Optional[Snowflake] = None
    user: User = None
    token: str = None
    source_guild: Guild = None
    source_channel: Channel = None
    url: str = None

# https://discord.com/developers/docs/resources/guild#welcome-screen-object-welcome-screen-structure
@dataclass
class WelcomeScreen(Data):
    description: Optional[str]
    welcome_channels: list[WelcomeScreenChannel]

# https://discord.com/developers/docs/resources/guild#welcome-screen-object-welcome-screen-channel-structure
@dataclass
class WelcomeScreenChannel(Data):
    channel_id: Snowflake
    description: str
    emoji_id: Optional[Snowflake]
    emoji_name: Optional[Snowflake]

casting = {
    cmdOptions.string: str,
    cmdOptions.integer: int,
    cmdOptions.boolean: bool,
    cmdOptions.user: User,
    cmdOptions.channel: Channel,
    cmdOptions.role: Role,
    cmdOptions.number: float,
}
backcasting = {casting[option]: option for option in casting}