

# a_file = open("C:/Users/admin/Desktop/check.txt", "r")
# list_of_lists = []
# for line in a_file:
#     stripped_line = line.strip()
#     line_list = stripped_line.split()
#     list_of_lists.append(line_list)
#     a_file.close()
#     print(list_of_lists)


a_file = open("C:/Users/admin/Desktop/check.txt", "r")
list_of_lists = [(line.strip()).split() for line in a_file]
#a_file.close()
# print(list_of_lists)

# Python code to flat a nested list with 
# multiple levels of nesting allowed. 

# input list 
# l = [1, 2, [3, 4, [5, 6]], 7, 8, [9, [10]]] 

# output list 
output = [] 

# function used for removing nested 
# lists in python. 
def reemovNestings(list_of_lists): #replce l by list of list
	for i in list_of_lists: 
		if type(i) == list: 
			reemovNestings(i) 
		else: 
			output.append(i) 

# Driver code 
print ('The original list: ', list_of_lists) 
reemovNestings(list_of_lists) 
print ('The list after removing nesting: ', output) 
