######################################################
# FILTER
######################################################

VOTE_DATE = "vote_date"
RANK = "rank"
VIEWS = "views"
REPLIES = "replies"
TAGGED = "tagged"
VOTES = "votes"
VISIT = "visit"
REPUTATION = "reputation"
JOINED = "joined"
ACTIVITY = "activity"
UPDATE = "update"
ANSWERS = "answers"
BOOKED = "bookmark"
CREATION = "creation"

# Map filter actions to respective database filters.
ORDER_MAPPER = {
    RANK: "-rank",
    UPDATE: "-lastedit_date",
    ANSWERS: "-answer_count",
    CREATION: "-creation_date",
    TAGGED: "-tagged",
    BOOKED: "-book_count",
    VIEWS: "-view_count",
    REPLIES: "-reply_count",
    VOTES: "-thread_votecount",
    VISIT: "-profile__last_login",
    REPUTATION: "-profile__score",
    JOINED: "-profile__date_joined",
    ACTIVITY: "-profile__date_joined",
    VOTE_DATE: "-votes__date",
}
