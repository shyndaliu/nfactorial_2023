Каждая база данных представляет собой папку с таблицами, где таблицы являются json файлами.
В файле main.py осуществляются все функции базы данных

комманды были заимствованы с языка SQL и корректность ввода проверяется с помощью regex

•СОЗДАНИЕ БАЗЫ ДАННЫХ-------------

CREATE DATABASE *db name*

    ex. CREATE DATABASE mydb

•УДАЛЕНИЕ БАЗЫ ДАННЫХ-------------

DROP DATABASE *db name*

    ex. DROP DATABASE mydb

•СОЗДАНИЕ ТАБЛИЦЫ--------------

CREATE TABLE *tb name* IN *db name* (
    column1 datatype(INT|BOOL|FLOAT|STR) constraint(PRIMARYKEY|NOTNULL| ),
    ...
)

    ex. CREATE TABLE phonebook IN mydb (
        id INT PRIMARYKEY,
        name STR,
        surname STR,
    )

•УДАЛЕНИЕ ТАБЛИЦЫ-------------

DROP TABLE *tb name*

    ex. DROP TABLE phonebook

•ВЫВОД [отфильтрованных/сортированных] ДАННЫХ

SELECT (*|column1,column2,....) FROM *tb_name* 
SELECT (*|column1,column2,....) FROM *tb_name* WHERE column1='value' 
SELECT (*|column1,column2,....) FROM *tb_name* ORDER BY *column* (ASC|DSC)

    ex. SELECT name,number FROM phonebook WHERE name='John' ORDER BY id DESC

•ВСТАВКА ДАННЫХ

INSERT INTO *tb name* (column1,column2,...) VALUES (value1,value2,...)

    ex. INSERT INTO phonebook (id,name,number) VALUES (1,John,Smith)

•УДАЛЕНИЕ СТРОКИ ПО ЗАДАННОМУ ПАРАМЕТРУ

DELETE FROM *tb name* WHERE column1='value' 

    ex. DELETE FROM phonebook WHERE name='John'

•ИЗМЕНЕНИЕ ЗНАЧЕНИЯ ПО ЗАДАННОМУ ПАРАМЕТРУ

UPDATE *tb name* WHERE column1='value' 
SET column2='newvalue'

    ex. UPDATE phonebook WHERE id=1
    SET surname='Brown'
