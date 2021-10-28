from hindiwsd import wsd, lesks


def wordsense(sentence):

    hinglish, hindi = wsd.preprocess_transliterate(sentence)
    pos = wsd.POS_tagger(hindi)

    for i in pos:
        lesks.lesk(i[0], i[1], hindi)

wordsense("mein baahar jaa rahaa hu")