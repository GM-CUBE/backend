# Hola

## SQL Alchemy con Docker

```python
conn_url = 'postgresql+psycopg2://yourUserDBName:yourUserDBPassword@yourDBDockerContainerName/yourDBName'
```


```python
@app.route('/prueba_all/<int:_id>', methods=['GET', 'PUT', 'DELETE'])
@crud_template(request, ['campo1', 'campo2', 'campo3', 'campo4'], ['campo1'])
def prueba_post(_id=None):

    if request.method == 'POST':
        campo1 = request.json['campo1']
        campo2 = request.json['campo2']
        campo3 = request.json['campo3']
        campo4 = request.json['campo4']

    if is_none(_id):
        return jsonify({
            "message": "Datos recibidos correctamente",
            "id": "nada",
            "hola": request.method
        }), 200
    
    else:
        return jsonify({
            "message": "Datos recibidos correctamente",
            "id": _id,
            "hola": request.method
        }), 200
```

```python
TABLE_CLASS_MAP = {
     'activity': Activity,
     'clash': Clash,
     'example': Example,
     'game_question': Game_Question,
     'games': Games,
     'level': Level,
     'paragraph': Paragraph,
     'questions': Questions,
     'shortcut_game': Shortcut_Game,
     'shortcuts': Shortcuts,
     'user': Users
     'queue': Queue
}
```