import os
from .myairav import Airav
from .myavsox import Avsox
from .mycarib import Carib
from .mydlsite import Dlsite
from .myfanza import Fanza
from .myfc2 import Fc2
from .myfc2club import Fc2club
from .myjav321 import Jav321
from .myjavbus import Javbus
from .myjavdb import Javdb
from .mymgstage import Mgstage
from .mymv91 import Mv91
from .htmlclass import getVideoInfoBase


class register_db():
    registered_db = {}

    def register(self,dbclass):
        #print(dbclass.__class__.__name__)
        self.registered_db[dbclass.__class__.__name__] = dbclass

    def main(self):
        self.register(Javdb())
        self.register(Javbus())
        self.register(Jav321())
        self.register(Airav())
        self.register(Avsox())
        self.register(Carib())
        self.register(Dlsite())
        self.register(Fanza())
        self.register(Fc2())
        self.register(Fc2club())
        self.register(Mgstage())
        self.register(Mv91())
    
    
if __name__ == '__main__':
    db = register_db()
    print(db.registered_db)
    
