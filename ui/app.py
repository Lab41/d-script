import sys
import h5py
import json
import operator
import web


sys.path.append("..")
import feat_analysis.adjmats as adjmats

urls = (
    # rest API backend endpoints
    "/rest/similarity/(author|fragment)/(.*)", "similarity",
    "/rest/classification/(.*)", "classification",
    # front-end routes to load angular app
    "/(.*)", "www",
    "/#(.*)", "index",
    "/", "index"
)
    
class www:
    def GET(self, filename):
        try:
            f = open('www/' + filename)
            return f.read() # or return f.read() if you're using 0.3
        except IOError: # No file named that
            web.notfound()
            
class index:
    def GET(self, filename):
        try:
            f = open("www/index.html")
            return f.read()
        except IOError:
            web.notfound()

class similarity:
    def GET(self, mode, item_id):
        
        # set up params
        i = web.input(item_id=None)
        params = web.input()

        # assemble list of nodes
        with h5py.File("www/icdar_distances.hdf5", "r") as f:
            # grab the fragment-to-fragment distance Dataset from f
            if mode == "fragment":
                dist_matrix = f['fragments']['metrics']
                # lookup and reverse lookup operations for fragments
                get_full_id = adjmats.get_full_id
                reverse_full_id = adjmats.reverse_full_id
                get_author = adjmats.get_author
            elif mode == "author":
                dist_matrix = f['authors']['metrics']
                # lookup and reverse lookup for authors
                # is simpler, provided continuous & zero-based labeling
                get_full_id = lambda x: "{0:03}".format(x)
                # id retrieval is just an int cast 
                reverse_full_id = int

            nodes = [] 
            for i in xrange(dist_matrix.shape[0]):
                nodes.append({"id": get_full_id(i)})
            
            # if we are doing a query on an item, also retrieve the K nearest neighbors
            # and create link objects for those
            links = []
            if item_id is not None and item_id != "":
                item_index = adjmats.reverse_full_id(item_id)
                num_nearest = 5
                nearest_indices = np.argsort(dist_matrix[item_index,:])[:num_nearest]
                #TODO: could also get links between neighbors?
                if mode=='fragment':
                    # mark nodes from same author
                    self_author = int(get_author(item_index))
                    self_author_node_indices = range(self_author*4, 4)
                    for i in self_author_node_indices:
                        nodes[i]['same_author'] = True
                    
                    
                for neighbor_index in nearest_indices:
                    neighbor_distance = dist_matrix[item_index, neighbor_index]
                    links.append({
                        "source": item_index,
                        "dest": neighbor_index,
                        "value": neighbor_distance
                    })
            response = { "nodes": nodes, "links": links }

        # return data object
        return json.dumps(response)
    
class classification:
    def GET(self, doc_id):
        
        # set up params
        i = web.input(doc_id=None)
        params = web.input()


        # retrieve features for document
        hstep = 20
        vstep = 20
        stdev_threshold=0.2
        num_shingles=100
        doc_feats = class_icdar_iterator.fielify_doc_by_id(doc_id, return_mean=False,
            hstep=hstep, vstep=vstep, stdev_threshold=stdev_threshold, 
            num_shingles=num_shingles)
        # run classifier
        author_probs = foo.get_author_probabilities(doc_feats)
        # get correct author
        correct_author = foo.lookup_author(doc_id)

        # get top K authors
        num_authors = 5
        author_limit = min(num_authors, len(author_probs))
        probability_cutoff = np.sort([ -prob for prob in author_probs.itervalues() ])[num_authors]
        authors_list = [ {"id": author, "value": prob} for author, prob in author_probs.iteritems() 
            if prob > probability_cutoff ]
        authors_list = sorted(authors_list, key=operator.itemgetter("value"), reverse=True)
        result = {
            "id": doc_id,
            "author_id" : correct_author,
            "authors": authors_list }
        
        # return data object
        return json.dumps(result)
    
app = web.application(urls, globals())
    
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
