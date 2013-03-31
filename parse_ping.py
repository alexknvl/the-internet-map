from __future__ import division
import re

reLine = re.compile(
r"""
Reply \s from \s (?P<ip>\d+\.\d+\.\d+\.\d+): \s bytes=(?P<bytes>\d+) \s time=(?P<timeout>\d+)ms \s TTL=(?P<ttl>\d+)
.*?""", re.VERBOSE)

def parsePingOutputLine(line):
  """
  >>> parsePingOutputLine("Reply from 188.123.255.38: bytes=32 time=10ms TTL=253")
  ('188.123.255.38', '32', '10', '253')
  """
  
  match = reLine.match(line)
  
  if match:
    return match.groups()
  else:
    return ()
    
if __name__ == "__main__":
  import doctest
  doctest.testmod()

  result = {}
  total = 0
  
  f = open("188.123.255.38.ping.log")
  for line in f:
    l = parsePingOutputLine(line)
    
    if l != ():
      timeout = int(l[2])
      
      if timeout not in result:
        result[timeout] = 0
      
      result[timeout] += 1
      total += 1
  f.close()
  
  for k,v in result.iteritems():
    print "%s\t%s" % (k, v / total)