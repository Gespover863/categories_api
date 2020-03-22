# Categories_API

## Описание

Данное приложение является **сервисом создания иерархической структуры данных категорий**. 

## Установка
Для успешного запуска приложения необходимо выполнить следующие шаги:

 - Установить все необходимые библиотеки командой `pip install -r pip install -r requirements.txt`
 - В `PostgreSQL` создать новую базу данных - `CREATE DATABASE categories_api`
 - В конфигурациях подключения к БД в файле `Categories_API/settings.py` 
   стоят `USER: postgres` и `PASSWORD: postgres` которые необходимо поменять в зависимости от 
   настроек вашей роли в `PostgreSQL`
 - Применить миграции к БД - `python manage.py migrate`.

## Postman
Для сервиса существует дополнительная документация **Postman'a**. 
Она находится в корневой директории приложения - **Categories_Api.postman_collection.json**

Для ее корректной работы необходимо создать в Postman локальную переменную **local_address**
в которой будет указан адрес, на котором у Вас будет запускаться приложение. 
После чего можно приступать к работе.

## Запросы

С приложением можно взаимодействовать посредством http-запросов.
Ниже будут приведены примеры всех возможных сценариев работы приложения.

### Получение информации о созданной категории 

Запрос:

    GET /api/get_graph/<id>
    

Ответ:

    {
    "success": true,
    "result": {
        "id": 1,
        "name": "Category 1",
        "parents": [],
        "children": [],
        "sublings": []
    },
    "error": null
    }

#### Пример

Запрос:

    GET /api/get_graph/1


Ответ:

    {
    "success": true,
    "result": {
        "id": 1,
        "name": "Category 1",
        "parents": [],
        "children": [
            {
                "id": 2,
                "name": "Category 1.1"
            },
            {
                "id": 11,
                "name": "Category 1.2"
            }
        ],
        "sublings": []
    },
    "error": null
    }
    
Либо, при условии, что был введен несуществующий идентификатор:
    
    {
    "success": false,
    "result": [],
    "error": "Идентификатор 1000 не существует в базе."
    }
    
### Получение списка всех существующих данных в базе

Запрос:

    GET /api/get_tree/

#### Пример

Запрос:

    GET /api/get_tree/

Ответ:

    {
    "success": true,
    "result": {
        "id": 1,
        "name": "Category 1",
        "children": [
            {
                "id": 2,
                "name": "Category 1.1",
                "children": [
                    {
                        "id": 3,
                        "name": "Category 1.1.1",
                        "children": [
                            {
                                "id": 3,
                                "name": "Category 1.1.1"
                            }
                        ]
                    }
                ]
            },
            {
                "id": 4,
                "name": "Category 1.2",
                "children": [
                    {
                        "id": 4,
                        "name": "Category 1.2"
                    }
                ]
            }
        ]
    },
    "error": null
    }

### Создание категорий

Запрос:

    GET /api/create_tree/
    
Raw:

    {
     "name": "Category 1",
     "children": [
         {
             "name": "Category 1.1",
             "children": [
                 {
                     "name": "Category 1.1.1",
                     "children": []
                 }
             ]   
         },
         {
             "name": "Category 1.2",
             "children": []
         }
      ]   
    }

    

Ответ:

    {
    "success": true,
    "result": {
        "id": 1,
        "name": "Category 1",
        "children": [
            {
                "id": 2,
                "name": "Category 1.1",
                "children": [
                    {
                        "id": 3,
                        "name": "Category 1.1.1",
                        "children": []
                    }
                ]
            },
            {   
                "id": 4,   
                "name": "Category 1.2",
                "children": []
            }
         ]  
       }
     }


### Удаление категорий

Запрос:

    GET /api/delete_tree/<id>
    

Ответ:

    {
    "success": true,
    "result": [],
    "error": null
    }

#### Пример

Запрос:

    GET /api/delete_tree/1

Ответ:

    {
    "success": true,
    "result": [],
    "error": null
    }
    
