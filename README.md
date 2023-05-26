### Truck API <br>
<p>
<img src="https://www.django-rest-framework.org/img/logo.png" title="Django" height="100"/>
</p>

**Не забудьте отредактировать файл .env**

**Собрать и запустить контейнер**        
```docker-compose up -d --build```

**Установка зависимостей**    
```pip install -r requirements.txt```    

**Изменение рабочего каталога на директорию с приложением**       
```cd truck_api```    

**Запуск миграций для создания базовых локаций и машин**     
```python manage.py migrate```   

**Создание суперпользователя**      
```python manage.py createsuperuser```   

**Запуск приложения**      
```python manage.py runserver```        

**Запуск планировщика для обновления локаций машин**        
```
celery -A truck_api beat -l info --logfile=celery.beat.log --detach
celery -A truck_api worker -l info --logfile=celery.log --detach
```

**Описание документации:** http://127.0.0.1:8000/swagger/  <br>

**Просмотр, добавление грузов:** http://127.0.0.1:8000/api/v1/goods/  <br> 
*Возможна фильтрация по критериям max_distance и weight.*<br> 
```
http://127.0.0.1:8000/api/v1/goods/?weight=20&max_distance=100 
```
Такой запрос выведет грузы с весом до 20 включительно и с машинами в радиусе 100 миль вклчительно. <br> 
<br> **Просмотр, изменение, удаление груза:** 
```http://127.0.0.1:8000/api/v1/goods/{pk}/ ``` <br>
*Возможна фильтрация по критериям max_distance и capacity.*<br>
```127.0.0.1:8000/api/v1/goods/3/?max_distance=500&capacity=50```
Такой запрос выведет груз с id=3 и машины в радиусе 100 миль включительно с грузоподъемностью 50 включительно. <br> 

**Просмотр, изменение машины:** 
```http://127.0.0.1:8000/api/v1/truck/{pk}}/```
