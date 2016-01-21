import sys
import h5py
import json
import operator
import web

import numpy as np

sys.path.append("..")

urls = (
    # rest API backend endpoints
    "/rest/static/(.*)", "static_data",
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
        def get_author_id(i):
            author_id = 1 + (i / 4)
            return author_id

        def get_fragment_id(i):
            file_id = 1 + (i % 4)
            return file_id

        def get_full_id(i):
            full_id = "{0:03}_{1}".format(get_author_id(i), get_fragment_id(i))
            return full_id

        def reverse_full_id(full_id):
            author_id, file_id = full_id.split(".")[0].split("_")
            author_int = int(author_id)
            file_int = int(file_id)
            return 4*(author_int - 1) + (file_int - 1)
        
        # set up params
        i = web.input(item_id=None)
        params = web.input()

        # assemble list of nodes
        # grab the fragment-to-fragment distance Dataset from f
        if mode == "fragment":
            with h5py.File("data/icdar_fragments_distances.hdf5", "r") as f:
                dist_matrix = f['metrics'].value
        elif mode == "author":
            with h5py.File("data/icdar_authors_distances.hdf5", "r") as f:
                dist_matrix = f['metrics'].value
            # ID lookup and reverse lookup for authors
            # are simpler, provided continuous & zero-based labeling
            get_full_id = lambda x: "{0:03}".format(x+1)
            reverse_full_id = lambda x: int(x) - 1

        nodes = [] 
        for i in xrange(dist_matrix.shape[0]):
            node_full_id = get_full_id(i)
            nodes.append({"id": node_full_id})

        # if we are doing a query on an item, also retrieve the K nearest neighbors
        # and create link objects for those
        links = []
        if item_id is not None and item_id != "":
            item_index = reverse_full_id(item_id)
            num_nearest = 5
            nearest_indices = np.argsort(dist_matrix[item_index,:])[1:(num_nearest+1)]
            cutoff_distance = dist_matrix[item_index,nearest_indices[num_nearest-1]]

            # make node objects
            if mode=='fragment':
                # mark nodes from same author
                self_author = int(get_author_id(item_index)) - 1
                self_author_node_indices = range(self_author*4, 4)
                for i in self_author_node_indices:
                    nodes[i]['same_author'] = True

            # make link objects    
            for neighbor_index in nearest_indices:
                # add edges to query node
                neighbor_distance = dist_matrix[item_index, neighbor_index]
                links.append({
                    "source": str(item_index),
                    "target": str(neighbor_index),
                    "value": str(neighbor_distance)
                })
                # add edges between successive neighbors if close enough
                for neighbor_2_index in nearest_indices:
                    if neighbor_2_index > neighbor_index:
                        neighbor_distance = dist_matrix[neighbor_index, neighbor_2_index]
                        if neighbor_distance < cutoff_distance:
                            links.append({
                                "source": str(neighbor_index),
                                "target": str(neighbor_2_index),
                                "value": str(neighbor_distance)
                            })
            response = { "nodes": nodes, "links": links }

        # return data object
        return json.dumps(response)
    
class classification:
    def GET(self, doc_id):
        
        # set up params
        i = web.input(doc_id=None)
        params = web.input()

        feats_path = "data/fiel_feat_icdar13_100shingles.hdf5"
        model_path = None

        # get correct author (HACK)
        correct_author_id = doc_id.split("_")[0]

        # retrieve features (a lookup, for now)
        with h5py.File(feats_path) as f:
            doc_feats = f[correct_author_id][doc_id + ".tif"].value
            # take mean over shingles
            doc_feats = np.mean(doc_feats, axis=0)
        
        # run classifier
        author_probs = foo.authorProbs(model_path, doc_feats)
        
        # get top K authors
        num_authors = 5
        author_limit = min(num_authors, len(author_probs))
        probability_cutoff = np.sort([-prob for prob in author_probs.itervalues()])[num_authors]
        authors_list = [ {"id": author, "value": prob} for author, prob in author_probs.iteritems() 
            if prob > probability_cutoff ]
        
        # sort by probability
        authors_list = sorted(authors_list, key=operator.itemgetter("value"), reverse=True)
        result = {
            "id": doc_id,
            "author_id" : correct_author_id,
            "authors": authors_list }
        
        # return data object
        return json.dumps(result)

class static_data:
    def GET(self, name):
        
        # set up params
        i = web.input(name=None)
        params = web.input()
        
        try:
            f = open("www/data/" + name + ".json")
            return f.read()
        except IOError:
            web.notfound()
        
app = web.application(urls, globals())
    
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
