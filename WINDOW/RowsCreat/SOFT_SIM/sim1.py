__author__ = 'Dai Tianyu (dtysky)'

from PIL import Image
import os

ModuleName='RowsCreat'

FileAll = []

class Rows():
	"""A class for creating and maintaining some row cache, using it to sumulate some fifos."""
	def __init__(self, frame, width, deepth):
		self.creat(frame, width, deepth)
		self.frist_fill()
	def creat(self, frame, width, deepth):
		self.frame = list(frame)
		self.frame.reverse()
		self.width = width
		self.deepth = deepth
	def frist_fill(self):
		self.rows = []
		for y in range(self.width):
			self.rows.append([])
			for x in range(self.deepth):
				self.rows[y].insert(0,self.frame.pop())
	def frame_empty(self):
		return len(self.frame) == 0
	def rows_empty(self):
		return len(self.rows[0]) == 0
	def update(self):
		output = []
		if not self.frame_empty():
			self.rows[0].insert(0,self.frame.pop())
		for i in range(len(self.rows)-1):
			now_pix = self.rows[i].pop()
			self.rows[i+1].insert(0,now_pix)
			output.append(now_pix)
		output.append(self.rows[self.width - 1].pop())
		return output

for root,dirs,files in os.walk('../IMAGE_FOR_TEST'):
    for f in files:
        if os.path.splitext(f)[1]=='.jpg':
        	FileAll.append((root+'/',f))

for root,f in FileAll:
	im_src = Image.open(root+f)
	xsize,ysize = im_src.size
	frame = im_src.getdata()
	width = 5
	deepth = xsize
	rows = Rows(frame, width, deepth)
	fo = open('../SIM_CHECK/dbg' + f + '.dat','w')
	for i in range(len(frame)):
		if rows.frame_empty():
			rows.creat(frame, width, deepth)
		fo.write(str(rows.update()) + '\n')
	fo.close()