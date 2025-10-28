# Intruções gerais para inicio do projeto

(Instale o git no seu computador https://git-scm.com/book/pt-br/v2/Come%C3%A7ando-Instalando-o-Git)

## 1 - Localize a pasta que você quer baixar o projeto e clone o repositório:

>git clone git@github.com:l-bonfim/projeto-avaliacao-1--introducao-a-computacao.git

## 2 - Crie uma branch pessoal para as suas alterações:

Como boas praticas, você deve criar uma branch para identificar a sua seção,
caso julgue necessario, a partir da sua branch crie novas branchs para as etapas
das sua atividade.

>git checkout -b seu-nome-e-sobrenome-section

### 2.1 - Caso divida sua branch em outras menores*:

Lembre-se de mergear suas branchs, a branch de sua seção antes de fazer qualquer pull request

## 3 - Seja o mais verboso possível:

Outra boa pratica é nomear as variáveis e funções de acordo com sua utilidade,
por exemplo:

>esta_e_uma_funcao_de_exemplo(): <br/>
>&emsp;aqui_e_uma_variavel_com_o_texto_exemplo = 'exemplo'

estamos nessa em grupo, e quanto mais claro ficar o que você está fazendo,
mais fácil será identificar erros e problemas, e unificar os códigos em um projeto coeso.

### 3.1 - Estajam sempre atentos a identação:

Aqui é mais um lembrete, estamos utilizando python, então a identação é muito importante.
Veja se no seu VScode na parte inferior está com "Spaces: 4", significa que seu tab é equivalente a
apertar a barra de espaço 4 vezes.

### 3.2 - lembre de fazer commits regularmente:

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

## 4 - Pair programming:

Provavelmente as atividades serão feitas em duplas, eu gostaria de sugerir a vocês a pratica
da programação em par, chamada de video e compartilhamento de tela de quem estiver escrevendo o código,
caso seja feito assim, adicionem ao fim do commit o nome das pessoas que realizaram a parte:

>git commit -m 'etapa x - feito por fulano 1 e fulano 2'

para identificação das passoas responsáveis pela etapa concluida.

Eu gosto da pratico do pair programming, porque acredito que ajuda a aprender a programar e deixa
mais rapido a identificação de problemas caso ocorram.

## 5 - Sugestões e nosso grupo:

Todos fazem parte do projeto, então sintam-se livres para sugerir ideias, o projeto será melhor
se todos acreditarem no que estão fazendo.

Vamos pro 10,0.
