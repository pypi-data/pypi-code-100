from ..activitypub import Commit, Person, PublicKey
from ..architecture.dvcs import factory as dvcs_factory
from ..format import format


class ActivityPub(object):
    def inbox(self, activity):
        if activity["type"] == "Commit":
            return Commit().from_dict(activity)

    def commit_get(self, d):
        dvcs = dvcs_factory(d)
        return Commit(
            **{
                "jsonld_context": [
                    "https://www.w3.org/ns/activitystreams",
                    "https://w3id.org/security/v1",
                    "https://forgefed.peers.community/ns",
                ],
                "context": dvcs.url,
                "hash": dvcs.hash,
            }
        )

    def person_get(self, d, url, username):
        users = {}

        def load(u):
            users[u["username"]] = u

        format.FormatUsers().load(f"{d}/users.json", load)
        u = users[username]

        i = None
        for e in format.FormatIdentities().load(f"{d}/identities.json"):
            if e["url"] == u["url"]:
                i = e
        assert i, f"No identity found for {u['url']}"
        url = f"{url}/user/{username}"
        return Person(
            **{
                "jsonld_context": [
                    "https://www.w3.org/ns/activitystreams",
                    "https://w3id.org/security/v1",
                    {
                        "manuallyApprovesFollowers": "as:manuallyApprovesFollowers",
                        "schema": "http://schema.org#",
                        "PropertyValue": "schema:PropertyValue",
                        "value": "schema:value",
                    },
                ],
                "id": url,
                "preferredUsername": username,
                "name": username,
                "inbox": f"{url}/inbox",
                "outbox": f"{url}/outbox",
                "followers": f"{url}/followers",
                "following": f"{url}/following",
                "summary": "",
                "publicKey": PublicKey(
                    id=f"{url}/#main-key",
                    owner=url,
                    publicKeyPem=i["public"],
                ),
                "manuallyApprovesFollowers": False,
                "discoverable": True,
            }
        )
