# bitmap.py
# Siddhartha Desai

class Bitmap:	
	def __init__(self):
		self.MASK = self.create_mask()
		self.BM = [0] * 32

		# Set first bit of first int to 1
		self.allocate_page(0, 0)


	def create_mask(self):
		'''Dynamically create a mask'''
		MASK = [1]
		for i in range(32):
			MASK.insert(0, MASK[0] << 1)
		return MASK


	def extract_segment(self, VA, start, end):
		for i in range(start, end+1):
			VA = VA & ~self.MASK[i]
		return VA


	def next_available_page_table(self):
		flag = 0
		for i in range(0, 32):
			for j in range(0, 32):
				test = self.BM[i] & self.MASK[j]
				if (test == 0):
					if flag == 0:
						flag += 1
					else:
						if j == 0:
							j, i = 31, i-1
						else:
							j -= 1
						return (i, j) # bit j of BM[i] is 0
				else:
					flag = 0
		return None


	def next_available_page(self):
		for i in range(0, 32):
			for j in range(0, 32):
				test = self.BM[i] & self.MASK[j]
				if (test == 0):
					return (i, j) # bit j of BM[i] is 0
		return None


	def allocate_page_table(self, i, j):
		'''Allocates a page table (takes up 2 frames)'''
		self.BM[i] = self.BM[i] | self.MASK[j]
		if (j == 31):
			i, j = i+1, 0
		else:
			j += 1
		self.BM[i] = self.BM[i] | self.MASK[j]


	def allocate_page(self, i, j):
		'''Allocates a frame (takes up 1 frame)'''
		self.BM[i] = self.BM[i] | self.MASK[j]

