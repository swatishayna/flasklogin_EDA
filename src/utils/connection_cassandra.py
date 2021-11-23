from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os
from pathlib import Path

class cassandra_user:
    def connect(self):
        dir_path = os.path.join((Path(__file__).resolve().parent.parent.parent),'files')
        file_path = os.path.join(dir_path,'secure-connect-onlineedaautomation.zip')
        cloud_config= {
        'secure_connect_bundle': file_path
                        }
        auth_provider = PlainTextAuthProvider('lmzksofvDqTOMcKEvCHkxxDq', 'QYJD5.tkio5FmTy.egAUkW,YoSi24UZRJcEeRerAA+0btYbZ6ZtSSdERAJeN.T.Wo_5no_GIxW0Dr+bc1R,Ue+3.,7-,cca6+bgQsezAUItB64U0zfkwvhn9DRn_bqXX')
        cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        self.session = cluster.connect()
        return self.session
    

    def get_useraccount(self,query):
        session = self.connect()
        session.execute("USE user_account")
        user_detail = session.execute(query)
        return user_detail.all()

    def adduser(self,query):
        try:
            session = self.connect()
            session.execute("USE user_account")
            info = session.execute(query)
            return info.all()
        except:
            print("^^^^^^^^^^^^^^^^^^^^^")




   
        
