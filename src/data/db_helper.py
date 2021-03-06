# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月3日

@author: ALEX
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.config import DbProp


def new_session():
    engine = create_engine(DbProp.url, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def insert(data):
    session = new_session()
    try:
        session.add(data)
        session.commit()
    finally:
        # 关闭session:
        session.close()

        
def batch_insert(data):
    session = new_session()
    try:
        session.add_all(data)
        session.commit()
    finally:
        # 关闭session:
        session.close()


def select(query, args):
    session = new_session()
    try:
        return query(session, args).all()
    finally:
        # 关闭session:
        session.close()

def selectSql(sql):
    engine = create_engine(DbProp.url, echo=False)
    conn = engine.connect()
    try:
        return conn.execute(sql).fetchall()
    finally:
        # 关闭session:
        conn.close()

def executeSql(sql):
    engine = create_engine(DbProp.url, echo=False)
    conn = engine.connect()
    try:
        conn.execute(sql)
    finally:
        # 关闭session:
        conn.close()