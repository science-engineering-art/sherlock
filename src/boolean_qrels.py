import re
from qrels import QRels


class BooleanQRels(QRels):
    def get_query(self, query):
        query = [ word for word in 
            re.findall(r"[\w']+", query.text) ]
        return ' & '.join(query)