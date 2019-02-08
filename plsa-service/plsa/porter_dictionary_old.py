__author__ = 'eyob'


import pickle

class porter_dictionary:


    def __init__(self):

        self.dictionary = dict()



    def add_element(self,stemmed, nonstemmed):

        self.arr = []

        if stemmed in self.dictionary:
            print('Stemmed word',stemmed,'present')
            self.arr = self.dictionary[stemmed]

            if nonstemmed in self.arr:
                print('Nonstemmed word',nonstemmed,'present')
                pass
            else:
                print('Nonstemmed word',nonstemmed,'absent')
                self.arr.append(nonstemmed)
                self.dictionary.update({stemmed:self.arr})
        else:
            print('Stemmed word',stemmed,'absent')
            self.arr.append(nonstemmed)
            self.dictionary.update({stemmed:self.arr})



    def write_dict_to_file(self,file_name):

        with open(file_name, 'wb') as handle:
            pickle.dump(self.dictionary,handle,protocol=2)


        self.sorted_keys = sorted(self.dictionary)

        with open(file_name+'.txt','w') as file1:
            for i in self.sorted_keys:
                file1.write(i+str(self.dictionary[i])+'\n')




    def load_dict(self,file_name):
        with open(file_name, 'rb') as handle:
            self.dictionary = pickle.load(handle)





if __name__ == '__main__':

    pass




