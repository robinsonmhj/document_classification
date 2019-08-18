import logging

logger = logging.getLogger(__name__)
def separateData(no=2, source_file="shuffled-full-set-hashed.csv"):
    """
    @brief divided the data evenly into n parts
    @param no the number of files divided into
    @param source_file file which you want to be divided
    
    """
    category = []
    category_map = {}
    with open(source_file,"r") as source:
        for line in source:
            columns = line.split(",")
            category=columns[0]
            data=columns[1]
            l = []
            if category in category_map:
                l=category_map[category]
            l.append(data)
            category_map[category]=l
    
    c_array=[]
    con_array=[]
    for i in range(no):
        c_array.append(list())
        con_array.append(list())
    for category, contents in category_map.items():
        counter = 0
        for content in contents:
            c_array[counter%no].append(category)
            con_array[counter%no].append(content)
            counter += 1
            
    return  c_array, con_array

def spilt_file():
    source_file ="data.csv"
    traing_data = "training_data.csv"
    testing_data = "testing_data.csv"
    with open(source_file,"r") as source, open(traing_data,"w+") as traing, open(testing_data,"w+") as testing:
        counter = 0
        for line in source:
            traing.write(line)
            if counter == 100:
                testing.write(line)
            counter += 1
