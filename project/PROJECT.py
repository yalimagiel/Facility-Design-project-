# written by:
# Oran Zipper - 205709298
# Hila Akry - 205948961
# Yali Natanson - 205925845

# import pickle package

import pickle

# import the data from pickle files

ten_escorts = 'WH_30x70_with_10_escorts.p'
ten_escorts_list = 'WH_30x70_with_10_escorts_items_list.p'
fifty_escorts = 'WH_30x70_with_50_escorts.p'
fifty_escorts_list = 'WH_30x70_with_50_escorts_items_list.p'
one_escorts = 'WH_30x70_with_100_escorts.p'
one_escorts_list = 'WH_30x70_with_100_escorts_items_list.p'

# loading the pickle file of 10 escorts
file_name_ten_escorts=ten_escorts
new_ten_escort = open(file_name_ten_escorts,'rb')
storage_list_ten_escorts = pickle.load(new_ten_escort)
new_ten_escort.close()

file_name_list_ten_escorts=ten_escorts_list
new_list_ten_escorts = open(file_name_list_ten_escorts,'rb')
out_item_list_ten_escorts = pickle.load(new_list_ten_escorts)
new_list_ten_escorts.close()

# loading the pickle file of 50 escorts
file_name_fifty_escorts=fifty_escorts
new_fifty_escort = open(file_name_fifty_escorts,'rb')
storage_list_fifty_escorts = pickle.load(new_fifty_escort)
new_fifty_escort.close()

file_name_list_fifty_escorts=fifty_escorts_list
new_list_fifty_escorts = open(file_name_list_fifty_escorts,'rb')
out_item_list_fifty_escorts = pickle.load(new_list_fifty_escorts)
new_list_fifty_escorts.close()

# loading the pickle file of 100 escorts
file_name_one_escorts=one_escorts
new_one_escort = open(file_name_one_escorts,'rb')
storage_list_one_escorts = pickle.load(new_one_escort)
new_one_escort.close()

file_name_list_one_escorts=one_escorts_list
new_list_one_escorts = open(file_name_list_one_escorts,'rb')
out_item_list_one_escorts = pickle.load(new_list_one_escorts)
new_list_one_escorts.close()

# class for item
class Item:
    def __init__(self,num,location, out = False):
        self.num = num
        self.location_start = location # item's location - (j, i)
        self.dist_I_O = 8000000000000000000000000000 # the distance of the item from IO exit
        self.dist_min_escort = 1000000000 # the distance of the item from the nearest escort
        self.out = out # attribute that contain if we need to take out the item, of we need - it will be True
        # finding which area the item is found and which IO exit is suitable in the same area
        if self.location_start[0]<20:
            self.area = 'a'
            self.item_i_o=(4, 0)
        elif self.location_start[0]>19 and self.location_start[0]<50:
            self.area='b'
            self.item_i_o = (34, 0)
        else:
            self.area='c'
            self.item_i_o = (64, 0)
        self.work = 'free' # as long this attribute is free, it means that the item is not related to other item. if his "out" attribute is True we need to relat him item (escort) that will help him to reach the IO exit
        self.selected_escort = None # contain which class of item (escort) related to the item
        self.route = [] # contain the direction of the next step that will happen
        self.moving=0 # define if the item was moved in one time step, if it was moved - it can't move another step
        self.stage=1 # which stage the item is found:
        # 0 - the item is in IO exit
        # 1 - the item's escort is moving one step at a time toward the item
        # 3 - the item's escort needs to make three steps in three time steps
        # 5 - the item's escort needs to make five steps in five time steps
        self.next_step=None # contain object from type item of the next step that will happen - only for the first step of the item


# class for storage
class Storage:
    def __init__(self, list_storage,list_out_items):
        self.list_storage = list_storage # list that describes the location of the starting items in the storage according to the given data file
        self.list_out_items = list_out_items # list that describes which items we need to take out
        # creating list of class item of all the items that are in the storage
        self.list_of_items = []
        for col in range(len(list_storage)):
            for row in range(len(list_storage[0])):
                if list_storage[col][row] in list_out_items:
                    self.list_of_items.append(Item(list_storage[col][row], (row, col), True))
                else:
                    self.list_of_items.append(Item(list_storage[col][row], (row, col)))
        # define the IO exit points
        self.i_o_A = (4, 0)
        self.i_o_B = (34, 0)
        self.i_o_C = (64, 0)
        self.step_list = [] # list that contain all steps that done in the same time step
        self.time_step = 1 # initialize the time step to be 1
        self.final_list = [] # cumulative list of the steps that has taken and in which time step it was
        # initialize the amount of escort in every area
        self.escort_A = 0
        self.escort_B = 0
        self.escort_C = 0
        # list of every area that contain the items that we neet to take out. the len of the list will be as the number of free escorts
        self.list_active_A = []
        self.list_active_B = []
        self.list_active_C = []
        self.list_need_to_go = [] # list that contains all the items in a particular time step that other item (escort) is making step toward him to get him closer to IO exit
        self.final_out_list = [] # list that contains to every item that we took it out, in which time step it happened


# function checking if the item needs to get out and it is free, if it does -
# sending the item to function that calculate the distance between the item and its IO exit
    def which_dist_from_I_O(self):
        for item in self.list_of_items:
            if item.out==True and item.work=='free': # checking if the item needs to get out and it is free (doen't have related to escort)
                # according to the area that item is found, sending the item with its IO exit to function that calculate the distance between them
                if item.area=='a':
                    item.dist_I_O = self.dist_from_I_O(item,self.i_o_A)
                elif item.area=='b':
                    item.dist_I_O = self.dist_from_I_O(item,self.i_o_B)
                else:
                    item.dist_I_O = self.dist_from_I_O(item,self.i_o_C)


# function that checking every item - if it is in the IO exit location and it needs to get out - if it does -
# chaging its stage to 0
# appending the item to the list that contain the items that needs to get out
    def exit_item(self):
        for item in self.list_of_items:
            if item.out==True and item.dist_I_O==0:
                item.stage=0
                self.list_need_to_go.append(item)

# function that acutally makes the step, taking out the item that need to be out
# moreover, the function adding the step to the step list
# chekcing if there is more item of the same number that need to be get out -
# if does - the function only changes the attributes of the specific item that got out
# if not - the function changes all item's attributes with the same number
    def exit(self,item):
        # adding the step to the step list
        self.step_list.append([[item.location_start[0], item.location_start[1], item.num],
                               [item.location_start[0], item.location_start[1], 0]])
        self.final_out_list.append([item.num, self.time_step])
        # changing the attribute of the specific item that went out
        item.out=False
        self.list_out_items.remove(item.num)  # removing the item that we took out
        if item.num not in self.list_out_items: # chekcing if there is more item of the same number that need to be get out
            for x in self.list_of_items:
                if x.num == item.num:
                    if x in self.list_need_to_go:
                        self.list_need_to_go.remove(x) # removing the number from the list need to go, since we don't need to take out this number
                    # changing the attribute of the all items with the same number
                    x.out = False
                    x.work = 'free'
                    if x.selected_escort!=None:
                        x.selected_escort.work = 'free'
                        x.selected_escort=None
        item.num = 0  # changin to the item to escort
        item.work = 'free'
        if item.selected_escort!=None:
            item.selected_escort.work = 'free'
        item.selected_escort = None



# function that calculate the number of free escorts
    def count_escort(self):
        # initialize the amount of free escorts to each area
        a=0
        b=0
        c=0
        for item in self.list_of_items:
            if item.num == 0 and item.work=='free': # checking if the item is escort and if it is free
                # if it does - adding the escort to the amount of the proper area amount
                if item.area=='a':
                    a+=1
                elif item.area=='b':
                    b+=1
                else:
                    c+=1
        self.escort_A=a
        self.escort_B=b
        self.escort_C=c



# same number of min dist item from I/O as number of escort
    def finding_min(self):
        # list for every area that contain the items that need to get out, that they are no in IO exit location and that they are free (don't related yet to an escort)
        area_A = []
        area_B = []
        area_C = []
        for item in self.list_of_items:
            if item.work=='free' and item.out==True and item.dist_I_O!=0: # checking if the items need to get out, that they are no in IO exit location and that they are free (don't related yet to an escort)
                if item.area=='a':
                    area_A.append(item)
                elif item.area=='b':
                    area_B.append(item)
                else:
                    area_C.append(item)
        # sorting every list by the distance between item and its IO exit (from the smallest to the biggest)
        A_sort=sorted(area_A,key=lambda item:item.dist_I_O)
        B_sort=sorted(area_B,key=lambda item:item.dist_I_O)
        C_sort=sorted(area_C,key=lambda item:item.dist_I_O)
        # checking if the number of free escorts in every area is bigger than the number of items that needs to get out -
        # if the number of free escorts is smaller than the number of items that needs to get out -
        # create a list , with the same len of the number of free escorts, that contain the items that needs to get out, in order from the smallest distance form its IO exit to the biggest
        # if  the number of free escorts is bigger than the number of items that needs to get out -
        # create the same list , but with the same len of the number of the items that needs to get out
        if self.escort_A<=len(A_sort):
            for i in range(self.escort_A):
                self.list_active_A.append(A_sort[i])
        if self.escort_A>len(A_sort):
            for i in range(len(A_sort)):
                self.list_active_A.append(A_sort[i])
        if self.escort_B <= len(B_sort):
            for j in range (self.escort_B):
                self.list_active_B.append(B_sort[j])
        if self.escort_B>len(B_sort):
            for i in range(len(B_sort)):
                self.list_active_B.append(B_sort[i])
        if self.escort_C <= len(C_sort):
            for k in range (self.escort_C):
                self.list_active_C.append(C_sort[k])
        if self.escort_C>len(C_sort):
            for i in range(len(C_sort)):
                self.list_active_C.append(C_sort[i])
        total_list=[]
        # combine between the lists of every area to one big list
        total_list.extend(self.list_active_A)
        total_list.extend(self.list_active_B)
        total_list.extend(self.list_active_C)
        self.list_active_A=[]
        self.list_active_B=[]
        self.list_active_C=[]
        self.finding_close_escort(total_list) # sending the unit list to function that will help to find the closest escort to each item in the list



# function that helps to find the next step for the escort, to bring it near to the item - one step at a time
    def match(self, select_item):
        select_item.stage=1
        # checking if i>=j to find out where the target needs to be next to the item
        if select_item.location_start[1]>=select_item.location_start[0]:
            if select_item.location_start==(0,0): # checking if the item is in (0,0)
                target = (select_item.location_start[0]+1, select_item.location_start[1]) # the target will be on the same line of the item, and on right side
            else:
                target=(select_item.location_start[0],select_item.location_start[1]-1) # in any other case, when i>=j, the target will be under the item
        else: # i<j
            if select_item.location_start[0]<select_item.item_i_o[0]: # if the IO exit is on left the item
                target = (select_item.location_start[0] + 1, select_item.location_start[1]) # the target will be on the right of item
            elif select_item.location_start[0]>select_item.item_i_o[0]: # if the IO exit is on right the item
                target = (select_item.location_start[0] - 1, select_item.location_start[1]) # the target will be on the left of item
            else: # if the item is in the same column of the IO exit
                target = (select_item.location_start[0], select_item.location_start[1] - 1) # he target will be under the item

        escort=select_item.selected_escort
        # three option that the escort is locatied next to the item, like it was already been switch between them - therefor, the escort doesn't get a new next step
        if escort.location_start[0]==select_item.location_start[0] and escort.location_start[0]==target[0] and escort.location_start[1]-1==select_item.location_start[1] and escort.location_start[1]-2==target[1]:
            escort.route = []
        elif escort.location_start[1]==select_item.location_start[1] and escort.location_start[1]==target[1] and escort.location_start[0]-1==select_item.location_start[0] and escort.location_start[0]-2==target[0]:
            escort.route = []
        elif escort.location_start[1]==select_item.location_start[1] and escort.location_start[1]==target[1] and escort.location_start[0]+1==select_item.location_start[0] and escort.location_start[0]+2==target[0]:
            escort.route = []
        else: # in case the escort didn't reach the target, and it isn't one of the three option from top
            if escort.location_start[0]<target[0]: # if the escort is on the left of the target
                # if the next step of the escort is the item's location, the escort won't make this step and will search different step to make
                # if the next step is not the item's location, the next step that the escort will have to do is right
                if escort.location_start[0]+1==select_item.location_start[0] and escort.location_start[1]==select_item.location_start[1]:
                    None
                else:
                    escort.route=['right']
            elif escort.location_start[0]>target[0]: # if the escort is on the right of the target
                # if the next step of the escort is the item's location, the escort won't make this step and will search different step to make
                # if the next step is not the item's location, the next step that the escort will have to do is left
                if escort.location_start[0]-1==select_item.location_start[0] and escort.location_start[1]==select_item.location_start[1]:
                    None
                else:
                    escort.route=['left']
            elif escort.location_start[0]==target[0]: # if the escort is in the sae column of the target
                # if the escort is under the target, its next step will be up
                # if the escort is above the targer, its next step will be down
                if escort.location_start[1]<target[1]:
                    escort.route=['up']
                elif escort.location_start[1]>target[1]:
                    escort.route=['down']
            elif escort.location_start[1]<target[1]: # if the escort is under the target , its next step will be up
                escort.route=['up']
            elif escort.location_start[1]>target[1]: # if the escort is above the target , its next step will be down
                escort.route=['down']
        if target==escort.location_start: # if the escort's location is the same of the target's location, it's time to do switch between the escort and the item
            select_item.stage = 3 # since the next step will be switch, after the next step the escort will be ready to do the threesomes steps
            # if the escort is under the item, the next step will be up
            # if the escort is left the item, the next step will be right
            # if the escort is right the item, the next step will be left
            if select_item.location_start[0]==escort.location_start[0] and select_item.location_start[1]-1==escort.location_start[1]:
                escort.route=['up']
            elif (select_item.location_start[0]-1)==escort.location_start[0] and select_item.location_start[1]==escort.location_start[1]:
                escort.route=['right']
            elif (select_item.location_start[0]+1)==escort.location_start[0] and select_item.location_start[1]==escort.location_start[1]:
                escort.route=['left']
        if escort.route==[]: # if the escort doesn't have next step
            # if the escort, the item and the IO exit are on the same column or on the 0'st row - the escort needs to do fifths steps
            if (escort.location_start[0]==select_item.item_i_o[0] and select_item.location_start[0]==select_item.item_i_o[0]) or  (escort.location_start[1]==select_item.item_i_o[1] and select_item.location_start[1]==select_item.item_i_o[1]):
                select_item.stage=5
            else: #the escort needs to do threesomes steps
                select_item.stage = 3
        if select_item.location_start==select_item.item_i_o: # if the item is already reached the IO exit, its stage will change to 0 and the next step will get him out
            select_item.stage = 0



# function that help finding the closet escort to every item that is in the list
# to every item that sending to this function, there is no possible way that the function won't find him an escort
    def finding_close_escort(self, list_min_value):
        i = 0 # helps us to find if the escort is in the same area of the item or not
        for item in list_min_value:
            if item.dist_I_O!=0: # checking if the item is not in the IO exit location
                for escort in self.list_of_items:
                    if escort.num==0 and escort.area==item.area : # finding escort in the storage (escort number must be 0) and checking if it is in the same area as the item
                        i = 1 # change to 1 if there is escort in the same area of the item (doesn't have to be free)
                        if escort.work=='free': # checking if the escort is free
                            dist = self.dist_from_escort(item, escort) # sending the item and the escort to the function "dist_from_escort" to calculate the distance between them
                            if dist <= item.dist_min_escort: # checking if the distance is the minimum - if it does, insert the value of the distance and the item (escort) to the appropriate attribute's item
                                item.dist_min_escort = dist
                                item.selected_escort = escort
                if i==0:
                    #if there is no  escort in the item's area
                    for escort in self.list_of_items:
                        if escort.num==0:
                            if escort.work == 'free':
                                dist = self.dist_from_escort(item, escort)
                                if dist < item.dist_min_escort:
                                    item.dist_min_escort = dist
                                    item.selected_escort = escort

                item.work='busy'
                item.selected_escort.work='busy'
                # every item, after the function found him escort, sending the item to function "match" to find the next step that the escort should do to get closer to the item
                self.match(item)

# function that found the location of the next step and sending the item with the same location of the next step together with the escort
    def direction(self,escort,item):
        if item.location_start== item.item_i_o and item.out==True: # if the item is already in the IO location - the item is sending to function exit
            self.exit(item)
        if escort.moving==0 and escort.next_step.moving==0:
            escort.route=[]
            self.step(escort.next_step,escort)


# function that helps to find the next step for the escort, to bring it near to the item - threesomes
    def match_for_three(self,item):
        item.stage=3
        escort=item.selected_escort
        escort.route=[]
        # checking if the distance between the item and the escort is bigger than 2,
        # if it does - sending the item to function "match" to bring the escort to the appropriate location next to the item
        if self.dist_from_escort(item,escort)>2:
            self.match(item)
        else:
            if item.location_start[0]>item.item_i_o[0]: # if the item is on the right side of the IO exit
                if escort.location_start[0]==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # if the escort is on the same column of the item but above it - the escort's next step will be left
                    escort.route.append('left')
                elif escort.location_start[0]+1==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # if the escort is on the left side of the item and the escort is above the item - the escort's next step will be down
                    escort.route.append('down')
                elif escort.location_start[0]+1==item.location_start[0] and escort.location_start[1]==item.location_start[1]:
                    # if the escort is on the left side of the item and they are at the same row - the escort's next step will be right
                    escort.route.append('right')
                elif escort.location_start[0]+1==item.location_start[0] and escort.location_start[1]+1==item.location_start[1]:
                    # if the escort is on the left side of the item and the escort is under the item - the escort's next step will be up
                    escort.route.append('up')
                elif escort.location_start[0]==item.location_start[0] and escort.location_start[1]+1==item.location_start[1]:
                    # if the escort is on the same column of the item and the escort is under the item - the escort's next step will be up
                    escort.route.append('up')
                elif escort.location_start[0]-1==item.location_start[0] and escort.location_start[1]+1==item.location_start[1]:
                    # if the escort is on the right side of the item and under the item - the escort's next step will be left
                    escort.route.append('left')
                elif escort.location_start[0]-1==item.location_start[0] and escort.location_start[1]==item.location_start[1]:
                    # if the escort is in the same row as the item and the escort is on the right side of the item - the escort's next step will be down
                    if escort.location_start[1] != 0:
                        escort.route.append('down')
                    else: # if the item's location is 0'st row, the escort will do fifths in his next step
                        item.stage=5
                elif escort.location_start[0]-1==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # if the escort is on the right side of the item and the escort is above the item - the escort's next step will be down
                    escort.route.append('down')
            elif item.location_start[0]<item.item_i_o[0]: # if the item is on the left side of the IO exit
                if escort.location_start[0]==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # if the escort is on the same column of the item but above it - the escort's next step will be right
                    escort.route.append('right')
                elif escort.location_start[0]+1==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # if the escort is on the left side of the item and the escort is above the item - the escort's next step will be down
                    escort.route.append('down')
                elif escort.location_start[0]+1==item.location_start[0] and escort.location_start[1]==item.location_start[1] :
                    # if the escort is on the left side of the item and they are at the same row
                    if escort.location_start[1]!=0:
                        # if the item is not in the 0'st row - the escort;s next step will be down
                        escort.route.append('down')
                    else: # if the item's location is 0'st row, the escort will do fifths in his next step
                        item.stage=5
                elif escort.location_start[0]+1==item.location_start[0] and escort.location_start[1]+1==item.location_start[1]:
                    # if the escort is on the left side of the item and the escort is under the item - the escort's next step will be right
                    escort.route.append('right')
                elif escort.location_start[0]==item.location_start[0] and escort.location_start[1]+1==item.location_start[1]:
                    # if the escort is on the same column of the item and the escort is under the item - the escort's next step will be up
                    escort.route.append('up')
                elif escort.location_start[0]-1==item.location_start[0] and escort.location_start[1]+1==item.location_start[1]:
                    # if the escort is on the right side of the item and under the item - the escort's next step will be up
                    escort.route.append('up')
                elif escort.location_start[0]-1==item.location_start[0] and escort.location_start[1]==item.location_start[1]:
                    # if the escort is in the same row as the item and the escort is on the right side of the item - the escort's next step will be left
                    escort.route.append('left')
                elif escort.location_start[0]-1==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # if the escort is on the right side of the item and the escort is above the item - the escort's next step will be down
                    escort.route.append('down')
            elif item.location_start[0]==item.item_i_o[0]: # if the item is on the same column oh the IO exit
                if escort.location_start[0]==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # if the escort is on the same column of the item and the escort is above the item - the escort will do fifths in his next step
                    item.stage=5
                elif escort.location_start[0]+1==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # if the escort is on the left side of the item and the escort is above the item - the escort's next step will be right
                    escort.route.append('right')
                elif escort.location_start[0]+1==item.location_start[0] and escort.location_start[1]==item.location_start[1]:
                    # if the escort is on the left side of the item and the same row of the item - the escort's next step will be down
                    escort.route.append('down')
                elif escort.location_start[0]+1==item.location_start[0] and escort.location_start[1]+1==item.location_start[1]:
                    # if the escort is on the left side of the item and under the item - - the escort's next step will be right
                    escort.route.append('right')
                elif escort.location_start[0]==item.location_start[0] and escort.location_start[1]+1==item.location_start[1]:
                    # if the escort is on the same column and under the item - - the escort's next step will be up
                    escort.route.append('up')
                elif escort.location_start[0]-1==item.location_start[0] and escort.location_start[1]+1==item.location_start[1]:
                    # if the escort is on the right side of the item and under the item - - the escort's next step will be left
                    escort.route.append('left')
                elif escort.location_start[0]-1==item.location_start[0] and escort.location_start[1]==item.location_start[1]:
                    # if the escort is on the same row of the item and on the right side of the item - the escort's next step will be down
                    escort.route.append('down')
                elif escort.location_start[0]-1==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # if the escort ia above the item and on the right side of the item - the escort's next step will be left
                    escort.route.append('left')
            elif item.location_start[1]==item.item_i_o[1] and item.location_start[0]>item.item_i_o[0]: # if the item is on the same row of the IO exit and on the right side of the IO exit
                if escort.location_start[0]==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # if the escort is on the same column and above the item - the escort's next step will be left
                    escort.route.append('left')
                elif escort.location_start[0]+1==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # the escort is on the left side of the item and the escort is above the item - the escort's next step will be down
                    escort.route.append('down')
                elif escort.location_start[0]+1==item.location_start[0] and escort.location_start[1]==item.location_start[1]:
                    # if the escort is on the left side of the item and the escort is on the same row of the item - the escort's next step will be right
                    escort.route.append('right')
                elif escort.location_start[0]-1==item.location_start[0] and escort.location_start[1]==item.location_start[1]:
                    # if the escort is on the same row of the item and on the right side of the item - the escort will do fifths in his next step
                    item.stage=5
                elif escort.location_start[0]-1==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # if the escort is above the item and on the right side of the item - the escort's next step will be left
                    escort.route.append('left')
            elif item.location_start[1]==item.item_i_o[1] and item.location_start[0]<item.item_i_o[0]: # if the item is on the same row of the IO exit and on the left side of the IO exit
                if escort.location_start[0]==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # if the escort is on the same column and above the item - the escort's next step will be right
                    escort.route.append('right')
                elif escort.location_start[0]+1==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # the escort is on the left side of the item and the escort is above the item - the escort's next step will be right
                    escort.route.append('right')
                elif escort.location_start[0]+1==item.location_start[0] and escort.location_start[1]==item.location_start[1]:
                    # if the escort is on the left side of the item and the escort is on the same row of the item - the escort will do fifths in his next step
                    item.stage=5
                elif escort.location_start[0]-1==item.location_start[0] and escort.location_start[1]==item.location_start[1]:
                    # if the escort is on the same row of the item and on the right side of the item - the escort's next step will be left
                    escort.route.append('left')
                elif escort.location_start[0]-1==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # if the escort is above the item and on the right side of the item - the escort's next step will be down
                    escort.route.append('down')
        if escort.route==[] and item.stage!=5: # if the escort doesn't have next step and the item's stage didn't change to 5 - the item's stage needs to change back to 1
            item.stage = 1
        if item.location_start==item.item_i_o: # if the item's location is the same as the IO exit - item's stage will change to 0 , and on the next step it will getout
            item.stage = 0


# function that helps to find the next step for the escort, to bring it near to the item - fifths
    def match_for_five(self,item):
        escort=item.selected_escort
        escort.route = []
        # checking if the distance between the item and the escort is bigger than 2,
        # if it does - sending the item to function "match" to bring the escort to the appropriate location next to the item
        if self.dist_from_escort(item,escort)>2:
            self.match(item)
        else:
            if item.location_start[0]<item.item_i_o[0]: # if the item is on the left side of the IO exit
                if escort.location_start[0]+1==item.location_start[0] and escort.location_start[1]==item.location_start[1]:
                    # if the escort is on the left side of the item and they are on the same row - the escort's next step will be up
                    escort.route.append('up')
                if escort.location_start[0]+1==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # if the escort is on the left side of the item and escort is above the item - the escort's next step will be right
                    escort.route.append('right')
                if escort.location_start[0]==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # if the escort is above item and they are on the same column - the escort's next step will be right
                    escort.route.append('right')
                if escort.location_start[0]-1==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # if the escort is on the right side of the item and the escort is above the item - the escort's next step will be down
                    escort.route.append('down')
                if escort.location_start[0]-1==item.location_start[0] and escort.location_start[1]==item.location_start[1]:
                    # if the escort is on the right side of the item and they are on the same row - the escort's next step will be left
                    escort.route.append('left')
            elif item.location_start[0]>item.item_i_o[0]: # if the item is on the right side of the IO exit
                if escort.location_start[0]+1==item.location_start[0] and escort.location_start[1]==item.location_start[1]:
                    # if the escort is on the left side of the item and they are on the same row - the escort's next step will be right
                    escort.route.append('right')
                if escort.location_start[0]+1==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # if the escort is on the left side of the item and escort is above the item - the escort's next step will be down
                    escort.route.append('down')
                if escort.location_start[0]==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # if the escort is above item and they are on the same column - the escort's next step will be left
                    escort.route.append('left')
                if escort.location_start[0]-1==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # if the escort is on the right side of the item and the escort is above the item - the escort's next step will be left
                    escort.route.append('left')
                if escort.location_start[0]-1==item.location_start[0] and escort.location_start[1]==item.location_start[1]:
                    # if the escort is on the right side of the item and they are on the same row - the escort's next step will be up
                    escort.route.append('up')
            elif item.location_start[0]==item.item_i_o[0]: # if the item is on the same column as the IO exit
                if escort.location_start[0]==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # if the escort and the item are on the same column and the escort is above the item - the escort's next step will be right
                    escort.route.append('right')
                if escort.location_start[0]+1==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # if the escort is on the left side of the item and escort is above the item - the escort's next step will be right
                    escort.route.append('right')
                if escort.location_start[0]+1==item.location_start[0] and escort.location_start[1]==item.location_start[1]:
                    # if the escort is on the left side of the item and they are on the same row - the escort's next step will be up
                    escort.route.append('up')
                if escort.location_start[0]+1==item.location_start[0] and escort.location_start[1]+1==item.location_start[1]:
                    # if the escort is on the left side of the item and the escort is under the item - the escort's next step will be up
                    escort.route.append('up')
                if escort.location_start[0]==item.location_start[0] and escort.location_start[1]+1==item.location_start[1]:
                    # if the escort is under the item and on the same column - the escort's next step will be up
                    escort.route.append('up')
                if escort.location_start[0]-1==item.location_start[0] and escort.location_start[1]+1==item.location_start[1]:
                    # if the escort is on the right side of the item and under the item - the escort's next step will be left
                    escort.route.append('left')
                if escort.location_start[0]-1==item.location_start[0] and escort.location_start[1]==item.location_start[1]:
                    # if the escort is on the right side of the item and on the same row - the escort's next step will be down
                    escort.route.append('down')
                if escort.location_start[0]-1==item.location_start[0] and escort.location_start[1]-1==item.location_start[1]:
                    # if the escort is on the right side of the item and above the item - the escort's next step will be down
                    escort.route.append('down')
        if escort.route == []: # if the escort doesn't have next step - the item's stage needs to change back to 1
            item.stage = 1
        if item.location_start==item.item_i_o: # if the item's location is the same as the IO exit - item's stage will change to 0 , and on the next step it will getout
            item.stage = 0


# function that acutally makes the step
# adding the step to the step list
    def step(self, item, escort):
        self.step_list.append([[item.location_start[0], item.location_start[1], item.num],
                            [escort.location_start[0], escort.location_start[1], escort.num]])
        # changing the attribute "moving" os the escort and the item that moved to 1 - since they made a step and moved
        item.moving=1
        escort.moving=1
        # switching between the locations
        item_start = item.location_start
        item.location_start = escort.location_start
        escort.location_start = item_start
        # calculate the distnace between the item that just moved and the escort that moved shift
        item.dist_I_O = self.dist_from_I_O(item, item.item_i_o)

# function that calculate the distance between item and escort - Manhattan distances
    def dist_from_escort(self,item, escort):
        sum = (abs(item.location_start[0]-escort.location_start[0])+abs(item.location_start[1]-escort.location_start[1]))
        return sum

# function that calculate the distance between item and its IO exit - Manhattan distances
    def dist_from_I_O(self,item, I_O):
        sum = (abs(item.location_start[0]-I_O[0])+abs(item.location_start[1]-I_O[1]))
        return sum

# function that sendig the escort and the item to function that acutally make the step - according to the item's stage
    def run_direction(self,item):
        if item.stage==1: # if item's stage is 1 - the item and its escort will be send to function "direction"
            self.direction(item.selected_escort,item)
        elif item.stage==3: # if item's stage is 3 - the item and its escort will be send to function "direction_for_three"
            self.direction(item.selected_escort,item)
        if item.location_start==item.item_i_o or item.stage==0: # if item's stage is 0 - the item and its escort will be send to function "exit"
            if item.selected_escort!=None:
                item.selected_escort.work='free'
            if item.num!=0 and item.out==True:
                self.exit(item)
        elif item.stage==5: # if item's stage is 5 - the item and its escort will be send to function "direction_for_five"
            self.direction(item.selected_escort,item)

# function that creates the list that contain every step in each time step it happend
# and a list that contain the number of the item that took out and in which time step it happend
# moreover, it is initializing the list of items that need to go and the step list
# and initializing the "moving" attribute of the item and the escort to 0 - so on the next time step they could move
    def final_step(self):
        self.list_need_to_go=[] # initializing the list of items that need to go
        for line in self.step_list:
            for i in self.list_of_items:
                if i.location_start==(line[0][0],line[0][1]) or i.location_start==(line[1][0],line[1][1]):
                    i.moving=0 # initializing the "moving" attribute of the item and the escort to 0 - so on the next time step they could move
            self.final_list.append([self.time_step,line[0],line[1]])
        self.time_step+=1
        self.step_list=[]

# function two is helping to find the next step of the escort and actually making the step

    def function_two(self):
        for item in self.list_need_to_go:
            if item.dist_I_O!=0: # checking if the item's location is not the same as the IO exit
                if item.stage == 1 and item.selected_escort.route==[]:
                    self.match(item)
                if item.stage==3 :
                    self.match_for_three(item)
                elif item.stage==5 :
                    self.match_for_five(item)
                    # after finding the next step of the escort with the appropriate mach function (according to its stage),
                    # sending the item to function "run direction" to actually make the step
                if item.selected_escort.route != []:  # checking if the item's location is not the same as the IO exit and the escort has next step
                    escort = item.selected_escort
                    next=()
                    # finding the next step location according to the escort route
                    if escort.route[0] == 'up':
                        next = (escort.location_start[0], escort.location_start[1] + 1)
                    elif escort.route[0] == 'down':
                        next = (escort.location_start[0], escort.location_start[1] - 1)
                    elif escort.route[0] == 'right':
                        next = (escort.location_start[0] + 1, escort.location_start[1])
                    elif escort.route[0] == 'left':
                        next = (escort.location_start[0] - 1, escort.location_start[1])
                    for i in self.list_of_items:
                        if next == i.location_start:
                            # insert the class item of the next step to the escort
                            escort.next_step = i
                    self.run_direction(item)
            else: # if the item's location is already in the IO exit, just need send the item to the function "run direction" without finding next step for its escort
                self.run_direction(item)
        self.final_step() # sending to "final step" function to make the list of steps that contain time step

# function one is preparing the item that we need to take out, finding him the perfect escort and matching the escort the next step that it need to do
# moreover, the function is building the list of items that need to get out

    def function_one(self):
        next = () # initialize the next step
        self.which_dist_from_I_O() # sending to this function that will help us to find which item , that need to get out, is close to the IO exit
        self.exit_item() # sending to this function that will help us to find out which item is in the IO exit and checking if we need to take it out
        self.count_escort() # sending to this function that will help us to calculate the amount of free escorts in the storage
        if self.escort_A!=0 or self.escort_B!=0 or self.escort_C!=0: # checking if there are free escort in the storage
            self.finding_min() # if there is a free escort, sending to the function that will help us to find the closer escort to item that needs to get out
            for item in self.list_of_items:
                # if the item is busy , the item is not an escort and there is an escort that related to him
                # the item will append to the list of items that need to go
                if item.work=='busy' and item.num!=0 and item.location_start!=item.item_i_o and item.selected_escort!=None:
                    self.list_need_to_go.append(item)
        elif self.escort_A==0 and self.escort_B==0 and self.escort_C==0:
            for item in self.list_of_items:
                # if the item is busy , the item is not an escort and there is an escort that related to him
                # the item will append to the list of items that need to go
                if item.work == 'busy' and item.num != 0 and item.location_start != item.item_i_o and item.selected_escort!=None:
                    self.list_need_to_go.append(item)
        for item in self.list_need_to_go:
            if item.dist_I_O!=0 and item.selected_escort.route!=[]: # checking if the item's location is not the same as the IO exit and the escort has next step
                escort=item.selected_escort
                # finding the next step location according to the escort route
                if escort.route[0]=='up':
                    next=(escort.location_start[0],escort.location_start[1]+1)
                elif escort.route[0]=='down':
                    next=(escort.location_start[0],escort.location_start[1]-1)
                elif escort.route[0]=='right':
                    next=(escort.location_start[0]+1,escort.location_start[1])
                elif escort.route[0]=='left':
                    next=(escort.location_start[0]-1,escort.location_start[1])
                for i in self.list_of_items:
                    if next==i.location_start:
                        # insert the class item of the next step to the escort
                        escort.next_step=i
        self.function_two() # sending to function two


# 10 escorts

s_ten_escorts = Storage(storage_list_ten_escorts,out_item_list_ten_escorts)

while len(s_ten_escorts.list_out_items)!=0:
    s_ten_escorts.function_one()

# list step by step
file_name_10_escorts_steps = '10_escorts_steps.p'
out_file_10_escorts_steps = open(file_name_10_escorts_steps,'wb')
pickle.dump(s_ten_escorts.final_list,out_file_10_escorts_steps)
out_file_10_escorts_steps.close()

# list of items that went out with their time step
file_name_10_escorts_out = '10_escorts_items_out.p'
out_file_10_escorts_items = open(file_name_10_escorts_out,'wb')
pickle.dump(s_ten_escorts.final_out_list,out_file_10_escorts_items)
out_file_10_escorts_items.close()

# 50 escorts

s_fifty_escorts = Storage(storage_list_fifty_escorts, out_item_list_fifty_escorts)

while len(s_fifty_escorts.list_out_items) != 0:
   s_fifty_escorts.function_one()

# list step by step
file_name_50_escorts_steps = '50_escorts_steps.p'
out_file_50_escorts_steps = open(file_name_50_escorts_steps, 'wb')
pickle.dump(s_fifty_escorts.final_list, out_file_50_escorts_steps)
out_file_50_escorts_steps.close()

# list of items that went out with their time step
file_name_50_escorts_out = '50_escorts_items_out.p'
out_file_50_escorts_items = open(file_name_50_escorts_out, 'wb')
pickle.dump(s_fifty_escorts.final_out_list, out_file_50_escorts_items)
out_file_50_escorts_items.close()

# 100 escorts

s_one_escorts = Storage(storage_list_one_escorts, out_item_list_one_escorts)

while len(s_one_escorts.list_out_items) != 0:
    s_one_escorts.function_one()

# list step by step
file_name_100_escorts_steps = '100_escorts_steps.p'
out_file_100_escorts_steps = open(file_name_100_escorts_steps, 'wb')
pickle.dump(s_one_escorts.final_list, out_file_100_escorts_steps)
out_file_100_escorts_steps.close()

# list of items that went out with their time step
file_name_100_escorts_out = '100_escorts_items_out.p'
out_file_100_escorts_items = open(file_name_100_escorts_out, 'wb')
pickle.dump(s_one_escorts.final_out_list, out_file_100_escorts_items)
out_file_100_escorts_items.close()
