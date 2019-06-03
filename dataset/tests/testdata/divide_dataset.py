splitLen = 10         # 20 lines per file
outputBase = 'small' # output.1.txt, output.2.txt, etc.

# This is shorthand and not friendly with memory
# on very large files (Sean Cavanagh), but it works.
input = open('tweet_to_work.csv', 'r').read().split('\n')

at = 1
for lines in range(0, 10*25, splitLen):
    # First, get the list slice
    outputData = input[lines:lines+splitLen]

    # Now open the output file, join the new slice with newlines
    # and write it out. Then close the file.
    output = open(outputBase + str(at) + '.csv', 'w')
    output.write('\n'.join(outputData))
    output.close()

    # Increment the counter
    at += 1
