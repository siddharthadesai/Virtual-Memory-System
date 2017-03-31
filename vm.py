# VM.py
# Siddhartha Desai

from bitmap import *
from tlb import *

class VMTLB:
	def __init__(self, ST_entries, PT_entries, VA_entries):

		self.PM = [0] * 524288
		self.BM = Bitmap()
		self.TLB = TLB()
		self.VA_entries = VA_entries

		self.initialize_PM(ST_entries, PT_entries)


	def initialize_PM(self, ST, PT):
		for s, f in zip(ST[::2], ST[1::2]):
			s, f = int(s), int(f)
			frame_num = f // 512
			self.PM[s] = f
			if f != -1:
				self.BM.allocate_page_table(frame_num//32, frame_num%32)

		for p, s, f in zip(PT[::3], PT[1::3], PT[2::3]):
			p, s, f = int(p), int(s), int(f)
			frame_num = f // 512
			self.PM[self.PM[s] + p] = f
			self.BM.allocate_page(frame_num//32, frame_num%32)


	def run(self, outfile):
		for o, v in zip(self.VA_entries[::2], self.VA_entries[1::2]):
			outfile.write(self.process_va(int(o), int(v)) + " ")


	def process_va(self, read_write, VA):
		if read_write == 0:
			return self.read_address(VA)
		else:
			return self.write_address(VA)


	def read_address(self, VA):
		sp, w = self.break_address_tlb(VA)
		value = self.TLB.hit_or_miss(sp, w)
		if value is None: # a miss
			s, p, w = self.break_address(VA)
			if self.PM[s] == -1:
				return 'm pf'
			elif self.PM[s] == 0:
				return 'm err'
			elif self.PM[self.PM[s] + p] == -1:
				return 'm pf'
			elif self.PM[self.PM[s] + p] == 0:
				return 'm err'
			else:
				self.TLB.update(sp, self.PM[self.PM[s] + p])
				return 'm ' + str(self.PM[self.PM[s] + p] + w)
		else: # a hit
			return 'h ' + str(value)


	def write_address(self, VA):
		sp, w = self.break_address_tlb(VA)
		value = self.TLB.hit_or_miss(sp, w)
		if value is None: # a miss
			s, p, w = self.break_address(VA)
			if self.PM[s] == -1 or self.PM[self.PM[s] + p] == -1:
				return 'm pf'
			if self.PM[s] == 0:
				# Find next 2 consecutive frames that are available and allocate a new blank PT
				i, j = self.BM.next_available_page_table() # bit j of BM[i] is free
				self.BM.allocate_page_table(i, j)
				# Update the ST
				self.PM[s] = (i*32 + j) * 512 # segment s points to address i*32 + j * 512
			if self.PM[self.PM[s] + p] == 0:
				# Now do the same thing for a page
				i, j = self.BM.next_available_page()
				self.BM.allocate_page(i, j)
				self.PM[self.PM[s] + p] = (i*32 + j) * 512
			self.TLB.update(sp, self.PM[self.PM[s] + p])
			return 'm ' + str(self.PM[self.PM[s] + p] + w)
		else: # a hit
			return 'h ' + str(value)


	def break_address(self, VA):
		s = self.BM.extract_segment(VA, 14, 31)
		s = s >> 19

		p = self.BM.extract_segment(VA, 4, 13)
		p = self.BM.extract_segment(p, 24, 31)
		p = p >> 9

		w = self.BM.extract_segment(VA, 4, 23)

		return (s, p, w)


	def break_address_tlb(self, VA):
		sp = self.BM.extract_segment(VA, 24, 31)
		sp = sp >> 9

		w = self.BM.extract_segment(VA, 4, 23)

		return (sp, w)

