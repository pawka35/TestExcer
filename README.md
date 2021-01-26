### Тестовое задание для TL
##### Для запуска необходимо уставить модули:
- [requests](https://pypi.org/project/requests/) 
	- pip install requests
- [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)
	- pip install SQLAlchemy
- [Django](https://pypi.org/project/Django/ "Django") 
	- pip install Django
	
##### Запуск проекта:
- Запуск клиента:
		_path_to_ptoject_folder_/ClienJsonToBD/main.py
		
- Запуск веб-интерфейса:
		_path_to_ptoject_folder_/WebFace/manage.py runserver

#### Содержание проекта:
- Директория: ClienJsonToBD 
	- main.py -запуск клиента
	- client.ini - настройки инициализации скрипта клиента
	- explanations.txt - пояснения к проекту
	- Поддиректория test:
		- unittests.py  файл автотестов для клиента
		
- Директория db
	- TestEx.db - База данных проекта
	- OrmClasses.py - классы для ORM `SQLAlchemy`
	- DBWork.py -  работа с БД
	- NotOrm_Classes.py - классы для работы с БД без `SQLAlchemy` (см. пояснения в explanation.txt)
	- NotOrmDBWork.py - работа с БД без `SQLAlchemy` (см. пояснения в explanation.txt)
	
- Директория WebFace
	- Поддиректория main:
		рабочая директория для пути http://host/ и http://host/username (то что писалось мной)
		
------------
### Test task for TL
##### You need to install module:
- [requests](https://pypi.org/project/requests/) 
	- pip install requests
- [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)
	- pip install SQLAlchemy
- [Django](https://pypi.org/project/Django/ "Django") 
	- pip install Django
	
##### Launch of the project:
- Launching the client:
		_path_to_ptoject_folder_/ClienJsonToBD/main.py
		
- Launching the web interface:
		_path_to_ptoject_folder_/WebFace/manage.py runserver

#### Content of the project:
- Directory: ClienJsonToBD 
	- main.py - start the client
	- client.ini - client script initialization settings
	- explanations.txt - explanations for the project
	- Subdirectory  test:
		- unittests.py - file of autotests for the client
		
- Directory: db
	- TestEx.db - Project database
	- OrmClasses.py - classes for ORM `SQLAlchemy`
	- DBWork.py -  working with the database
	- NotOrm_Classes.py - classes for working with the database without `SQLAlchemy` (read in explanation.txt)
	- NotOrmDBWork.py - working with a database without `SQLAlchemy` (read in explanation.txt)
	
- Directory WebFace
	- Subdirectory  main:
		working directory for the URLs: http://host/ и http://host/username (that what was written by me)


