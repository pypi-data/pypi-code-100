from neomodel import (
    FloatProperty,
    IntegerProperty,
    Relationship,
    StringProperty,
    StructuredNode,
    StructuredRel,
    UniqueIdProperty,
    DateTimeProperty,
    BooleanProperty,
)


class Client(StructuredNode):
    client_id = StringProperty(required=True, unique_index = True)
    client_name = StringProperty(required=True)
    client_taxonomy_config = StringProperty(required=False)


class ProblemSolution(StructuredNode):
    client_id = StringProperty(required=True, index=True)
    argument_type = StringProperty(required=True, index = True)  # Problem or Solution
    pro_con_flag = StringProperty(required=True, index = True)  # Pro or Con
    process_datetime = DateTimeProperty(default_now=True)


class Topic(StructuredNode):
    client_id = StringProperty(required=True, index=True)
    text = StringProperty(required=True, index = True)
    tsne_coords = StringProperty(required=True)
    process_datetime = DateTimeProperty(default_now=True)

class TopicRel(StructuredRel):
    confidence = FloatProperty(required=False, default=1)


class SubTopic(StructuredNode):
    client_id = StringProperty(required=True, index=True)
    text = StringProperty(required=True, index = True)
    topic = Relationship(Topic, 'HAS_TOPIC', model=TopicRel)
    process_datetime = DateTimeProperty(default_now=True)

class SubTopicRel(StructuredRel):
    confidence = FloatProperty(required=False)


class Sentiment(StructuredNode):
    client_id = StringProperty(required=True, index=True)
    sentiment = IntegerProperty(required=True, index=True)
    process_datetime = DateTimeProperty(default_now=True)


class UserMood(StructuredNode):
    client_id = StringProperty(required=True, index=True)
    mood = IntegerProperty(required=True, index=True)

    
class Emoji(StructuredNode):
    client_id = StringProperty(required=True, index=True)
    label = StringProperty(required=True, index=True)
    pax_label = StringProperty(required=True)
    group = StringProperty(required=True)
    plutchik_category = StringProperty()
    process_datetime = DateTimeProperty(default_now=True)


class EmojiRel(StructuredRel):
    intensity = IntegerProperty(required=False)
    probability = FloatProperty(required=False)


class EntityType(StructuredNode):
    #client_id = StringProperty(required=True, index=True)
    text = StringProperty(required=True, unique_index = True)
    process_datetime = DateTimeProperty(default_now=True)


class Entity(StructuredNode):
    client_id = StringProperty(required=True, index=True)
    uid = UniqueIdProperty()
    client_id = StringProperty(required=True, index=True)
    name = StringProperty(required=True, index = True)
    type = Relationship(EntityType, 'OF_TYPE')
    process_datetime = DateTimeProperty(default_now=True)
    

class EntityTypeRel(StructuredRel):
    confidence = FloatProperty(required=False)


class UserDemographics(StructuredNode):
    client_id = StringProperty(required=True, index=True)
    taxonomy = StringProperty(required=True)
    value = StringProperty(required=True)
    category = StringProperty()

# With inherited classes neomodel creates multiple labels to the node 
# (i.e. the class name and each inherited class name will be a label associated to the node)
class CustomDemographic(UserDemographics):
    parent = Relationship('CustomDemographic', 'HAS_PARENT_PROPERTY')


class AgeGroup(UserDemographics):
    pass


class GenderIdentity(UserDemographics):
    pass


class Location(UserDemographics):
    category = StringProperty(default='GeoLocation')


class Ethnicity(UserDemographics):
    pass


class EducationLevel(UserDemographics):
    pass


class Occupation(UserDemographics):
    pass


class UserCommunicationRel(StructuredRel):
    number_of_comunications=IntegerProperty(default=0)
    first_comunication_date=DateTimeProperty(default_now=True)
    last_comunication_date=DateTimeProperty(default_now=True)
    

class User(StructuredNode):
    uid = StringProperty(required=True, unique_index = True)
    client_id = StringProperty(required=True, index=True)
    name = StringProperty()
    anonymous = BooleanProperty()
    process_datetime = DateTimeProperty(default_now=True)
    communicates_with = Relationship('User', 'COMMUNICATES_WITH', model=UserCommunicationRel)
    age_group = Relationship(AgeGroup, 'HAS_DEMOGRAPHIC')
    ethnicity = Relationship(Ethnicity, 'HAS_DEMOGRAPHIC')
    location = Relationship(Location, 'HAS_DEMOGRAPHIC')
    gender_identity = Relationship(GenderIdentity, 'HAS_DEMOGRAPHIC')
    custom_demographic = Relationship(CustomDemographic, 'HAS_DEMOGRAPHIC')
    #TODO need to check if there is a cleaner way
    #class_relation_map is added to be able to dynamically associate the class object name with the reltionship attribute object name in User node
    #used in write_user_demographics
    class_relation_map = {'CustomDemographic':'custom_demographic',
                'AgeGroup':'age_group',
                'GenderIdentity':'gender_identity',
                'Location':'location',
                'Ethnicity':'ethnicity',
            }
    

class UserGroup(User):
    members = Relationship(User, 'HAS_MEMBER')
    
class Comment(StructuredNode):
    uid = StringProperty(required=True, unique_index = True)
    text = StringProperty(required=True)
    client_id = StringProperty(required=True, index=True)
    forum_id = StringProperty(required=True, index=True)
    forum_text = StringProperty()
    conversation_id = StringProperty()
    conversation_text = StringProperty()
    create_datetime = DateTimeProperty(default_now=False)
    process_datetime = DateTimeProperty(default_now=True)
    number_likes = IntegerProperty(default=0)
    number_dislikes = IntegerProperty(default=0)
    number_good_rating = IntegerProperty(default=0)
    number_replies = IntegerProperty(default=0)
    avg_sentiment = Relationship(Sentiment, 'HAS_AVG_SENTIMENT')
    emoji = Relationship(Emoji, 'HAS_EMOJI', model=EmojiRel)
    topic = Relationship(Topic, 'HAS_TOPIC', model=TopicRel)
    subtopic = Relationship(SubTopic, 'HAS_SUBTOPIC', model=SubTopicRel)
    user = Relationship(User, 'POSTED_BY')
    entity = Relationship(Entity, 'HAS_ENTITY')
    user_mood = Relationship(UserMood, 'HAS_USER_MOOD')
    argument = Relationship(ProblemSolution, 'HAS_ARGUMENT')
    conversation = Relationship(ProblemSolution, 'HAS_CONVERSATION')
    parent_comment_id = StringProperty(required=False)
    parent_comment = Relationship('Comment', 'HAS_PARENT_COMMENT')

class Sentence(StructuredNode):
    uid = UniqueIdProperty()
    text = StringProperty(required=True)
    client_id = StringProperty(required=True, index=True)
    forum_id = StringProperty(required=True, index=True)
    conversation_id = StringProperty()
    process_datetime = DateTimeProperty(default_now=True)
    comment = Relationship(Comment, 'DECOMPOSES')
    sentiment = Relationship(Sentiment, 'HAS_SENTIMENT')
    emoji = Relationship(Emoji, 'HAS_EMOJI', model=EmojiRel)
    topic = Relationship(Topic, 'HAS_TOPIC', model=TopicRel)
    subtopic = Relationship(SubTopic, 'HAS_SUBTOPIC', model=SubTopicRel)


class Chunk(StructuredNode):
    uid = UniqueIdProperty()
    text = StringProperty(required=True)
    client_id = StringProperty(required=True, index=True)
    forum_id = StringProperty(required=True, index=True)
    conversation_id = StringProperty()
    process_datetime = DateTimeProperty(default_now=True)
    comment = Relationship(Comment, 'DECOMPOSES')
    sentiment = Relationship(Sentiment, 'HAS_SENTIMENT')
    emoji = Relationship(Emoji, 'HAS_EMOJI', model=EmojiRel)
    topic = Relationship(Topic, 'HAS_TOPIC', model=TopicRel)
    subtopic = Relationship(SubTopic, 'HAS_SUBTOPIC', model=SubTopicRel)
    entity = Relationship(Entity, 'HAS_ENTITY')
    argument = Relationship(ProblemSolution, 'HAS_ARGUMENT')


class Conversation(StructuredNode):
    uid = StringProperty(required=True, unique_index = True)
    client_id = StringProperty(required=True, index=True)
    forum_id = StringProperty(required=True, index=True)
    text = StringProperty(required=True)
    description = StringProperty(required=False)
    process_datetime = DateTimeProperty(default_now=True)

    
class Question(StructuredNode):
    uid = UniqueIdProperty()
    text = StringProperty(required=True)
    client_id = StringProperty(required=True, index=True)
    forum_id = StringProperty(required=True, index=True)
    conversation_id = StringProperty()
    process_datetime = DateTimeProperty(default_now=True)


class ClusterHead(StructuredNode):
    uid = UniqueIdProperty()
    text = StringProperty(required=True)
    similarity_score = FloatProperty(required=True)
    element_count = IntegerProperty()
    client_id = StringProperty(required=True, index=True)
    forum_id = StringProperty(required=True, index=True)
    conversation_id = StringProperty()
    process_datetime = DateTimeProperty(default_now=True)
    question = Relationship(Question, 'ANSWERS')


class ClusterElement(StructuredNode):
    uid = UniqueIdProperty()
    text = StringProperty(required=True)
    client_id = StringProperty(required=True, index=True)
    forum_id = StringProperty(required=True, index=True)
    conversation_id = StringProperty()
    process_datetime = DateTimeProperty(default_now=True)
    sentences = Relationship(Sentence, 'DERIVES_FROM')
    chunks = Relationship(Chunk, 'DERIVES_FROM')
    cluster_head = Relationship(ClusterHead, 'DECOMPOSES')

