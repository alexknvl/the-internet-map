import re

reLine = re.compile(
r"""\s+
(?P<n>\d+)\s+
(?P<p1> \d+ \s ms | \*)\s+
(?P<p2> \d+ \s ms | \*)\s+
(?P<p3> \d+ \s ms | \*)\s+
(?P<ip>\d+\.\d+\.\d+.\d+ | Request\stimed\sout\. | \S+ \s+ \[\d+\.\d+\.\d+.\d+\]) 
.*?""", re.VERBOSE)

reIp = re.compile(r"(\d+\.\d+\.\d+.\d+).*?", re.VERBOSE)
reHostAndIp = re.compile(r"(?P<host>\S+) \s+ \[(?P<ip>\d+\.\d+\.\d+.\d+)\].*?", re.VERBOSE)
reRequestTimedOut = re.compile(r"Request\stimed\sout\. .*?", re.VERBOSE)

def parseTracertOutputLine(line):
  """
  >>> parseTracertOutputLine(" 13   143 ms   153 ms   147 ms  la-in-f113.1e100.net [74.125.143.113]")
  ('13', '143', '153', '147', '74.125.143.113')
  
  >>> parseTracertOutputLine(" 12     *        *        *     Request timed out.")
  ('12', '*', '*', '*', '*')
  
  >>> parseTracertOutputLine("  1   210 ms   211 ms   206 ms  172.24.160.1")
  ('1', '210', '211', '206', '172.24.160.1')
  
  >>> parseTracertOutputLine("  2   192 ms     *      314 ms  10.244.2.98")
  ('2', '192', '*', '314', '10.244.2.98')
  
  >>> parseTracertOutputLine("over a maximum of 30 hops:")
  ()
  """
  
  match = reLine.match(line)
  if match:
    n, p1, p2, p3, ip = match.groups()
    
    def parseTimeout(t):
      if t == '*':
        return '*'
      else: 
        return t.partition(' ')[0]
    
    p1 = parseTimeout(p1)
    p2 = parseTimeout(p2)
    p3 = parseTimeout(p3)
        
    match = reRequestTimedOut.match(ip)
    if match:
      ip = "*"
      return (n, p1, p2, p3, ip)
      
    match = reHostAndIp.match(ip)
    if match:
      ip = match.group("ip")
      return (n, p1, p2, p3, ip)
    
    return (n, p1, p2, p3, ip)
  
  return ()

def parseTracertOutput(output):
  result = []

  for line in output.splitlines():
    l = parseTracertOutputLine(line)
    if l != ():
      result.append(l)
  
  return result

def runTraceroute(hosts, maxHops, maxTimeout):
  import subprocess
  from time import sleep

  processes = []
  
  for h in hosts:
    p = subprocess.Popen("tracert -h %s -w %s %s" % (maxHops, maxTimeout, h), stdout=subprocess.PIPE)
    processes.append(p)
    sleep(0.05)
  
  return zip(hosts, [parseTracertOutput(p.stdout.read()) for p in processes])

import itertools
def pairwise(iterable):
  "s -> (s0,s1), (s1,s2), (s2, s3), ..."
  a, b = itertools.tee(iterable)
  next(b, None)
  return itertools.izip(a, b)

from random import randrange
 
def generateIP():
    blockOne = randrange(0, 255, 1)
    blockTwo = randrange(0, 255, 1)
    blockThree = randrange(0, 255, 1)
    blockFour = randrange(0, 255, 1)
    print 'Random IP: ' + str(blockOne) + '.' + str(blockTwo) + '.' + str(blockThree) + '.' + str(blockFour)
    return str(blockOne) + '.' + str(blockTwo) + '.' + str(blockThree) + '.' + str(blockFour)  
  
if __name__ == "__main__":
  import doctest
  doctest.testmod()
  
  f = open('out.csv', "a+")
  
  maxHops = 30
  maxTimeout = 500
  
  while True:
    out = runTraceroute([generateIP() for _ in range(100)], maxHops, maxTimeout)
    for host, route in out:
      route = filter(lambda p: p[4] != '*', route)
      for p1, p2 in pairwise(route):
        f.write("%s\t%s\n" % (p1[4], p2[4]))
        #f.write("%s\t%s\n" % (p2[4], p1[4]))
    f.flush()
  f.close()