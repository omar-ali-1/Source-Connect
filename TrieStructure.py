import sys



class TrieNode(object):
    def __init__(self):
        self.word = None
        self.item = None
        self.childrenCount = 0
        self.children = {}


class TrieTree(object):
    def __init__(self):
        self.head = TrieNode()
        self.nodeCount = 1
        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', \
            'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ']

    def insert(self, word, item):
        self.nodeCount += 1
        node = self.head
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TrieNode()
            node = node.children[letter]

        node.word = word
        node.item = item

    # The search function returns a list of all words that are less than the given
    # maximum distance from the target word
    def search(self, word, maxCost):
        # build first row
        currentRow = range(len(word) + 1)
        results = []
        trie = self.head
        # recursively search each branch of the trie
        for letter in trie.children:
            self.searchRecursive(trie.children[letter], letter, word, currentRow,
                results, maxCost, 0)
        return results

    # This recursive helper is used by the search function above. It assumes that
    # the previousRow has been filled in already.
    def searchRecursive(self, node, letter, word, previousRow, results, maxCost, index):
        columns = len( word ) + 1
        currentRow = [ previousRow[0] + 1 ]
        # Build one row for the letter, with a column for each letter in the target
        # word, plus one for the empty string at column 0
        for column in xrange( 1, columns ):
            insertCost = currentRow[column - 1] + 1
            deleteCost = previousRow[column] + 1
            if word[column - 1] != letter:
                replaceCost = previousRow[ column - 1 ] + 1
            else:
                replaceCost = previousRow[ column - 1 ]
            currentRow.append( min( insertCost, deleteCost, replaceCost ) )
        # if the last entry in the row indicates the optimal cost is less than the
        # maximum cost, and there is a word in this trie node, then add it.
        if node.item and (word[0:index+1] in node.item.name or word[0:index+1].capitalize() in node.item.name): # there
            # seems to be a problem with word not being there while item is. Look into it.

            results.append((node.item, 1.0/(index+1)))
        elif currentRow[-1] <= maxCost and node.word != None:
            results.append( (node.item, currentRow[-1] ) )
        # if any entries in the row are less than the maximum cost, then
        # recursively search each branch of the trie
        if True:#min( currentRow ) <= maxCost:                                                                 # fix this
            for letter in node.children:
                self.searchRecursive( node.children[letter], letter, word, currentRow,
                    results, maxCost, index + 1)

    def traverseInOrder(self, operation, node='head'):
        if node == 'head':
            node = getattr(self, 'head')
        #print node.word
        if operation and node.item:
            operation(node)
        #print node.children
        sortedChildrenKeys = sorted([k for k in node.children])
        for letter in sortedChildrenKeys:
            self.traverseInOrder(operation, node.children[letter])
            '''
            if letter in node.children:
                self.traverseInOrder(operation, node.children[letter])
            elif letter.upper() in node.children:
                self.traverseInOrder(operation, node.children[letter.upper()])
            '''

    def deleteItem(self, word):
        def helper(node, word, ind):
            if ind == len(word):
                if node.word == word:
                    node.word = None
                    node.item = None
                    self.nodeCount -= 1
                    if len(node.children) == 0:
                        return 1
                    else:
                        return 0
                else:
                    return 0
            else:
                if word[ind] in node.children:
                    delete = helper(node.children[word[ind]], word, ind+1)
                    if delete:
                        del node.children[word[ind]]
                        if node.word == None and node.item == None and len(node.children) == 0:
                            return 1
                        else:
                            return 0
        helper(self.head, word, 0)

    def printTree(self, node=None):
        if node==None:
            node = self.head
        if node.word:
            print node.word
        for letter in node.children:
            #print node.children[letter]
            self.printTree(node.children[letter])

'''
start = time.time()
results = search( TARGET, MAX_COST )
end = time.time()

for result in results: print result

print "Search took %g s" % (end - start)
'''