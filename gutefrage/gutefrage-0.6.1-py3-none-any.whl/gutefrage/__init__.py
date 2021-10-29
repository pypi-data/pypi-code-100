import requests 
import json
from bs4 import BeautifulSoup


class gutefrage:

  def __init__(self, user, pwd):
      self.gutefrageusername = user
      self.gutefragepasswort = pwd
      self.subrefferer = ""
      self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36", "X-Client-Id":"net.gutefrage.nmms.desktop", "x-api-key":"dfdza43a-8560-4641-b316-ff928232734c","Origin":"https://www.gutefrage.net", "Referer":"https://www.gutefrage.net/"+self.subrefferer,"Sec-Fetch-Site":"same-origin","Content-Type":"application/json"}
      myobj = {"query":"\n        \n    mutation LoginWithUsernameOrEmail($emailOrUsername: String!, $password: String!) {\n      loginWithUsernameOrEmail(emailOrUsername: $emailOrUsername, password: $password) {\n        accessToken\n        refreshToken\n      }\n    }\n  \n\n        \n      ","variables":{"emailOrUsername":self.gutefrageusername,"password": self.gutefragepasswort}}
      req = requests.post("https://www.gutefrage.net/graphql", headers=self.headers, json=myobj)
      try:
          tokens = json.loads(req.text)
          self.accessToken = tokens["data"]["loginWithUsernameOrEmail"]["accessToken"]
          self.refreshToken = tokens["data"]["loginWithUsernameOrEmail"]["refreshToken"]
          self.user = self.gutefrageusername
          del self.gutefragepasswort
          del self.gutefrageusername
          del user
          del self.user
      except:
          tokens = req.text
          raise Exception("\033[31m\033[1mError: "+tokens)
  # def post(self):
  #     self.subrefferer = "frage_hinzufuegen"
  #     req = requests.post("https://www.gutefrage.net/graphql", headers=self.headers, cookies = {"gfAccessToken":self.accessToken,"gfRefreshToken":self.refreshToken})
  #     print(req.text)
  #May come back later. Post via the API

  def convert_to_id(self, url):
      self.subrefferer = "mitteilungen"
      req = requests.get("https://www.gutefrage.net/frage/"+url, headers = self.headers)
      if req.status_code == 200:
        content = req.content
        bsdoc = BeautifulSoup(content, 'html.parser')
        return int(bsdoc.find("article")['id'].replace("Question-",""))
      else:
        print("Error: "+str(req.status_code))

  def convert_to_stripped(self, id):
    self.id = id
    self.subrefferer = "nmms-api/questions/"
    req = requests.get('https://www.gutefrage.net/nmms-api/questions/'+str(self.id), headers = self.headers)
    jsontext = json.loads(req.text)
    self.id = self.id
    self.url = jsontext["stripped_title"]
    return self.url

  def comment(self, comment_id):
    return self._comment(comment_id, self.accessToken, self.refreshToken)




  class _comment:
      def __init__(self, comment_id, accessToken, refreshToken):
        self.accessToken = accessToken
        self.refreshToken = refreshToken
        self.comment_id = comment_id
        self.subrefferer = ""
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36", "X-Client-Id":"net.gutefrage.nmms.desktop", "x-api-key":"dfdza43a-8560-4641-b316-ff928232734c","Origin":"https://www.gutefrage.net", "Referer":"https://www.gutefrage.net/"+self.subrefferer,"Sec-Fetch-Site":"same-origin","Content-Type":"application/json"}

      def info(self, *args):
          self.subrefferer = "nmms-api/answers/"
          req = requests.get('https://www.gutefrage.net/nmms-api/answers/'+str(self.comment_id), headers = self.headers)
          jsontext = json.loads(req.text)
          if len(args) == 0:
            return jsontext
          else:
            for arg in args:
              return jsontext[arg]



  def question(self, id):
    return self._question(id, self.accessToken, self.refreshToken)
  
  class _question:
      def __init__(self, id, accessToken, refreshToken):
        self.accessToken = accessToken
        self.refreshToken = refreshToken
        self.id = id
        self.subrefferer = ""
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36", "X-Client-Id":"net.gutefrage.nmms.desktop", "x-api-key":"dfdza43a-8560-4641-b316-ff928232734c","Origin":"https://www.gutefrage.net", "Referer":"https://www.gutefrage.net/"+self.subrefferer,"Sec-Fetch-Site":"same-origin","Content-Type":"application/json"}
        self.like = self._like()

      def convert_to_stripped(self, id):
        self.id = id
        self.subrefferer = "nmms-api/questions/"
        req = requests.get('https://www.gutefrage.net/nmms-api/questions/'+str(self.id), headers = self.headers)
        jsontext = json.loads(req.text)
        self.id = self.id
        self.url = jsontext["stripped_title"]
        return self.url
        
      def reply(self,msg):
        self.subrefferer = "frage"
        myobj = {"query":"\n        \n    mutation CreateAnswer($answer: NewAnswer!) {\n      answer {\n        createAnswer: createAnswer(answer: $answer) {\n          id\n        }\n      }\n    }\n  \n\n        \n      ","variables":{"answer":{"questionId":self.id,"body":"<p>"+msg+"</p>","images":[]}}}
        cookies = {'gfAccessToken': self.accessToken, 'gfRefreshToken':self.refreshToken, 'gf-li':'1'}
        req2 = requests.post("https://www.gutefrage.net/graphql", headers = self.headers, cookies = cookies, json = myobj)
        if req2.status_code == 200:
          return req2.text
        else:
          print(req2.status_code)
          print(req2.text)

      def detailed_info(self):
        self.subrefferer = "frage"
        slug = self.convert_to_stripped(self.id)
        myobj = {"query":"\n        \n    query QdpLoggedIn($slug: String!, $includeQuestionAuthorStatistics: Boolean!) {\n      questionBySlug(questionSlug: $slug) {\n        ...StandardQdp\n      }\n    }\n  \n\n        \n    fragment StandardQdp on Question {\n      id\n      title\n      htmlBody\n      slug\n      self {\n        hasUpvotedQuestion\n        hasBookmarkedQuestion\n        isFollowingQuestion\n        canVerifyAnswer\n        editCapabilities\n        canHideQuestionTag\n      }\n      author {\n        ...Author\n        ...AuthorAvatar\n        ...ScoreLevel\n        statistics @include(if: $includeQuestionAuthorStatistics) {\n          questionCounts {\n            totalCount\n          }\n        }\n      }\n      adultContent {\n        ads {\n          hasReportedContentViolation\n        }\n      }\n      marketingChannel {\n        channel\n        subchannel\n      }\n      questionTags {\n        ...QuestionTag\n      }\n      createdAt\n      stats {\n        impressions {\n          total\n        }\n      }\n      answers {\n        ...Answer\n      }\n      images {\n        ...ContentImage\n      }\n      supportHint\n      poll {\n        ...QuestionPoll\n      }\n      status\n      upvotes\n      followerCount\n      mostHelpfulAnswerStatus\n      isResubmissionBlocked\n      resubmissionCount\n      latestSubmission {\n        isResubmission\n        datetime\n        user {\n          id\n          nickname\n          displayedName\n          ...AuthorAvatar\n        }\n      }\n      activities {\n        activityId\n        activity\n        expiresAt\n      }\n      latestActivityAt\n      recommendedQuestions {\n        question {\n          id\n          title\n          slug\n          htmlBody\n          createdAt\n          answerCount\n          author {\n            nickname\n            displayedName\n            ...AuthorAvatar\n          }\n        }\n        poolName\n      }\n      recommendedQuestionsForContentAuthors: recommendedQuestionsForContentAuthors {\n        question {\n          id\n          title\n          slug\n          htmlBody\n          createdAt\n          answerCount\n          author {\n            nickname\n            displayedName\n            ...AuthorAvatar\n          }\n        }\n        poolName\n      }\n      clarifications {\n        ...QuestionClarification\n      }\n      comments {\n        ...QuestionComment\n      }\n      blickwechsel {\n        userId\n        ...BlickwechselEvent\n      }\n      category {\n        category {\n          id\n          name\n          slug\n          description\n        }\n        parentCategories {\n          name\n          slug\n        }\n      }\n      reactions {\n        ...Reaction\n      }\n    }\n  ,\n    fragment Author on User {\n      id\n      displayedName\n      nickname\n      createdAt\n      roles\n      expertProfile {\n        qualification\n        reason\n        tags {\n          name\n        }\n      }\n      ...ScoreLevel\n      onlineStatus\n    }\n  ,\n    fragment AuthorAvatar on User {\n      avatar {\n        ...Avatar\n      }\n    }\n  ,\n    fragment ScoreLevel on User {\n      scoreLevel {\n        level\n        levelGroup\n        progress {\n          percent\n          score\n          scoreLevelStart\n          scoreNextLevel\n        }\n      }\n    }\n  ,\n    fragment ContentImage on Image {\n      id\n      urls {\n        big\n        full\n      }\n      webpUrls {\n        big\n        full\n      }\n      description\n    }\n  ,\n    fragment Answer on Answer {\n      __typename\n      id\n      questionId\n      createdAt\n      stats {\n        impressions {\n          total\n        }\n      }\n      htmlBody\n      author {\n        ...Author\n        ...AuthorAvatar\n        ...ScoreLevel\n        userExpertises {\n          expertiseType\n          description\n          tags {\n            name\n          }\n        }\n      }\n      expertVerifications {\n        ...ExpertVerification\n      }\n      isMostHelpful\n      comments {\n        ...Comment\n      }\n      images {\n        ...ContentImage\n      }\n      pollVote {\n        choiceId\n        text\n      }\n      userSatisfaction {\n        counts {\n          positive\n        }\n        self\n      }\n      appreciation {\n        totalCount\n        self {\n          isAllowed\n          hasAlreadyAppreciated\n        }\n      }\n      video {\n        externalUrl\n      }\n      expertise\n      latestVersion {\n        createdAt\n        version\n      }\n      status\n      isDeleted\n      reactions {\n        ...Reaction\n      }\n    }\n  ,\n    fragment QuestionComment on QuestionComment {\n      id\n      body\n      createdAt\n      author {\n        nickname\n        displayedName\n        roles\n        ...AuthorAvatar\n        ...ScoreLevel\n      }\n      reply {\n        ...QuestionCommentReply\n      }\n    }\n  ,\n    fragment QuestionClarification on QuestionClarification {\n      id\n      body\n      createdAt\n      author {\n        slug\n      }\n      images {\n        ...ContentImage\n      }\n    }\n  ,\n    fragment QuestionPoll on Poll {\n      choices {\n        id\n        text\n        voteCount\n        selfVoted\n      }\n    }\n  ,\n    fragment QuestionTag on QuestionTag {\n      tag {\n        id\n        name\n        normalizedTag\n        questionFrequency\n      }\n      creator {\n        nickname\n        displayedName\n      }\n      hidden\n      self {\n        hasAddedQuestionTag\n      }\n    }\n  ,\n    fragment BlickwechselEvent on BlickwechselEvent {\n      status\n      eventTitle\n      shortTitle\n      eventDescription\n      eventType\n      detailsUrl\n      plannedFor\n      tag {\n        slug\n      }\n      user {\n        displayedName\n        nickname\n        ...AuthorAvatar\n        coverUrls {\n          urls {\n            mobile\n            desktopNmms\n          }\n        }\n      }\n      blickwechselStatistics {\n        totalQuestionCount\n        answeredQuestionCount\n      }\n    }\n  ,\n    fragment Reaction on ReactionEmoji {\n      user {\n        slug\n        displayedName\n      }\n      identifier\n    }\n  ,\n    fragment Avatar on UserAvatar {\n      urls {\n        default\n        nmmslarge\n      }\n      webpUrls {\n        default\n        nmmslarge\n      }\n    }\n  ,\n    fragment ExpertVerification on ExpertVerification {\n      user {\n        displayedName\n        nickname\n        ...AuthorAvatar\n        expertProfile {\n          reason\n        }\n      }\n    }\n  ,\n    fragment Comment on Comment {\n      id\n      createdAt\n      htmlBody\n      parentId\n      author {\n        ...Author\n        ...AuthorAvatar\n      }\n      voteCount\n      voteStatus\n      status\n      reactions {\n        ...Reaction\n      }\n    }\n  ,\n    fragment QuestionCommentReply on QuestionCommentReply {\n      id\n      body\n      createdAt\n      user {\n        nickname\n        displayedName\n        roles\n        ...AuthorAvatar\n        ...ScoreLevel\n      }\n    }\n  \n      ","variables":{"slug":slug,"includeQuestionAuthorStatistics":False}}
        cookies = {'gfAccessToken': self.accessToken, 'gfRefreshToken':self.refreshToken, 'gf-li':'1'}
        req2 = requests.post("https://www.gutefrage.net/graphql", headers = self.headers, cookies = cookies, json = myobj)
        if req2.status_code == 200:
          jsonied = json.loads(req2.text)
          return jsonied["data"]["questionBySlug"]
        else:
          print(req2.status_code)
          print(req2.text)

      def info(self, *args):
          self.subrefferer = "nmms-api/questions/"
          req = requests.get('https://www.gutefrage.net/nmms-api/questions/'+str(self.id), headers = self.headers)
          jsontext = json.loads(req.text)
          if len(args) == 0:
            return jsontext
          else:
            for arg in args:
              return jsontext[arg]
          # elif data == "title":
          #   return jsontext["title"]
          # elif data == "id":
          #   return jsontext["id"]
          # elif data == "userid":
          #   return jsontext["userid"]
          # elif data == "stripped_title":
          #   return jsontext["stripped_title"]
          # elif data == "tag_ids":
          #   return jsontext["tag_ids"]
      
      def replies(self):
        self.subrefferer = "nmms-api/questions/"
        req = requests.get('https://www.gutefrage.net/nmms-api/questions/'+str(self.id), headers = self.headers)
        jsontext = json.loads(req.text)
        slug = jsontext["stripped_title"]
        self.subrefferer = "mitteilungen"
        myobj = {"query":"\n        \n    query QdpLoggedIn($slug: String!) {\n      questionBySlug(questionSlug: $slug) {\n        ...StandardQdp\n      }\n    }\n  \n\n        \n    fragment StandardQdp on Question {\n      id\n      title\n      htmlBody\n      slug\n      self {\n        hasUpvotedQuestion\n        hasBookmarkedQuestion\n        isFollowingQuestion\n        canVerifyAnswer\n        editCapabilities\n      }\n      author {\n        ...Author\n        ...AuthorAvatar\n        ...ScoreLevel\n        statistics {\n          questionCounts {\n            totalCount\n          }\n        }\n      }\n      adultContent {\n        ads {\n          hasReportedContentViolation\n        }\n      }\n      marketingChannel {\n        channel\n        subchannel\n      }\n      questionTags {\n        ...QuestionTag\n      }\n      createdAt\n      stats {\n        impressions {\n          total\n        }\n      }\n      answers {\n        ...Answer\n      }\n      images {\n        ...ContentImage\n      }\n      supportHint\n      poll {\n        ...QuestionPoll\n      }\n      status\n      upvotes\n      followerCount\n      mostHelpfulAnswerStatus\n      isResubmissionBlocked\n      resubmissionCount\n      latestSubmission {\n        isResubmission\n        datetime\n        user {\n          id\n          nickname\n          displayedName\n          ...AuthorAvatar\n        }\n      }\n      activities {\n        activityId\n        activity\n        expiresAt\n      }\n      latestActivityAt\n      recommendedQuestions {\n        question {\n          id\n          title\n          slug\n          htmlBody\n          createdAt\n          answerCount\n          author {\n            nickname\n            displayedName\n            ...AuthorAvatar\n          }\n        }\n        poolName\n      }\n      recommendedQuestionsForContentAuthors: recommendedQuestionsForContentAuthors {\n        question {\n          id\n          title\n          slug\n          htmlBody\n          createdAt\n          answerCount\n          author {\n            nickname\n            displayedName\n            ...AuthorAvatar\n          }\n        }\n        poolName\n      }\n      clarifications {\n        ...QuestionClarification\n      }\n      comments {\n        ...QuestionComment\n      }\n      blickwechsel {\n        userId\n      }\n      category {\n        category {\n          id\n          name\n          slug\n          description\n        }\n        parentCategories {\n          name\n          slug\n        }\n      }\n    }\n  ,\n    fragment Author on User {\n      id\n      displayedName\n      nickname\n      createdAt\n      roles\n      expertProfile {\n        qualification\n        reason\n        tags {\n          name\n        }\n      }\n      ...ScoreLevel\n      onlineStatus\n    }\n  ,\n    fragment AuthorAvatar on User {\n      avatar {\n        urls {\n          default\n          nmmslarge\n        }\n        webpUrls {\n          default\n          nmmslarge\n        }\n      }\n    }\n  ,\n    fragment ScoreLevel on User {\n      scoreLevel {\n        level\n        levelGroup\n        progress {\n          percent\n          score\n          scoreLevelStart\n          scoreNextLevel\n        }\n      }\n    }\n  ,\n    fragment ContentImage on Image {\n      id\n      urls {\n        big\n        full\n      }\n      webpUrls {\n        big\n        full\n      }\n      description\n    }\n  ,\n    fragment Answer on Answer {\n      __typename\n      id\n      questionId\n      createdAt\n      stats {\n        impressions {\n          total\n        }\n      }\n      htmlBody\n      author {\n        ...Author\n        ...AuthorAvatar\n        ...ScoreLevel\n        userExpertises {\n          expertiseType\n          description\n          tags {\n            name\n          }\n        }\n      }\n      expertVerifications {\n        ...ExpertVerification\n      }\n      isMostHelpful\n      comments {\n        ...Comment\n      }\n      images {\n        ...ContentImage\n      }\n      pollVote {\n        choiceId\n        text\n      }\n      userSatisfaction {\n        counts {\n          positive\n        }\n        self\n      }\n      appreciation {\n        totalCount\n        self {\n          isAllowed\n          hasAlreadyAppreciated\n        }\n      }\n      video {\n        externalUrl\n      }\n      expertise\n      latestVersion {\n        createdAt\n        version\n      }\n      status\n      isDeleted\n    }\n  ,\n    fragment QuestionComment on QuestionComment {\n      id\n      body\n      createdAt\n      author {\n        nickname\n        displayedName\n        roles\n        ...AuthorAvatar\n        ...ScoreLevel\n      }\n      reply {\n        ...QuestionCommentReply\n      }\n    }\n  ,\n    fragment QuestionClarification on QuestionClarification {\n      id\n      body\n      createdAt\n      author {\n        slug\n      }\n      images {\n        ...ContentImage\n      }\n    }\n  ,\n    fragment QuestionPoll on Poll {\n      choices {\n        id\n        text\n        voteCount\n        selfVoted\n      }\n    }\n  ,\n    fragment QuestionTag on QuestionTag {\n      tag {\n        id\n        name\n        normalizedTag\n        questionFrequency\n      }\n      creator {\n        nickname\n        displayedName\n      }\n      hidden\n      self {\n        hasAddedQuestionTag\n      }\n    }\n  ,\n    fragment ExpertVerification on ExpertVerification {\n      user {\n        displayedName\n        nickname\n        ...AuthorAvatar\n        expertProfile {\n          reason\n        }\n      }\n    }\n  ,\n    fragment Comment on Comment {\n      id\n      createdAt\n      htmlBody\n      parentId\n      author {\n        ...Author\n        ...AuthorAvatar\n      }\n      voteCount\n      voteStatus\n      status\n    }\n  ,\n    fragment QuestionCommentReply on QuestionCommentReply {\n      id\n      body\n      createdAt\n      user {\n        nickname\n        displayedName\n        roles\n        ...AuthorAvatar\n        ...ScoreLevel\n      }\n    }\n  \n      ","variables":{"slug":slug}}
        cookies = {'gfAccessToken': self.accessToken, 'gfRefreshToken':self.refreshToken, 'gf-li':'1'}
        req2 = requests.post("https://www.gutefrage.net/graphql", headers = self.headers, cookies = cookies, json = myobj)
        
        if req2.status_code == 200:
          parsed = json.loads(req2.text)
          replies = parsed["data"]["questionBySlug"]["answers"]
          return replies
        else:
          print(req2.status_code)
          print(req2.text)
        


      def _like(self): 
        self.id = int(self.id)
        self.subrefferer = "mitteilungen"
        myobj = {"query":"\n        \n    mutation UpvoteQuestion($questionId: Int!) {\n      question {\n        upvotes: upvote(questionId: $questionId)\n      }\n    }\n  \n\n        \n      ","variables":{"questionId":self.id}}
        cookies = {'gfAccessToken': self.accessToken, 'gfRefreshToken':self.refreshToken, 'gf-li':'1'}
        req2 = requests.post("https://www.gutefrage.net/graphql", headers = self.headers, cookies = cookies, json = myobj)
        if req2.status_code == 200:
          return True
        else:
          print(req2.status_code)
          print(req2.text)
          return False
    



  def new(self, amount: int):
    cookies = {'gfAccessToken': self.accessToken, 'gfRefreshToken':self.refreshToken, 'gf-li':'1'}
    myobj = {"query":"\n        \n    query LatestQuestions(\n      $limit: Int!\n      $onlyUnanswered: Boolean!\n      $onlyResubmitted: Boolean!\n      $downCursor: StreamCursor\n      $ownUserId: Int!\n      $fromDateTime: OffsetDateTime\n    ) {\n      questions {\n        stream {\n          byLatestSubmission(\n            limit: $limit\n            onlyUnanswered: $onlyUnanswered\n            onlyResubmitted: $onlyResubmitted\n            downCursor: $downCursor\n            fromDateTime: $fromDateTime\n          ) {\n            questions {\n              ...Question\n            }\n            boundaries {\n              down {\n                cursor\n              }\n            }\n          }\n        }\n      }\n      userById(userId: $ownUserId) {\n        userInterests {\n          tag {\n            name\n            slug\n            questionFrequency\n          }\n        }\n      }\n    }\n  \n\n        \n    fragment Question on Question {\n      __typename\n      id\n      slug\n      title\n      htmlBody\n      upvotes\n      self {\n        hasUpvotedQuestion\n        hasBookmarkedQuestion\n      }\n      clarifications {\n        id\n        body\n        createdAt\n        isDeleted\n      }\n      questionTags {\n        tag {\n          id\n          name\n          normalizedTag\n          slug\n          questionFrequency\n        }\n        hidden\n        hiddenByUser {\n          slug\n          displayedName\n        }\n        creator {\n          slug\n          displayedName\n        }\n      }\n      questionStatus: status\n      isDeleted\n      isApprovedByAdmin\n      deletionInfo {\n        ...QuestionDeletionInfo\n      }\n      createdAt\n      answerCount\n      resubmissionCount\n      latestSubmission {\n        isResubmission\n        datetime\n        user {\n          id\n          nickname\n          displayedName\n          ...AuthorAvatar\n        }\n      }\n      poll {\n        choices {\n          id\n          text\n          voteCount\n        }\n      }\n      images {\n        id\n        urls {\n          big\n          thumbnail\n        }\n        webpUrls {\n          big\n          thumbnail\n        }\n      }\n      author {\n        ...Author\n        ...AuthorMods\n      }\n      mostHelpfulAnswerStatus\n      complaints {\n        ...Complaint\n      }\n      category {\n        ...Category\n      }\n      moderationAnnotations {\n        ...ModerationAnnotation\n      }\n    }\n  ,\n    fragment Author on User {\n      id\n      nickname\n      displayedName\n      createdAt\n      ...AuthorAvatar\n      roles\n      onlineStatus\n    }\n  ,\n    fragment AuthorMods on User {\n      complaints {\n        type\n      }\n    }\n  ,\n    fragment AuthorAvatar on User {\n      avatar {\n        urls {\n          default\n          nmmslarge\n        }\n        webpUrls {\n          default\n          nmmslarge\n        }\n      }\n    }\n  ,\n    fragment Complaint on Complaint {\n      createdAt\n      message\n      type\n      user {\n        displayedName\n        nickname\n      }\n    }\n  ,\n    fragment Category on HierarchicalCategory {\n      category {\n        name\n      }\n      parentCategories {\n        name\n      }\n    }\n  ,\n    fragment QuestionDeletionInfo on QuestionDeletion {\n      moderator {\n        nickname\n        displayedName\n      }\n      reason {\n        __typename\n        ... on QuestionDeletionCustomReason {\n          freetext\n        }\n        ... on QuestionDeletionPredefinedReason {\n          value\n        }\n      }\n    }\n  ,\n    fragment ModerationAnnotation on ModerationAnnotation {\n      id\n      user {\n        id\n        slug\n        displayedName\n      }\n      content\n      createdAt\n      leastRequiredRole\n      entityId\n      entity {\n        __typename\n        ... on User {\n          id\n          displayedName\n          slug\n        }\n        ... on Question {\n          id\n        }\n      }\n    }\n  \n      ","variables":{"onlyUnanswered":False,"onlyResubmitted":False,"limit":amount,"ownUserId":1}}

    subrefferer = "home/neue/alle"
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36", "X-Client-Id":"net.gutefrage.nmms.desktop", "x-api-key":"dfdza43a-8560-4641-b316-ff928232734c","Origin":"https://www.gutefrage.net", "Referer":"https://www.gutefrage.net/"+subrefferer,"Sec-Fetch-Site":"same-origin","Content-Type":"application/json"}

    req_new = requests.post("https://www.gutefrage.net/graphql", headers=headers, json=myobj, cookies = cookies)
    parsed = json.loads(req_new.text)
    questions = parsed["data"]["questions"]["stream"]["byLatestSubmission"]["questions"]
    quests = []
    # print(json.dumps(questions, indent=4, sort_keys=True))
    for xe in questions:
      quests.append(self.question(xe["id"]))
    return quests
    # print(req_new.text)
    
  def user(self, nick):
    return self._user(nick, self.accessToken, self.refreshToken)
  
  class _user:
      def __init__(self, nick, accessToken, refreshToken):
        self.accessToken = accessToken
        self.refreshToken = refreshToken
        self.nick = nick
        self.subrefferer = ""
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36", "X-Client-Id":"net.gutefrage.nmms.desktop", "x-api-key":"dfdza43a-8560-4641-b316-ff928232734c","Origin":"https://www.gutefrage.net", "Referer":"https://www.gutefrage.net/"+self.subrefferer,"Sec-Fetch-Site":"same-origin","Content-Type":"application/json"}

      def info(self):
        self.subrefferer = self.nick
        cookies = {'gfAccessToken': self.accessToken, 'gfRefreshToken':self.refreshToken, 'gf-li':'1'}
        myobj = {"query":"\n        \n    query UserProfile($nickname: String!) {\n      user {\n        byNickname(nickname: $nickname) {\n          id\n          slug\n          displayedName\n          profileData {\n            aboutMe\n            aboutMeInEmojis {\n              identifier\n            }\n            address {\n              street\n              city\n              zipCode\n              country\n              countryCode\n            }\n            partialDateOfBirth: dateOfBirth {\n              year\n              month\n              day\n            }\n            gender\n            profession\n            webUrl\n          }\n          statistics {\n            answerCounts {\n              totalCount\n              liveCount\n            }\n            appreciations\n            compliments\n            friends\n            mostHelpfulAnswers\n            questionCounts {\n              totalCount\n              liveCount\n            }\n            questionResubmissions\n          }\n          availableMonthlySummaries {\n            yearMonth {\n              year\n              month\n            }\n          }\n          businessProfileInformation {\n            email\n            faxNumber\n            phoneNumber\n            webUrl\n          }\n          badgeGroups {\n            awardedBadges {\n              awardedAt\n              badge {\n                title\n                description\n                message\n                imageUrl\n              }\n            }\n            badgeInProgress {\n              badge {\n                title\n                description\n                message\n                imageUrl\n              }\n              progressPercentage\n            }\n          }\n          userInterests {\n            tag {\n              name\n              slug\n              questionFrequency\n            }\n          }\n          expertProfile {\n            qualification\n            reason\n            tags {\n              name\n              slug\n              questionFrequency\n            }\n          }\n          userExpertises {\n            description\n            expertiseType\n            id\n            tags {\n              name\n            }\n          }\n          createdAt\n          roles\n          ...AuthorAvatar\n          coverUrls {\n            baseUrl\n            urls {\n              desktop\n              mobile\n              desktopNmms\n            }\n          }\n          ...ScoreLevel\n          complaints {\n            createdAt\n            message\n            type\n            user {\n              displayedName\n              slug\n            }\n          }\n          isInactive\n          moderation {\n            suspendedReason\n            isInTestGroup\n          }\n          self {\n            messagePermissions {\n              allowedToSendMessageStatus\n            }\n            isBlocked\n          }\n          friendship {\n            self {\n              friendshipStatus\n            }\n            pendingRequests {\n              sent {\n                requests {\n                  sender {\n                    slug\n                    displayedName\n                    createdAt\n                    roles\n                    ...AuthorAvatar\n                  }\n                  receiverId\n                  message\n                }\n              }\n            }\n          }\n          isPubliclyVisible\n          onlineStatus\n        }\n      }\n    }\n  \n\n        \n    fragment AuthorAvatar on User {\n      avatar {\n        ...Avatar\n      }\n    }\n  ,\n    fragment ScoreLevel on User {\n      scoreLevel {\n        level\n        levelGroup\n        progress {\n          percent\n          score\n          scoreLevelStart\n          scoreNextLevel\n        }\n      }\n    }\n  ,\n    fragment Avatar on UserAvatar {\n      urls {\n        default\n        nmmslarge\n      }\n      webpUrls {\n        default\n        nmmslarge\n      }\n    }\n  \n      ","variables":{"nickname":self.nick}}

        subrefferer = "home/neue/alle"
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36", "X-Client-Id":"net.gutefrage.nmms.desktop", "x-api-key":"dfdza43a-8560-4641-b316-ff928232734c","Origin":"https://www.gutefrage.net", "Referer":"https://www.gutefrage.net/"+subrefferer,"Sec-Fetch-Site":"same-origin","Content-Type":"application/json"}

        req_new = requests.post("https://www.gutefrage.net/graphql", headers=headers, json=myobj, cookies = cookies)
        parsed = json.loads(req_new.text)
        return parsed["data"]["user"]["byNickname"]

      def friendreq(self, text):
        myobj = {"query":"\n        \n    mutation RequestFriendship($otherUserNickname: String!, $text: String) {\n      friendship {\n        requestFriendship(otherUserNickname: $otherUserNickname, text: $text)\n      }\n    }\n  \n\n        \n      ","variables":{"otherUserNickname":self.nick,"text":text}}
        cookies = {'gfAccessToken': self.accessToken, 'gfRefreshToken':self.refreshToken, 'gf-li':'1'}
        req2 = requests.post("https://www.gutefrage.net/graphql", headers = self.headers, cookies = cookies, json = myobj)
        if req2.status_code == 200:
          return True
        else:
          print(req2.status_code)
          print(req2.text)
          return False


  def post(self, title="", body="", tags=[], poll_choices=[], subscribe=False, images=[]):
        if len(tags) == 0:
          print("Kein Tags argument angegeben")
          return False
        elif len(tags) == 1:
          print("Nur ein Tags argument angegeben")
          return False
        myobj = {"query":"\n        \n    mutation ValidateQuestion(\n      $title: String!\n      $body: String\n      $tags: [String!]!\n      $poll_choices: [NewPollChoice!]\n      $subscribe: Boolean\n    ) {\n      question {\n        validate(\n          question: {\n            title: $title\n            body: $body\n            tags: $tags\n            pollChoices: $poll_choices\n            subscribe: $subscribe\n          }\n        )\n      }\n    }\n  \n\n        \n      ","variables":{"title":title,"body":body,"tags":tags,"poll_choices":poll_choices,"subscribe":subscribe,"images":images}}

        
        cookies = {'gfAccessToken': self.accessToken, 'gfRefreshToken':self.refreshToken, 'gf-li':'1'}
        req2 = requests.post("https://www.gutefrage.net/graphql", headers = self.headers, cookies = cookies, json = myobj)
        if req2.status_code == 200:
          return True
        else:
          print(req2.status_code)
          print(req2.text)
          return False
