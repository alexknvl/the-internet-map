#!/usr/bin/python2.7

import pygeoip as geoip
from gexf import Gexf

db = geoip.Database('GeoIP.dat')
gexf = Gexf("Alexander Konovalov", "The internet map")
graph = gexf.addGraph("directed", "static", "The internet map")

attrid = graph.addNodeAttribute("country", "??", type="string")
def addIP(ip):
  if not graph.nodeExists(ip):
    info = db.lookup(ip)
    country = "??"
    if info.country:
      country = info.country
    n = graph.addNode(ip, ip)
    n.addAttribute(attrid, country)

n = 0
with open("out.csv") as f:
  for line in f: 
    ips = tuple(line.strip().replace("-", ".").split('\t'))
    if len(ips) < 2:
      continue
    ip1, ip2 = ips
    addIP(ip1)
    addIP(ip2)
    graph.addEdge("%s->%s" % (ip1, ip2), ip1, ip2)
    n += 1
    print n

with open("test.gexf", "w") as f:
  gexf.write(f)
