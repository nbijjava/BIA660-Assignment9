from InvertedIndex import InvertedIndex
from Database import Database
import csv

word_doc_dict={}

def __init__(self, db):
    self.db = db
        
def highlight_term(id, term, text):
    replaced_text = text.replace(term, "\033[1;32;40m {term} \033[0;0m".format(term=term))
    return "--- document {id}: {replaced}".format(id=id, replaced=replaced_text)

def main():    
    db = Database()
    index = InvertedIndex(db)
    
    with open('JEOPARDY_CSV.csv',encoding="utf=8") as f:        
        reader = csv.reader(f, delimiter=",")
        next(reader)
        for i, row in enumerate(reader):
            document = {
                'id': i,
                'text':  " ".join([row[3], row[5], row[6]]) 
            }
            index.index_document(document) 
    
    
    search_term = input("Enter term(s) to search: ")
    result = index.lookup_query(search_term)
            
        
    for term in result:
        for appearance in result[term]:
            # Belgium: { docId: 1, frequency: 1}
            document = db.get(appearance.docId)
            print(highlight_term(appearance.docId, term, document['text']))
        print("-----------------------------")    
       

main()