lines_seen = set() # holds lines already seen
outfile = open("tweet_to_work.csv", "w")
for line in open("tweets_processed.csv", "r"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()
