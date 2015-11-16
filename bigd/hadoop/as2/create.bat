notepad join1_mapper.py

notepad join1_reducer.py

notepad join1_FileA.txt

notepad join1_FileB.txt

notepad make_join2data.py

notepad make_data_join2.txt

chmod +x join1_mapper.py

chmod +x join1_reducer.py

cat join1_File*.txt|./join1_mapper.py|sort|./join1_reducer.py