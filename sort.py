import random
import sys
import string

bufsize = 1000
minbuf = 50
overlap = 100
totalitems = 100000

class tuplesort:

    tuparray = []
    low = 0
    lastspilled = None
    runs = []
    current_run = []
    nswaps = 0
    nitems = 0

    def checkinvariants(self):
        n = 0
        for run in self.runs:
            n = n + len(run)
        n = n + len(self.current_run)
        n = n + len(self.tuparray)
        if n != self.nitems:
            print "n(%d) != nitems(%d)" % (n, self.nitems)
            exit()

    def input(self, value):
#        print "input: %f" % value
#        print "bufsize=%d" % len(self.tuparray)
        if len(self.tuparray) >= bufsize:
            self.spillarray()
#        print "bufsize=%d" % len(self.tuparray)
        self.tuparray.append(value)
        self.nitems = self.nitems + 1
        #self.checkinvariants()
        return

    def finish(self):
        self.spillarray(force=True)
        self.new_run()
        if len(self.tuparray) > 0:
            self.spillarray(force=True)
            self.new_run()

    def spillarray(self, force = False):
        high = len(self.tuparray) - 1

        if self.lastspilled != None:
            self.low = self.pivot(self.lastspilled, self.low, high) + 1

#        if (self.low > 0):
#            print "residue (self.lastspilled=%f):" % self.lastspilled
#            print self.tuparray[0:self.low]
#        print "spillable:"
#        print self.tuparray[self.low:]

        m = high - overlap
        if m - self.low < minbuf:
            m = self.low + minbuf
        if force or m > high:
            m = high
#        print "spilling %d..%d" % (self.low, m)
        self.qsort(self.low, high, m)

#        print "spilling:"
#        print self.tuparray[self.low:m+1]

        self.current_run.extend(self.tuparray[self.low:m+1])
        self.tuparray[self.low:m+1] = []
        self.lastspilled = self.current_run[-1]
        if self.low > bufsize-minbuf:
            self.new_run()
#        print "self.lastspilled = %f tuparray:" % self.lastspilled
#        print self.tuparray

    def new_run(self):
#        print "starting new run"
        self.runs.append(self.current_run)
        self.current_run = []
        self.low = 0
        self.lastspilled = None

    def pivot(self, value, l, h):
        i = l-1
        #print "pivoting on value: %d:" % value
        #print self.tuparray[l:h+1]
        for j in range(l, h+1):
            if self.tuparray[j] <= value:
                i = i + 1
                tmp = self.tuparray[i]
                self.tuparray[i] = self.tuparray[j]
                self.tuparray[j] = tmp
                self.nswaps = self.nswaps + 1
        #print self.tuparray[l:h+1]
        return i

#    def pivot(self, value, l, h):
#        while (h > l):
#            while (h > l and self.tuparray[h] > value):
#                h = h - 1
#            while (h > l and self.tuparray[l] < value):
#                l = l + 1
#            if (h > l):
#                tmp = self.tuparray[l]
#                self.tuparray[l] = self.tuparray[h]
#                self.tuparray[h] = tmp
#                h = h - 1
#        return l
#
#        while (h > l):
#            tmp = self.tuparray[l]
#            if tmp > value:
#                self.tuparray[l] = self.tuparray[h]
#                self.tuparray[h] = tmp
#                h = h - 1
#            else:
#                l = l + 1
#        if self.tuparray[l] > value:
#            return l
#        else:
#            return l + 1

    def qsort(self, l, h, m):
        self.qsort_worker(l, h, m)
        if self.tuparray[l:m+1] != sorted(self.tuparray[l:m+1]):
            print "ARRAY NOT SORTED!"

    def qsort_worker(self, l, h, m):
        if (h - l  < 8):
            self.tuparray[l:h+1] = sorted(self.tuparray[l:h+1])
        elif (h > l):
            k = self.pivot(self.tuparray[h], l, h)
            self.qsort_worker(l, k-1, m)
            if k+1 <= m:
                self.qsort_worker(k+1, h, m)


if __name__ == "__main__":
    actualoverlap = None
    if len(sys.argv) > 1:
        bufsize = int(sys.argv[1])
    if len(sys.argv) > 2:
        totalitems = int(sys.argv[2])
    if len(sys.argv) > 3:
        minbuf = int(sys.argv[3])
    if len(sys.argv) > 4:
        overlap = int(sys.argv[4])
    if len(sys.argv) > 5:
        actualoverlap = int(sys.argv[5])

    if (bufsize <= 8):
        print "bufsize=%d" % bufsize
        exit(1)
    if (totalitems <= 20):
        print "totalitems=%d" % totalitems
        exit(1)
    if (minbuf <= 0 or minbuf > bufsize):
        print "minbuf=%d" % minbuf
        exit(1)
    if (overlap < 0 or overlap >= bufsize):
        print "overlap=%d" % overlap
        exit(1)
    if (actualoverlap != None and actualoverlap < 0):
        print "actualoverlap=%d" % actualoverlap
        exit(1)

#    print "Processing %d tuples, in a %d buffer, reading minimum %d at a time overlapping by %d" % (totalitems, bufsize, minbuf, overlap)

    ts = tuplesort()
    if (actualoverlap == None):
        for i in range(0, totalitems):
            ts.input(random.random())
    else:
        for i in range(0, totalitems):
            ts.input(i + actualoverlap * random.random())
    ts.finish()
    n = 0
    for run in ts.runs:
        n = n + len(run)
        if run != sorted(run):
            print "Run not sorted!"
            print run
    if len(ts.tuparray) > 0:
        print "tuparray still contains %d items!" % len(ts.tuparray)
    if len(ts.current_run) > 0:
        print "current run still contains %d items!" % len(ts.current_run)
    if n != totalitems:
        print "Only have %d items after generating runs!" % n
    #print "Generated %d runs using %d swaps" % (len(ts.runs), ts.nswaps)
    if (actualoverlap == None):
        print "%d,%d,%d,%d,None,%d,%d" % (totalitems,bufsize,minbuf,overlap,len(ts.runs), ts.nswaps)
    else:
        print "%d,%d,%d,%d,%d,%d,%d" % (totalitems,bufsize,minbuf,overlap,actualoverlap,len(ts.runs), ts.nswaps)
