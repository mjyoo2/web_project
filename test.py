from app.module.login_database import *
from app.module.database import Database
import numpy as np
import pickle as pkl

if __name__ == '__main__':
    a= 1
    with open('hhh.pkl', 'wb') as f:
        pkl.dump(a, f)