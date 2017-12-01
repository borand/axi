from imposm.parser import OSMParser
from shapely import geometry

class Handler(object):
    def __init__(self, transform=None):
        self.transform = transform
        self.coords = []
        self.nodes = []
        self.ways = []
        self.relations = []
    def on_coords(self, coords):
        self.coords.extend(coords)
    def on_nodes(self, nodes):
        self.nodes.extend(nodes)
    def on_ways(self, ways):
        self.ways.extend(ways)
    def on_relations(self, relations):
        self.relations.extend(relations)
    def transform_point(self, lng, lat):
        if self.transform:
            return self.transform(lng, lat)
        return lng, lat
    def create_geometries(self):
        # create lookup tables
        coords_by_id = {}
        nodes_by_id = {}
        ways_by_id = {}
        relations_by_id = {}
        for osmid, lng, lat in self.coords:
            lng, lat = self.transform_point(lng, lat)
            coords_by_id[osmid] = (lng, lat)
        for osmid, tags, (lng, lat) in self.nodes:
            lng, lat = self.transform_point(lng, lat)
            nodes_by_id[osmid] = (lng, lat, tags)
        for osmid, tags, refs in self.ways:
            ways_by_id[osmid] = (tags, refs)
        for osmid, tags, members in self.relations:
            relations_by_id[osmid] = (tags, members)
            # for refid, reftype, role in members:
            #     pass
        # create geometries
        geoms = []
        for osmid, tags, (lng, lat) in self.nodes:
            lng, lat = self.transform_point(lng, lat)
            g = geometry.Point(lng, lat)
            g.tags = tags
            geoms.append(g)
        for osmid, tags, refs in self.ways:
            coords = [coords_by_id[x] for x in refs]
            closed = refs[0] == refs[-1]
            if 'highway' in tags or 'barrier' in tags:
                closed = False
            if tags.get('area') == 'yes':
                closed = True
            if closed:
                g = geometry.Polygon(coords)
            else:
                g = geometry.LineString(coords)
            g.tags = tags
            geoms.append(g)
        return geoms

def parse(filename, transform=None):
    handler = Handler(transform)
    p = OSMParser(
        concurrency=1,
        coords_callback=handler.on_coords,
        nodes_callback=handler.on_nodes,
        ways_callback=handler.on_ways,
        relations_callback=handler.on_relations)
    p.parse(filename)
    return handler.create_geometries()
