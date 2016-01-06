import sys
import h5py
import json
import web

sys.path.append("..")

urls = (
    # rest API backend endpoints
    "/rest/similarity/(.*)", "similarity",
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
    def GET(self, item_id):
        
        # set up params
        i = web.input(item_id=None)
        params = web.input()

        # assemble list of nodes
        with h5py.File("www/icdar_distances.hdf5", "r") as f:
            # grab the fragment-to-fragment distance Dataset from f
            dist_matrix = f['fragments']
            for 

        
        # dummy example of a request for doc with id "a"
        a = {
            # each node object will be rendered as a circle
            # additional attributes can be added here
            # to expose on the front end like labels, etc.
            # there are no required attributes or naming requirements
            "nodes": [
                {
                    "id": "a"
                },
                {
                    "id": "b"
                },
                {
                    "id": "c"
                },
                {
                    "id": "d"
                }
            ],
            # each link object will be rendered as a line between circles
            # each object must have a key named "source" and one named "target"
            # the source value by default goes by index of the above nodes array
            # but if you want to use the id instead to connect that can work
            # additional attributes can be added to expose on the front end like
            # value could be used to spatially lay out nodes so smaller the value
            # the closer spatially the source and target are in the viz
            "links": [
                {
                    "source": 0,
                    "target": 1,
                    "value": 5
                },
                {
                    "source": 1,
                    "target": 2,
                    "value": 1.2
                }
            ]
        }
        
        # dummy example of a request for author with id "b"
        b = {
            # additional attributes can be added here
            # to expose on the front end like labels, etc.
            # there are no required attributes or naming requirements
            "nodes": [
                {
                    "id": "b"
                },
                {
                    "id": "x"
                },
                {
                    "id": "y"
                },
                {
                    "id": "z"
                }
            ],
            # each link object will be rendered as a transparent line between circle groups
            # each object must have a key named "source" and one named "target"
            # the source value by default goes by index of the above nodes array
            # but if you want to use the id instead to connect that can work
            # additional attributes can be added to expose on the front end like
            # value could be used to spatially lay out node groups so smaller the value
            # the closer spatially the source and target are in the viz
            "links": [
                {
                    "source": 0,
                    "target": 1,
                    "value": 5
                },
                {
                    "source": 1,
                    "target": 2,
                    "value": 1.2
                }
            ]
        }
        
        # use dictionary to return data when param matches
        def getData(item_id):
            return {
                'a': a,
                'b': b
            }[item_id]
        
        # return data object
        return json.dumps(getData(item_id))
    
class classification:
    def GET(self, doc_id):
        
        # set up params
        i = web.input(doc_id=None)
        params = web.input()

        # dummy example of a request for doc with id "a"
        a = {
            "id": "a",
            # no required attributes or naming requirements
            # value could be confidence
            # ideally the best match would be the first object in the array
            "author": [
                {
                    "id": "x",
                    "name": "author1",
                    "value": 5
                },
                {
                    "id": "x",
                    "name": "author2",
                    "value": 4.3
                },
                {
                    "id": "x",
                    "name": "author3",
                    "value": 4.2
                },
                {
                    "id": "x",
                    "name": "author4",
                    "value": 1
                },
                {
                    "id": "x",
                    "name": "author5",
                    "value": 0.8
                }
            ],
            # no required attributes or naming requirements
            # value could be the relatedness value in the entire feature set for this doc
            "features": [
                {
                    "id": "x",
                    "name": "feature1",
                    "value": 10
                },
                {
                    "id": "x",
                    "name": "feature2",
                    "value": 3
                },
                {
                    "id": "x",
                    "name": "feature3",
                    "value": 7.4
                }
            ]
        }
                
        # use dictionary to return data when param matches
        def getData(doc_id):
            return {
                'a': a
            }[doc_id]
        
        
        # return data object
        return json.dumps(getData(doc_id))
    
app = web.application(urls, globals())
    
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
