from flask import Flask, render_template, request, url_for, redirect, session

app = Flask(__name__)

compromissos = []

metas = []

app.secret_key = 'sua_chave_secreta'

# Rota para a Página Inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para Carteira
@app.route('/carteira', methods=['GET', 'POST'])
def carteira():
    if 'carteira' not in session:
        session['carteira'] = 1000

    if request.method == 'POST':
        action = request.form['action']

        if action == 'adicionar':
            # Ação de adicionar dinheiro
            valor_adicionar = float(request.form['valor_adicionar'])
            session['carteira'] += valor_adicionar
        elif action == 'excluir':
            # Ação de excluir dinheiro
            valor_excluir = float(request.form['valor_excluir'])
            session['carteira'] -= valor_excluir  # Permitir saldo negativo
    return render_template('carteira.html', carteira=session['carteira'])

# Rota para Compromissos Financeiros
@app.route('/compromissos')
def compromissos():
    return render_template('compromissos.html', compromissos=compromissos)

# Rota para Metas
@app.route('/metas', methods=['GET', 'POST'])
def metas_page():
    if request.method == 'POST':
        opcao_metas = int(request.form['opcao_metas'])

        if opcao_metas == 1:
            return render_template('adicionar_meta.html')
        elif opcao_metas == 2:
            return render_template('editar_meta.html')
            # ... lógica para editar a meta ...
        elif opcao_metas == 3:
            return render_template('excluir_meta.html')
            # ... lógica para excluir a meta ...
        elif opcao_metas == 4:
            return render_template('visualizar_meta.html', metas=metas)
        elif opcao_metas == 5:
            return render_template('index.html')
    return render_template('metas.html')

@app.route('/adicionar_meta', methods=['POST'])
def adicionar_meta():
    nome_meta = request.form['nome_meta']
    prazo_meta = request.form['prazo_meta']
    valor_meta = float(request.form['valor_meta'])

    nova_meta = {'Nome': nome_meta, 'Prazo': prazo_meta, 'Valor': valor_meta}
    metas.append(nova_meta)

    return render_template('adicionar_meta.html', nova_meta=nova_meta)


@app.route('/editar_meta', methods=['GET', 'POST'])
def editar_meta():
    if request.method == 'POST':
        nome_meta_editar = request.form['nome_meta_editar']
        novo_nome_meta = request.form['novo_nome_meta']
        novo_prazo_meta = request.form['novo_prazo_meta']
        novo_valor_meta = float(request.form['novo_valor_meta'])

        # Lógica para encontrar e editar a meta
        for meta in metas:
            if meta['Nome'] == nome_meta_editar:
                meta['Nome'] = novo_nome_meta
                meta['Prazo'] = novo_prazo_meta
                meta['Valor'] = novo_valor_meta
                break

        return render_template('editar_meta.html', meta=meta)

    return render_template('editar_meta.html')


@app.route('/excluir_meta', methods=['POST'])
def excluir_meta():
    nome_meta_excluir = request.form['nome_meta_excluir']

    # Lógica para encontrar e excluir a meta
    for meta in metas:
        if meta['Nome'] == nome_meta_excluir:
            metas.remove(meta)
            break

    return render_template('excluir_meta.html', meta=meta)


# Rota para Emergências
@app.route('/emergencias', methods=['GET', 'POST'])
def emergencias():
    if 'emergencias' not in session:
        session['emergencias']= 1000

    if request.method == 'POST':
        action = request.form['action']
        if action == 'adicionar':
            # Ação de adicionar dinheiro
            valor_adicionar = float(request.form['valor_adicionar'])
            session['emergencias'] += valor_adicionar
        elif action == 'resgatar':
            # Ação de resgatar dinheiro
            valor_resgatar = float(request.form['valor_resgatar'])
            session['emergencias'] -= valor_resgatar  # Permitir saldo negativo
    return render_template('emergencias.html', saldo=session['emergencias'])

# Rota para Dinheiro Livre
@app.route('/dinheiro_livre')
def dinheiro_livre():
    carteira_dinheiro_livre = 0.0
    mensagem = ''

    if request.method == 'POST':
        opcao_dinheiro_livre = int(request.form['opcao_dinheiro_livre'])

        if opcao_dinheiro_livre == 1:
            valor_adicional = float(request.form['valor_adicional'])
            carteira_dinheiro_livre = carteira_dinheiro_livre + valor_adicional
            mensagem = f"Novo saldo de dinheiro livre: {carteira_dinheiro_livre}"
            return render_template('gerenciar_dinheiro.html', mensagem=mensagem)

        elif opcao_dinheiro_livre == 2:
            if carteira_dinheiro_livre > 0:
                valor_utilizado = float(request.form['valor_utilizado'])
                if carteira_dinheiro_livre >= valor_utilizado:
                    carteira_dinheiro_livre -= valor_utilizado
                    mensagem = f"Dinheiro livre utilizado. Novo saldo: {carteira_dinheiro_livre}"
                    return render_template('gerenciar_dinheiro.html', carteira_dinheiro_livre=carteira_dinheiro_livre,
                                           mensagem=mensagem)
                else:
                    mensagem = "Saldo insuficiente de dinheiro livre."
                    return render_template('gerenciar_dinheiro.html', carteira_dinheiro_livre=carteira_dinheiro_livre,
                                           mensagem=mensagem)
            else:
                mensagem = "Sem dinheiro livre disponível."
                return render_template('gerenciar_dinheiro.html', carteira_dinheiro_livre=carteira_dinheiro_livre,
                                       mensagem=mensagem)

        elif opcao_dinheiro_livre == 3:
            mensagem = f"Saldo de dinheiro livre disponível: {carteira_dinheiro_livre}"
            return render_template('gerenciar_dinheiro.html', mensagem=mensagem)

    return render_template('gerenciar_dinheiro.html', mensagem=mensagem,
                    carteira_dinheiro_livre=carteira_dinheiro_livre)

    # Adicione lógica para dinheiro livre conforme necessário
    return render_template('dinheiro_livre.html')

# Rota para Dicas
@app.route('/dicas')
def dicas():
    # Adicione lógica para dicas conforme necessário
    return render_template('dicas.html')

# Rota para Gráficos
@app.route('/graficos')
def graficos():
    # Adicione lógica para gráficos conforme necessário
    return render_template('graficos.html')

if __name__ == '__main__':
        app.run(debug=True)

