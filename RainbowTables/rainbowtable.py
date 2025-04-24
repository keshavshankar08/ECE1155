import hashlib



class RainbowTable:


    def __init__(self, algorithm, chain_length):
        """RainbowTable constructor

        Arguments:
                algorithm {string} -- name of hash algorithm used
                chain_length {int} -- chain length

        Raises:
                ValueError -- if algorithm is not 'sha1' or 'md5'
        """

        # load algorithm TODO manage arguments properly
        if(algorithm != hashlib.md5) and (algorithm != hashlib.sha1):
            raise ValueError("Algorithm not supported")
        self.algorithm = algorithm
        self.chain_length = chain_length
    '''
    Loads a RainbowTable object with a table from a text file
    Arguments:
        filename -- file to take table from
    '''
    '''
    def load_rainbow_table_from_compressed(self, filename):
        lines = compression.decode_and_decompress(filename)
        my_dict = {}
        for line in lines:
            if ":" in line:
                key, value = line.strip().split(":", 1)
                my_dict[key.strip()] = value.strip()
        self.table = my_dict
    '''
    
    def load_rainbow_table(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            my_dict = {}
            for line in f:
                key, value = line.strip().split(":", 1)
                my_dict[key.strip()] = value.strip()
        self.table = my_dict


    def hash_function(self, plaintext):
        """Returns a string that contains the computed hash of the 
        given string, using the algorithm chosen

        Arguments:
                plaintext {string} -- plaintext to hash

        Returns:
                string -- the hash computed
        """
        hash = self.algorithm()
        hash.update(plaintext.encode('utf-8'))
        return hash.hexdigest()


    def reduce_function(self, hashstring):
        """Returns a string that contains the reduced value of the 
        given hash string

        Arguments:
                plaintext {string} -- hash to reduce

        Returns:
                string -- the hash computed
        """

        return hashstring[0:(ord(hashstring[0])%8)+8] # reduction is between 8 and 16 characters
    def generate_chain(self, password):
        '''produces a chain starting from a plaintext
        
        Arguments:
            password {string} -- plaintext to start from
        
        Returns:
            string -- the final hash (chain tail)
        '''
        reduced = password
        for i in range(self.chain_length):
            hashed = self.hash_function(reduced)
            reduced = self.reduce_function(hashed)
        return hashed


    def generate_table(self, text_table):
        '''generates the full table
        '''
        collisions = 0
        self.table = {}
        file = open(text_table, "r", encoding='utf-8')
        password = file.readline().strip()
        while password:
            # generates a random password of allowed length        
            chainTail = self.generate_chain(password)
            if(chainTail in self.table):
                collisions += 1
            self.table[chainTail] = password
            password = file.readline().strip()
        print("collisions detected: " + str(collisions))
    '''
    Writes table to a textfile

    Arguments:
        filename -- text file to write dictionary to

    '''
    def save_to_text_file(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            for key, value in self.table.items():
                f.write(f"{key}: {value}\n")

    
    def save_to_file(self, filename):
        '''
        writes this object on a file
        
        Arguments:
            filename {string} -- output file path
        
        Returns:
            bool -- true if success
        
        if (filename is None):
            return False
        fd = open(filename, "wb")
        if(fd.write(pickle.dumps(self)) > 0):
            return True
        return False
    '''

    '''
    @staticmethod
    def load_from_file(filename):
        loads a RainbowObject previously generated
        
        Arguments:
            filename {string} -- input file path
        
        Raises:
            ValueError -- if the file does not contain a valid object
        
        Returns:
            RainbowTable -- the loaded object
        
        with open(filename, 'rb') as inputFile:
            objectLoaded = pickle.load(inputFile)
        if(not isinstance(objectLoaded, RainbowTable)):
            raise ValueError("The file " + filename +
                             " does not contain a valid table")
        return objectLoaded
'''


    def lookup(self, hash_to_crack):
        '''looks for a cracked hash
        
        Arguments:
            hash_to_crack {string}
        
        Returns:
            the plaintext if found, None otherwise
        '''
        new_hash = hash_to_crack
        for i in range(self.chain_length):
            if new_hash in self.table.keys(): # check if hash matches end of chain
                possible_password = self.crack(new_hash, hash_to_crack) # find corresponding plaintext
                if possible_password:
                    return possible_password
            reduced_hash = self.reduce_function(new_hash)
            new_hash = self.hash_function(reduced_hash)
        return None




    def crack(self, chain_tail, password_hash):
        '''tries to crack a given hash on a single chain
        
        Arguments:
            chainhead {string}
            hash_to_crack {string}
        
        Returns:
            string -- the plaintext if found, None otherwise
         '''
        
        reduced = self.table[chain_tail]
        for i in range(self.chain_length):
            hashed = self.hash_function(reduced)
            if hashed == password_hash:
                return reduced
            reduced = self.reduce_function(hashed)
        return None
<<<<<<< HEAD
    

=======
>>>>>>> 5360654bb2e291faa2081232c96cbea4713dbbcf

