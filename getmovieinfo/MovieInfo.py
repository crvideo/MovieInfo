import argparse
import jsons
import os
import re
import sys
from .WebCrawler.register import register_db
import os
import io


def argparse_function():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", default='', nargs='?', help="Custom file number to search all db.")
    parser.add_argument("-k", "--keyword", default='', nargs='?', help="Custom keyword to search two dbs.")	
    parser.add_argument("--cache_dir", default='~/.config/cache_dir', nargs='?', help="The path to save search results.")

    args = parser.parse_args()
    return args

def main():
    args = argparse_function()
    db = register_db()
    db.main()
    #print(db.registered_db)
    #print(args)
    if args.number:
        for dbname in ["Javbus","Javdb","Jav321","Carib","AVsox","Airav","Dlsite","Fanza","Fc2","Fc2club","Mgstage","Mv91"]:
            res = db.registered_db.get(dbname).main(args.number)
            if res['download']:
                #print(res)
                print(jsons.dumps(res['download'][0]))
                break
                
    if args.keyword:
        args.cache_dir = os.path.expanduser(args.cache_dir)
        #print(args.cache_dir)
        if not os.path.exists(args.cache_dir):
            os.makedirs(args.cache_dir,exist_ok=True)
        if not os.path.exists(args.cache_dir + "/" + args.keyword+".json"):
            for dbname in ["Javbus","Javdb"]:
                res = db.registered_db.get(dbname).searchKeyword(args.keyword)
                if res and res[0]["title"]:
                    with io.open(args.cache_dir + "/" + args.keyword + ".json","w",encoding='utf8') as f:
                        f.write(jsons.dumps(res))
                    break
            print(jsons.dumps(res))
        else:
            with open(args.cache_dir + "/" + args.keyword + ".json","r",encoding = 'utf8') as f:
                res = f.read()
                print(res)
        

if __name__ == '__main__':
    main()

