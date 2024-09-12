<h1>Users Transaction Simple App</h1>


<h2>Getting started</h2>

1. Clone git repository
```
git clone https://github.com/SerhiiL06/users-transactions.git
```

2. Change current directory
```
cd users-transactions
```

3. Install all dependencies for this project
```
pip install -r requirements.txt
```

4. Rename env file
```
mv .env_example .env
```
5. Enter your database name into the env file and save this
```
nano .env
```

6. Run the project
```
uvicorn main:app --reload
```