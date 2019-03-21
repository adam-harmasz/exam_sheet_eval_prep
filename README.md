# EXAM SHEET PREPARATION AND EVALUATION REST API

This is an application to help with the process of preparing and evaluating exams. User(teacher)
can prepare schema of the exam and make as many copies as he needs to, and then after student
finished his test, he'll see score of the closed tasks, and answers of open tasks.

### GETTING STARTED

2. Download  
    - You need to clone repository to your local destination  
    `$ cd path/to/your/workspace`  
    `https://github.com/henryy07/exam_sheet_eval_prep.git`
    - if you have established ssh connection to github you can use this link to clone repo:  
    `git@github.com:henryy07/exam_sheet_eval_prep.git`  
1. To run this application you need to have installed docker and docker-compose, 
if you don't have it already, please visit this sites for further instruction:  
    - [docker](https://docs.docker.com/ee/supported-platforms/)  
    - [docker-compose](https://github.com/Yelp/docker-compose/blob/master/docs/install.md)  
2. If you have docker applications installed type this commands to build docker container:  
`docker build .`  
`docker-compose build`  
3. After that run migrations, and load data from fixtures with this command:  
`python manage.py loaddata core/fixture/initial.json`
4. It's good idea to create superuser:  
`python manage.py createsuperuser`

### USAGE

This application has 4 parts:  

    1. User management - I chose djoser to handle user management for my app, important endpoints for this app:  
        - 'auth/user-create/'  
        - 'auth/token/login'    
        
    2. Endpoints for teacher(user with teacher flag):  
        - '/exam/api/v1/exam_sheets/', here you can create your exam schema  
        - '/exam/api/v1/task_sheets/', here you can assign tasks for your schema  
        - '/exam/api/v1/answer_sheets/', here you can assign answers to tasks  
        
    3. Endpoints mostly for users who will attend to such exam(students?):  
        - '/exam/api/v1/exam_student/', exams ready to be assigned to an user  
        - '/exam/api/v1/task_student/', tasks assigned to exam, filled with necessary data, ready to be completed by user  
        - '/exam/api/v1/open_task_student/', tasks assigned to exam, filled with necessary data, ready to be completed by user  
        - '/exam/api/v1/answer_student/', answers assigned to tasks  

    4. Endpoints to evaluate exam:
        - '/exam/api/v1/exam_eval/', endpoint with exams which are ready for evaluation
        - '/exam/api/v1/student_grade/', endpoint with students/users grades
        - '/exam/api/v1/task_eval/', enpoint with open tasks which are ready to be evaluated  
        
To create exam schema and evaluate it:  
    - You need to choose name of the schema and number of copies you require  
    - Assign tasks to your exam   
    - Assign answers to your tasks(not open ones)  
    - If your exam is ready, click on checkbox "is finished", every update on the object with this status will create exams     
    - After that process students can attend to these exams, if user finished all of the tasks, he needs to click on checkbox "is finished"  
    - After that sheet for evaluation is created with assigned open tasks ready to be checked, points are automatically sumed.
    - If teacher finished evaluation of the exam he can rate it(it's necessary to choose grade)
    - After exam evaluation grade is assigned to the student/user 