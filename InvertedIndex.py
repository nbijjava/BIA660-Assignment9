from Appearance import Appearance
import spacy

class InvertedIndex:
    
    """
    Inverted Index class.
    """
    def __init__(self, db):
        self.index = dict()
        self.db = db
    def __repr__(self):
        """
        String representation of the Database object
        """
        return str(self.index)
        
    def index_document(self, document):
        """
        Process a given document, save it to the DB and update the index.
        """
        appearances_dict = dict()             
            
        nlp = spacy.load("en_core_web_lg")    
        nlp.max_length = 3324221
        doc = nlp(document['text'])     
        # Removing stopwords and punctuation from the doc.
        robotics_doc=[token for token in doc if not (token.is_stop or token.is_punct or token.is_space)] 
   
        # Dictionary with each term and the frequency it appears in the text.
        for token in robotics_doc:                  
            term_frequency = 0
            for item in appearances_dict:
                if token.text in str(item):
                    term_frequency = appearances_dict[item].frequency     
            appearances_dict[token.text] = Appearance(document['id'], term_frequency + 1)
            # print("appearances_dict " + str(appearances_dict[token.text]))              
                    
        # Update the inverted index
        update_dict = { key: [appearance]
                       if key not in self.index
                       else self.index[key] + [appearance]
                       for (key, appearance) in appearances_dict.items() }
        self.index.update(update_dict)
        # Add the document into the database
        self.db.add(document)
        return document
    
    def lookup_query(self, query):
        """
        Returns the dictionary of terms with their correspondent Appearances. 
        This is a very naive search since it will just split the terms and show
        the documents where they appear.
        """      
        
        return{
                term : self.index[term]
                for diff in query.split(' ') 
                    for term in self.index
                        if diff in str(term)
            }