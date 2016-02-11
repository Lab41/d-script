# Top k (soft criteria)
k = 10
# Max top (hard criteria)
maxtop = 3
# Number of examples per image
g = 8

# Run through the adjacency matrix
softcorrect = 0
hardcorrect = 0
totalnum = 0
for j, i in enumerate(F):
    if ((j-1) % g) == 0:
        continue
    topk = i.argsort()[-k:]
    # Soft criteria
    if j/g in topk/g:
        softcorrect += 1
    totalnum +=1
    # Hard criteria
    hardcriteria = sum([1 for jj in (j/g == topk[-maxtop:]/g) if jj])
    if hardcriteria == maxtop:
	hardcorrect+=1

# Print out results    
print "Not considering disguised handwriting"
print "Top %d (soft criteria) = %f" %( k, (softcorrect+0.0) / totalnum )
print "Top %d (hard criteria) = %f" %( k, (hardcorrect+0.0) / totalnum / maxtop )


