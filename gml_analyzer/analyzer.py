from tag import Tag
from stroke import Stroke
import glob
import os

os.chdir("/Users/max/Code/src/gml_analyzer_1_formax/data")

tags = set()

for filename in glob.glob("*.gml"):
  gml = open(filename, "r").read()
  tag = Tag.fromGML(gml)
  tag.filename = filename
  
  tags.add(tag)
  
print "-- finished loading tags --"

for tag in tags:
  tag.flattened_stroke().self_intersection_count

print len(tags)