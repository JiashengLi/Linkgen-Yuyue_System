import os


docu = os.getcwd()
for dir_cont in os.walk(docu):
    for file in dir_cont[2]:
        if os.path.splitext(file)[1] in ['.jpg'] or file=='test.py':
            pass
        else:
            try:
                file_path = os.path.join(dir_cont[0],file)
                file_new = file+'.jpg'
                file_path_new = os.path.join(dir_cont[0],file_new)
                os.rename(file_path, file_path_new)
                print ('成功更改文件名%s'%(file))
            except Exception as e:
                print ('更改文件名%s时发生错误，错误信息为：\n%s'%s(file,str(e)))
            
