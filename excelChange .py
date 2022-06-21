import xlrd #引入库
import wordTrans
ef=xlrd.open_workbook("D:\\test\\****.xlsx") #打开文件返回工作簿对象

#table_page_num=0 #读取文件中的第几sheet
#nameCol=3        #用于生成mysql 属性名 的列序号
#dataCol=7        #用来获取mysql 属性类型 的列序号

#start_col=0     #需要生成mysql 语句的起始列
#end_col=44      #用于生成mysql 语句的结束列



#获取表的数据,并转化为建库所需数组
#所需参数:[table_page_num: 需要读取的sheet编号 ,start_col:用于数据生成的起始列 ,end_col:用于数据生成的起始列 ,
#          nameRow:用来生成属性名的行,dataRow：用来生成数据类型的行]
def get_table_data(table_page_num,start_col,end_col,nameRow,dataRow):  
    sheet=ef.sheet_by_index(table_page_num)   #获取第table_page_num 页  也可以通过sheet的名称进行获取，sheet_by_name('sheet名称')
    sql_data_type=[]   #数据类型
    sql_col_name=[]    #列名

    mysqlType=['varchar','varchar','decimal','date','boolean','varchar']
    
    #把表格内的数据转化成，符合规范的变量名
    sql_col_name=wordTrans.exceltocol(sheet.row_values(nameRow,start_col,end_col)) 
    for i in range(start_col,end_col):   
        #根据表格内的数据，获取变量类型
        temp_type_num=sheet.cell(dataRow,i).ctype 
        sql_data_type.append(mysqlType[temp_type_num])

    return [sql_col_name,sql_data_type]
        

# 表中字段生成语句
def fieldstatement(col_name,sql_Type):
    #根据列数据类型写入sql insert语句
    if sql_Type=="varchar":
        inser_param="`{0}` {1}(255) NULL ".format(col_name,sql_Type) 

    elif sql_Type=="decimal":
        inser_param="`{0}` {1}(10,2) NULL ".format(col_name,sql_Type)
        
    else:
        inser_param="`{0}` {1}".format(col_name,sql_Type)
    return inser_param

def create_table_statement(table_page_num,name_list,type_list):
    #创建sql语句
    createTableSql="CREATE TABLE {tableName}( \n".format(tableName=wordTrans.wordtoname(ef.sheet_names()[table_page_num]))
    for i in range(len(type_list)):
        #拼接建库语句
        inser_param=fieldstatement(name_list[i],type_list[i])
        if (i!=len(name_list)-1):
            inser_param+=','
            
        createTableSql=createTableSql+inser_param

    createTableSql+=')'

    return createTableSql


if __name__=="__main__":
    print("开始执行")
    dataArray=get_table_data(0,0,44,3,7)
    print(create_table_statement(0,dataArray[0],dataArray[1]))


