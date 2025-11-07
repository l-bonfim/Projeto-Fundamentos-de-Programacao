# Intruções gerais para inicio do projeto

(Instale o git no seu computador https://git-scm.com/book/pt-br/v2/Come%C3%A7ando-Instalando-o-Git)

## 1 - Localize a pasta que você quer baixar o projeto e clone o repositório:

>git clone git@github.com:l-bonfim/projeto-avaliacao-1--introducao-a-computacao.git

## 2 - Crie uma branch pessoal para as suas alterações:

Como boas praticas, você deve criar uma branch para identificar a sua seção,
caso julgue necessario, a partir da sua branch crie novas branchs para as etapas
das sua atividade.

>git checkout -b seu-nome-e-sobrenome-section

### 2.1 - Mantenha sempre seu código atualizado:

Antes de tomar qualquer ação para inciar sua parte do projeto, verifique se os códigos estão atualizados
em relação ao git.

Vá para branch main:

>git checkout main
>git pull

Com esses processos, você garante que estará atualizado com o nosso github, e não jogará fora qualquer progresso
que você já tiver feito, caso programe antes de fazer isso.

Para voltar para sua branch como tudo atualizado:

>git checkout seu-nome-e-sobrenome-section
>git merge main

### 2.2 - Caso divida sua branch em branches de etapas:

Para criar branches para etapas do projeto:

>git checkout -b etapa-exemplo-branch

Você pode commitar (seção 4.2) na branch de etapa, mas lembre-se que você deve fazer o pull request,
a partir da sua branch então, antes de utilizar o:

>git push

Faça:

>git checkout seu-nome-e-sobrenome-section
>git merge etapa-exemplo-branch

## 3 - Para iniciar sua parte:

Nosso foco é um backend bem feito, então quando for programar algo, certifique que o seu terminal está dentro da pasta do backend,
depois de já estar na pasta do projeto:

>cd ./backend

Você terá que ativar o ambiente de desenvolvimento virtual dentro dela, para ter acesso as extensões.

### 3.1 - Ativando o .venv (ambiente virtual de desenvolvimento):

Dentro do nosso backend existe uma pasta chamada ".venv", nela tem todas as biblioteca e dependências que iremos usar,
mas para usa-la é preciso ativa-la:

>./.venv/bin/activate

Fazendo isso você vai habilitar o uso, terminando de programar, desative-a:

>deactivate

Para ativar o endereço de backend, depois de estar no ambiente virtual, utilize:

>flask --app ./src/app run --debug

### 3.2 - Extensão thunder client:

Uma extensão útil para gente é o thunder client, onde podemos testar as requisições do projeto:

>GET POST PUT DELETE

Se você tiver iniciado o backend, o endereço dele será o:

>http://localhost:5000

Para testar um exemplo de funcionamento, voce pode utilizar o que já foi programado em:

>http://localhost:5000/register

No endereço do thunder client, selecione o metodo de POST, e envie um dado qualquer em JSON:

>{
>    "dado de teste": "teste"
>}

Se ele receber o dado e apresentar status de codigo 200, o backend estará recebendo a comunicação em JSON.

### 3.3 - Caso queira mexer com o frontend:

Você precisará do node, e depois acessar a pasta do frontend:

>cd ..

(caso esteja na pasta do backend)

>cd ./frontend

Estando nela, você precisará instalar os pacotes, mas antes de instalar os pacotes, o ideal é que você volte para a
branch main e instale:

>npm install

Após isso, volte para a sua branch e use:

>git merge main
>npm start

Abrirá o navegador "em live", com as páginas do projeto.

## 4 - Seja o mais verboso possível:

Outra boa pratica é nomear as variáveis e funções de acordo com sua utilidade,
por exemplo:

>esta_e_uma_funcao_de_exemplo(): <br/>
>&emsp;aqui_e_uma_variavel_com_o_texto_exemplo = 'exemplo'

estamos nessa em grupo, e quanto mais claro ficar o que você está fazendo,
mais fácil será identificar erros e problemas, e unificar os códigos em um projeto coeso.

### 4.1 - Estaja sempre atento a identação:

Aqui é mais um lembrete, estamos utilizando python, então a identação é muito importante.
Veja se no seu VScode na parte inferior está com "Spaces: 4", significa que seu tab é equivalente a
apertar a barra de espaço 4 vezes.

### 4.2 - Lembre de fazer commits regularmente:

Sempre que você temrinar uma etapa de sua atividade, lembre-se de commitar o código.

>git status

para ver o que você alterou;

>git add .

adiciona todas as alteroções no seu commit;

>git commit -m 'mensagem do commit'

comenta a seção de alterações que você adicionou;

Isso é útil para sabermos o que foi feito, e caso hajam problemas, podemos recuperar o progresso
a partir de algum commit, quando você desejar salvar seu progresso no github, utilize o comando:

>git push -u origin seu-nome-e-sobrenome-section

apenas para a primeira vez, proximos pushs podem ser feito apenas com:

>git push

## 5 - Pair programming:

Provavelmente as atividades serão feitas em duplas, eu gostaria de sugerir a vocês a pratica
da programação em par, chamada de video e compartilhamento de tela de quem estiver escrevendo o código,
caso seja feito assim, adicionem ao fim do commit o nome das pessoas que realizaram a parte:

>git commit -m 'etapa x - feito por fulano 1 e fulano 2'

para identificação das passoas responsáveis pela etapa concluida.

Eu gosto da pratico do pair programming, porque acredito que ajuda a aprender a programar e deixa
mais rapido a identificação de problemas caso ocorram.

## 6 - Sugestões e nosso grupo:

Todos fazem parte do projeto, então sintam-se livres para sugerir ideias, o projeto será melhor
se todos acreditarem no que estão fazendo.

Vamos pro 10,0.
