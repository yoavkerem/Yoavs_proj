with open('datas.txt','r') as f:
    data_list=[]
    for line in f:
        print(line)
        data_list.append(line.split(' ')[1][:-1])
print(data_list[0])
print(data_list[1])
