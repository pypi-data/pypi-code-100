#!/usr/bin/env python
#************************************************************************
# Copyright 2021 O7 Conseils inc (Philippe Gosselin)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#************************************************************************
"""Module allows to view and access CodeCommit"""

#--------------------------------
#
#--------------------------------
import logging
import pprint

import o7lib.util.input
import o7lib.util.displays
import o7lib.aws.base

logger=logging.getLogger(__name__)


#*************************************************
#
#*************************************************
class CodeCommit(o7lib.aws.base.Base):
    """Class for Codecommit for a Profile & Region"""
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html

    #*************************************************
    #
    #*************************************************
    def __init__(self, profile = None, region = None, session = None):
        super().__init__(profile=profile, region=region, session=session)
        self.ccClient = self.session.client('codecommit')



    #*************************************************
    #
    #*************************************************
    def LoadRepos(self):
        """Returns all Repos for this Session"""

        logger.info(f'LoadRepos')

        repos = []
        param={}


        done=False
        while not done:


            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.list_repositories
            resp = self.ccClient.list_repositories(**param)
            #pprint.pprint(resp)

            if 'nextToken' in resp:
                param['nextToken'] = resp['nextToken']
            else:
                done = True

            logger.info(f'LoadRepos: Number of Repos found {len(resp["repositories"])}')
            if len(resp["repositories"]) == 0:
                break

            repositoryNames = []
            for repositorie in resp["repositories"]:
                repositoryNames.append(repositorie['repositoryName'])

            respDetails = self.ccClient.batch_get_repositories(repositoryNames = repositoryNames)
            # # pprint.pprint(respDetails)
            repos += respDetails["repositories"]

        return repos


    #*************************************************
    #
    #*************************************************
    def LoadBranches(self, repoName):
        """Returns all Branches for this Repo"""

        logger.info(f'LoadBranches {repoName=}')

        branches = []
        param={
            'repositoryName' : repoName
        }

        done=False
        while not done:


            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.list_branches
            resp = self.ccClient.list_branches(**param)
            #pprint.pprint(resp)

            if 'nextToken' in resp:
                param['nextToken'] = resp['nextToken']
            else:
                done = True

            logger.info(f'LoadBranches: Number of Branches found {len(resp["branches"])}')
            branches += resp["branches"]

        return branches

    #*************************************************
    #
    #*************************************************
    def LoadPullRequests(self, repoName):
        """Returns all Branches for this Repo"""

        logger.info(f'LoadPullRequests {repoName=}')

        prs = []
        param={
            'repositoryName' : repoName,
            'pullRequestStatus' : 'OPEN'
        }

        done=False
        while not done:


            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.list_pull_requests
            resp = self.ccClient.list_pull_requests(**param)
            #pprint.pprint(resp)

            if 'nextToken' in resp:
                param['nextToken'] = resp['nextToken']
            else:
                done = True

            logger.info(f'LoadPullRequests: Number of Pull Request found {len(resp["pullRequestIds"])}')
            if len(resp["pullRequestIds"]) == 0:
                break

            for prId in resp["pullRequestIds"]:
                respDetails = self.ccClient.get_pull_request(pullRequestId = prId)
                prs.append(respDetails['pullRequest'])

        return prs

    #*************************************************
    #
    #*************************************************
    def DisplayRepos(self, repos):
        """Displays a summary of Repos in a Table Format"""
        self.ConsoleTitle(left='CodeCommit Repositories List')
        print('')
        params = {
            'columns' : [
                {'title' : 'id'      , 'type': 'i',       'minWidth' : 4  },
                {'title' : 'Name'    , 'type': 'str',  'dataName': 'repositoryName'},
                {'title' : 'Created', 'type': 'date', 'dataName': 'creationDate'},
                {'title' : 'Updated', 'type': 'since', 'dataName': 'lastModifiedDate'},
                {'title' : 'Default', 'type': 'str', 'dataName': 'defaultBranch'},
                {'title' : 'Description' , 'type': 'str', 'dataName': 'repositoryDescription'},
            ]
        }
        o7lib.util.displays.Table(params, repos)

    #*************************************************
    #
    #*************************************************
    def MenuRepoDetails(self, repoName):
        """Menu to view and edit details of a Repo"""



        while True :

            pprint.pprint(self.LoadBranches(repoName))
            pprint.pprint(self.LoadPullRequests(repoName))

            # repos = self.LoadRepos()
            # self.DisplayRepos(repos)
            keyType, key = o7lib.util.input.InputMulti('Option -> Back(b) Details(int): ')

            if keyType == 'str':
                if key.lower() == 'b':
                    break

                # if key.lower() == 'r':
                #     #pprint.pprint(repos)
                #     o7lib.util.input.WaitInput()


            # if keyType == 'int' and key > 0 and key <= len(repos):

            #     o7lib.util.input.WaitInput()


    #*************************************************
    #
    #*************************************************
    def MenuRepos(self):
        """Menu to view and edit all codecommit repos in current region"""

        while True :

            repos = self.LoadRepos()
            self.DisplayRepos(repos)
            keyType, key = o7lib.util.input.InputMulti('Option -> Back(b) Details(int): ')

            if keyType == 'str':
                if key.lower() == 'b':
                    break

                if key.lower() == 'r':
                    pprint.pprint(repos)
                    o7lib.util.input.WaitInput()


            if keyType == 'int' and key > 0 and key <= len(repos):
                self.MenuRepoDetails(repos[key - 1].get('repositoryName'))

#*************************************************
#
#*************************************************
if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)-5.5s] [%(name)s] %(message)s"
    )

    CodeCommit().MenuRepos()
