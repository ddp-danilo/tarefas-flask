from flask import Flask, request, jsonify
import json

app = Flask(__name__)
tarefas = [{
    'id': '0',
    'responsavel': 'Dan',
    'tarefa': 'Fazer alguma coisa',
    'status': 'pendente'
}]
# procura uma tarefa com o id requisitado, devolve sua posição ou -1 se não achar
def acha_tarefa(usr_id):
    str_usr_id = str(usr_id)
    pos = -1
    for tar in tarefas:
        pos += 1
        if len(tar) > 0:
            if tar['id'] == str_usr_id:
                return pos
    return -1
# retorna a mensagem de tarefa inexistente.
def men_tar_vazia(tar_pos):
    if tar_pos >= 0:
        return tarefas[tar_pos]
    else:
        return {'Erro': 'Nenhuma tarefa tem o id requisitado.'}
# mostra uma tarefa usando o id e também altera uma tarefa usando o id.
@app.route('/tarefas/<int:usr_id>', methods=['GET', 'POST', 'DELETE'])
def retorna_tarefa(usr_id):
    print(tarefas)
    tar_pos = acha_tarefa(usr_id)
    if request.method == 'GET':
        print(tar_pos)
        response = men_tar_vazia(tar_pos)
    if request.method == 'POST':
        dados = json.loads(request.data)
        if tar_pos >= 0:
            tarefas[tar_pos]['status'] = dados['status']
            response = tarefas[usr_id]
        else:
            response = men_tar_vazia(tar_pos)
    if request.method == 'DELETE':
        if tar_pos >= 0:
           tarefas[tar_pos] = {}
           response = {'mensagem': 'Tarefa removida com sucesso.'}
        else:
            response = men_tar_vazia(tar_pos)
    return jsonify(response)

# mostra uma lista de tarefas e a permite adicionar mais
@app.route('/tarefas', methods=['GET','POST'])
def lista_tarefas():
    if request.method == 'GET':
        response = tarefas
    elif request.method == 'POST':
        dados = json.loads(request.data)
        posicao = len(tarefas)
        dados['id'] = str(posicao)
        tarefas.append(dados)
        mensagem = 'Tarefa adicionada com sucesso. id={}'.format(posicao)
        response = {'mensagem': mensagem}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)