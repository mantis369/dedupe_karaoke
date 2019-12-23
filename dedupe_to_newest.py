from os import fdopen, open, unlink, walk
from os import O_BINARY, O_RDONLY, O_NOINHERIT
from os.path import getmtime, join
from hashlib import md5
from time import ctime

base = "D:\\"
delete_non_matches = True
extensions = [".mp3", ".mcg", ".mp4"] #karaoke files

class InvalidFile(Exception):
	pass
invalidfile = InvalidFile()

dupes = []
all_files = {}
for root, dirs, files in walk(base, topdown=True):
	for fn in files:
		try:
			goodfile = False
			for x in extensions:
				if fn.endswith(x):
					goodfile = True
					break
			if not goodfile:
				raise invalidfile
		except InvalidFile:
			continue
		if fn in all_files:
			dupes.append([fn, join(root, fn), all_files[fn]])
		all_files[fn] = join(root, fn)
print ("Found", len(dupes), "duplicate files.")
	
def md5sum(fn):
	#based on https://www.programcreek.com/python/example/157/hashlib.md5
	global delete_non_matches
	if delete_non_matches:
		return "foo"
		
	try:
		fd = open(fn, O_BINARY | O_RDONLY | O_NOINHERIT)
	except OSError:
		raise IOError("Cannot read from", fn)
	f = fdopen(fd, "rb")
	m = md5()
	try:
		while fn:
			fn = f.read(200000)
			m.update(fn)
	finally:
		f.close()
	return m.digest()
	
if delete_non_matches:
	print("WARNING: we are deleting files whose MD5 sums do not match!")

deletion_count = 0
for d in dupes:
	fn, left, right = d
	lsum = md5sum(left)
	rsum = md5sum(right)
	if lsum == rsum:
		try:
			ltime = ctime(getmtime(left))
			rtime = ctime(getmtime(right))
			if ltime >= rtime:
				unlink(right)
			else:
				unlink(left)
			deletion_count += 1
		except:
			print("Unable to work with file", fn)

print("Deleted", deletion_count, "duplicate files.")