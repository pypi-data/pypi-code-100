# -*- coding: utf-8 -*-
"""
    pod2gen
    ~~~~~~

    :copyright: 2013, Lars Kiesow <lkiesow@uos.de>; 2016, Thorben Dahl
        <thorben@sjostrom.no>; 2021, Slim Beji <mslimbeji@gmail.com>
    :license: FreeBSD and LGPL, see license.* for more details.
"""
import datetime
import sys

from dateutil import tz


def print_enc(s):
    """Print function accepting strings and byte arrays."""
    print(s.decode("utf-8") if type(s) == type(b"") else s)


def main():
    """Create an example podcast and print it or save it to a file."""
    # There must be exactly one argument, and it is must end with rss
    if len(sys.argv) != 2 or not (sys.argv[1].endswith("rss")):
        # Invalid usage, print help message
        # print_enc is just a custom function which functions like print,
        # except it deals with byte arrays properly.
        print_enc("Usage: %s ( <file>.rss | rss )" % "python -m pod2gen")
        print_enc("")
        print_enc(
            "  rss              -- Generate RSS test output and print it to stdout."
        )
        print_enc(
            "  <file>.rss       -- Generate RSS test teed and write it to file.rss."
        )
        print_enc("")
        exit()

    # Remember what type of feed the user wants
    arg = sys.argv[1]

    from pod2gen import (
        AlternateMedia,
        Category,
        Funding,
        License,
        Location,
        Media,
        Person,
        Podcast,
        Soundbite,
        Trailer,
        Transcript,
        htmlencode,
    )

    # Initialize the feed
    p = Podcast()
    p.name = "Testfeed"
    p.authors.append(Person("Lars Kiesow", "lkiesow@uos.de"))
    p.website = "http://example.com"
    p.copyright = "cc-by"
    p.description = "This is a cool feed!"
    p.is_serial = True
    p.language = "de"
    p.location = Location("Austin, TX", osm="R113314", geo="geo:30.2672,97.7431")
    p.feed_url = "http://example.com/feeds/myfeed.rss"
    p.add_funding(Funding("Support the show!", "https://www.example.com/donations"))
    p.add_funding(Funding("Become a member!", "https://www.example.com/members"))
    p.category = Category("Leisure", "Aviation")
    p.explicit = False
    p.complete = False
    p.new_feed_url = "http://example.com/new-feed.rss"
    p.owner = Person("John Doe", "john@example.com")
    p.locked = False
    p.xslt = "http://example.com/stylesheet.xsl"

    e1 = p.add_episode()
    e1.id = "http://lernfunk.de/_MEDIAID_123#1"
    e1.title = "First Element"
    e1.season = 1
    e1.season_name = "Volume 1"
    e1.episode_number = 1
    e1.episode_name = "First episode"
    e1.chapters_json = "https://example.com/episode1/chapters.json"
    e1.summary = htmlencode(
        """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Tamen
            aberramus a proposito, et, ne longius, prorsus, inquam, Piso, si ista
            mala sunt, placet. Aut etiam, ut vestitum, sic sententiam habeas aliam
            domesticam, aliam forensem, ut in fronte ostentatio sit, intus veritas
            occultetur? Cum id fugiunt, re eadem defendunt, quae Peripatetici,
            verba <3."""
    )
    e1.link = "http://example.com"
    e1.authors = [Person("Lars Kiesow", "lkiesow@uos.de")]
    e1.publication_date = datetime.datetime(2014, 5, 17, 13, 37, 10, tzinfo=tz.UTC)
    e1.media = Media(
        "http://example.com/episodes/loremipsum.mp3",
        454599964,
        duration=datetime.timedelta(hours=1, minutes=32, seconds=19),
    )
    e1.add_soundbite(Soundbite(1234.5, 42.25, text="Why the Podcast Namespace Matters"))
    e1.add_soundbite(Soundbite(73.0, 60))
    transcript1 = Transcript(
        "https://examples.com/transcript_sample.txt",
        "text/html",
        language="es",
        is_caption=True,
    )
    e1.add_transcript(transcript1)
    transcript2 = Transcript(
        "https://examples.com/transcript_sample_2.txt", "text/html"
    )
    e1.add_transcript(transcript2)
    e1.location = Location(
        "Dreamworld (Queensland)", geo="geo:-27.86159,153.3169", osm="W43678282"
    )
    persons = [
        Person(
            name="Becky Smith",
            group="visuals",
            role="Cover Art Designer",
            href="https://example.com/artist/beckysmith",
            img="http://example.com/images/alicebrown.jpg",
        ),
        Person(
            email="mslimbeji@gmail.com",
            group="writing",
            role="guest writer",
            href="https://www.wikipedia/slimbeji",
            img="http://example.com/images/slimbeji.jpg",
        ),
    ]
    e1.persons = persons
    e1.episode_number = 1
    p.persons = persons

    trailers = [
        Trailer(
            text="Coming April 1st, 2021",
            url="https://example.org/trailers/teaser",
            pubdate=datetime.datetime(2021, 8, 15, 8, 15, 12, 0, tz.UTC),
            length=12345678,
            type="audio/mp3",
            season=2,
        )
    ]
    p.trailers = trailers

    license = License(
        "my-podcast-license-v1", "https://example.org/mypodcastlicense/full.pdf"
    )
    e1.license = license
    p.license = license
    p.generate_guid()

    am = AlternateMedia(
        "audio/mp4",
        43200000,
        bitrate=128000,
        height=1080,
        lang="en-US",
        title="Standard",
        rel="Off stage",
        codecs="mp4a.40.2",
        default=False,
        encryption="sri",
        signature="sha384-ExVqijgYHm15PqQqdXfW95x+Rs6C+d6E/ICxyQOeFevnxNLR/wtJNrNYTjIysUBo",
    )
    am.sources = {
        "https://example.com/file-0.mp3": None,
        "ipfs://QmdwGqd3d2gFPGeJNLLCshdiPert45fMu84552Y4XHTy4y": None,
        "https://example.com/file-0.torrent": "application/x-bittorrent",
    }
    e1.add_alternate_media(am)

    # Should we just print out, or write to file?
    if arg == "rss":
        # Print
        print_enc(p.rss_str())
    elif arg.endswith("rss"):
        # Write to file
        p.rss_file(arg, minimize=True)


if __name__ == "__main__":
    main()
