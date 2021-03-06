__author__ = 'Tianyu Dai (dtysky)'

from PIL import Image
import os, json
from ctypes import *
user32 = windll.LoadLibrary('user32.dll')
MessageBox = lambda x:user32.MessageBoxA(0, x, 'Error', 0) 

FileFormat = ['.jpg', '.bmp']
Conf = json.load(open('../ImageForTest/conf.json', 'r'))['conf']

def show_error(e):
	MessageBox(e)
	exit(0)

def name_format(root, name, ex, conf):
	return '%s-%sx%s' % (name, conf['xoffset'], conf['yoffset'])

def conf_format(im, conf):
	size = len(bin(max(im.size) - 1)) - 2
	offset = (conf['xoffset'], conf['yoffset'])
	res = ''
	for p in offset:
		r = [bin(int(p)).split('0b').pop()]
		r.insert(0, '1' if p < 0 else '0')
		for i in xrange(size - len(r[1])):
			r[1] = '0' + r[1]
		res += r[0] + r[1] + '\n'
	return '%s\n%s' % (im.mode, res)

def color_format(mode, color):
	if mode != 'RGB':
		color = [color]
	res = ''
	for c in color:
		tmp = bin(c)[2:]
		for i in xrange(10 - len(bin(c))):
			tmp = '0' + tmp
		res += tmp
	return res

def count_format(size, count):
	res = bin(count)[2:]
	for i in xrange(len(bin(size)) - len(bin(count))):
		res = '0' + res
	return res

def create_dat(im, conf):
	mode = im.mode
	if mode not in ['RGB', 'L']:
		show_error('Simulations for this module just supports RGB and Gray-scale images, check your images !')
	if im.size != (512, 512):
		show_error('Simulations for this module just supports 512x512 images, check your images !')
	data_src = im.getdata()
	data_res = ''
	for y in xrange(ysize):
		for x in xrange(xsize):
			data_res += count_format(xsize - 1, xsize - 1 - x) + '\n'
			data_res += count_format(ysize - 1, ysize - 1 - y) + '\n'
			data_res += color_format(mode, data_src[(ysize - 1 - y) * xsize + (xsize - 1 - x)]) + '\n'
	return data_res[:-1]

FileAll = []
for root,dirs,files in os.walk('../ImageForTest'):
    for f in files:
    	name, ex=os.path.splitext(f)
        if ex in FileFormat:
        	FileAll.append((root+'/', name, ex))
dat_index = ''
for root, name, ex in FileAll:
	im_src = Image.open(root + name + ex)
	xsize, ysize = im_src.size
	for c in Conf:
		dat_res = open('../FunSimForHDL/%s.dat' \
			% name_format(root, name, ex, c), 'w')
		dat_res.write('%d\n%d\n' % (xsize, ysize))
		dat_res.write('%s' % conf_format(im_src, c))
		dat_res.write(create_dat(im_src, c))
		dat_index += '%s' % name_format(root, name, ex, c)
		dat_index += '\n'
		dat_res.close()
dat_index = dat_index[:-1]
dat_index_f = open('../FunSimForHDL/imgindex.dat','w')
dat_index_f.write(dat_index)
dat_index_f.close()