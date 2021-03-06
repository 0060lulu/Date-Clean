import re

import pandas as pd


# <editor-fold desc="案例模块">
def open_file(sheets_name):
    df=pd.read_excel('数据集/多行转多列数据集.xlsx',sheet_name=sheets_name)
    return df

def get_new_columns(df):
    '''
    >> 利用正则匹配出目标columns
    >> df.columns=['栋数', '户型', '姓名', '性别', '电话', '房号', '姓名.1', '性别.1', '电话.1', '房号.1','姓名.2', '性别.2', '电话.2', '房号.2']
    >> 当我们的columns重复的时候，pandas会自动帮我们在重复的columns后面加上.编号。
    :param df:
    :return:
    '''
    # 提取columns对应的字段
    pattern_name=r',(姓名.?\d?),'
    pattern_room=r',(房号.?\d?),'
    pattern_phoone=r',(电话.?\d?),'
    # 通过前后增加逗号，确保正则的精准匹配
    columns_str=','+','.join(df.columns.to_list())+','
    columns_name=re.findall(pattern_name,columns_str)
    columns_room=re.findall(pattern_room,columns_str)
    columns_phone=re.findall(pattern_phoone,columns_str)
    target_columns=[]
    # 将每一行的数据变为一个一层嵌套的列表
    for i in range(len(columns_name)):
        target_columns+=[columns_room[i],columns_name[i],columns_phone[i]]
    return target_columns

# 用于rebuild_df的apply
def merge_cols(Series):
    # 获取非空项
    Series=Series[Series.notna()]
    # 获取当行所有数据
    value=Series.values
    result=[]
    # 将每一行的数据变为一个一层嵌套的列表
    for idx in range(0,len(value),3):
        result.append([value[idx],value[idx+1],value[idx+2]])
    return result

def rebuild_df(df,merge_columns):
    # 获取表格头部通用信息
	# merge_columns=['房号', '姓名', '电话', '房号.1', '姓名.1', '电话.1', '房号.2', '姓名.2', '电话.2']
    df_new=df.iloc[:,:2]
    # 对数据进行合并
    df_new['merge']=df.loc[:,merge_columns].apply(merge_cols,axis=1)
    # 通过explode变成多行
    df=df_new.explode('merge')
    # 拆分merge列的列表
    df['房号']=df['merge'].str[0]
    df['姓名']=df['merge'].str[1]
    df['电话']=df['merge'].str[2]
    df.drop('merge',axis=1,inplace=True)
    return df
# </editor-fold>




if __name__ == '__main__':
    # <editor-fold desc="案例程序">
    sheets_name_list=pd.ExcelFile('数据集/多行转多列数据集.xlsx').sheet_names
    for sheets_name in sheets_name_list:
        df=open_file(sheets_name)
        merge_columns=get_new_columns(df)
        df=rebuild_df(df,merge_columns)
        df.to_excel(f'数据集/{sheets_name}.xls', index=False, sheet_name=sheets_name,encoding='utf-8')
    # </editor-fold>

