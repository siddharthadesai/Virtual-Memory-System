# tlb.py
# Siddhartha Desai

class TLB:
	def __init__(self):
		self.tlb = [[0, None, None] for y in range(4)]


	def hit_or_miss(self, sp, w):
		'''Calls hit method if sp matches, otherwise return None'''
		index = self._search_for_match_sp(sp)
		#print("SP: ", sp)
		return self._hit(index[0], w) if index else None


	def _hit(self, index, w):
		# PA = f + w
		PA = self.tlb[index][2] + w

		# Decrement all LRU values greater than LRU[k] by 1
		for i in range(4):
			if self.tlb[i][0] > self.tlb[index][0]:
				self.tlb[i][0] -= 1

		# Set LRU[k] = 3
		self.tlb[index][0] = 3

		return PA


	def _search_for_match_sp(self, sp):
		'''Looks through the sp column of the tlb and finds if there is a match.
		   If there is, return the index'''
		return [i for i in range(4) if self.tlb[i][1] == sp]


	def update(self, sp, new_f):
		# Find line with LRU = 0, and set it to 3
		index = self._search_for_match_lru(0)
		if index:
			index = index[0]
		else:
			index = self._search_for_open_spot()[0]

		self.tlb[index][0] = 3

		# Replace sp and f field
		self.tlb[index][1] = sp
		self.tlb[index][2] = new_f

		# Decrement all other LRU values by 1
		for i in range(4):
			if i != index:
				self.tlb[i][0] -= 1


	def _search_for_match_lru(self, lru):
		'''Looks through the LRU column of the tlb and finds the index with 0'''
		return [i for i in range(4) if self.tlb[i][0] == lru]

	def _search_for_open_spot(self):
		'''Looks through the LRU column of the tlb and finds the index less than 0'''
		return [i for i in range(4) if self.tlb[i][0] < 0]


	def add_entry(self, index, lru, sp, f):
		self.tlb[index][0] = lru
		self.tlb[index][1] = sp
		self.tlb[index][2] = f


	def print_tlb(self):
		print()
		for i in self.tlb:
			print(i)



		