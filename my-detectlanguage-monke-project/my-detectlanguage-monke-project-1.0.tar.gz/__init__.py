def dl(string):
    english = ["more", "wholesome", "milk", "comb", "who", "what", "where", "whose", "how", "why",
                "the", "when", "have", "quite", "verb", "just", "burger", "contain", "consist",
                "he", "she", "they", "quotient", "red", "green", "yellow", "blue", "green", "black",
                "of", "in", "aboard", "about", "against", "along", "mid", "anti", "among", "sus", "between",
                "at", "there", "some", "my", "of", "be", "use", "her", "than", "her", "and",
                "this", "an", "would", "first", "have", "each", "make", "water", "to", "from", "to", "which",
                "like", "been", "in", "or", "him", "call", "is", "one", "do", "into", "who", "you", "had",
                "time", "oil", "that", "by", "their", "has", "it's", "it", "word", "if", "look", "now", "but", 
                "will", "two", "find", "was", "not", "up", "more", "long", "for", "other", "write", "down",
                "on", "all", "about", "go", "day", "are", "were", "out", "see", "did", "will", "am", "is", "love",
                "i", "I", "neither", "nor", "cover", "english", "lish", "rish", "ese"
                ]


    if any(x in string for x in english):
        print("english")



dl("vietnamese")