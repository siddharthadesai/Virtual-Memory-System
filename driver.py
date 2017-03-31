# driver.py
# Siddhartha Desai

from vm import *

if __name__ == '__main__':
	init_file = open('file_name_1'', 'r')
	va_file = open('file_name_2', 'r')
    
	output_file = open('', 'w')

	ST_entries = init_file.readline().split()
	PT_entries = init_file.readline().split()
	VA_entries = va_file.readline().split()

	VM = VM(ST_entries, PT_entries, VA_entries)
	VM.run(output_file)

	init_file.close()
	va_file.close()
	output_file.close()
