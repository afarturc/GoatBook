# Goatbook 🐐 - TPW Project 1

Este projeto surge como uma sátira ao elevado uso de redes sociais por parte da populção mundial atualmente,
ou por outras palavras, se todas as pessoas usam, porque é que as cabras não podem usar também?

Com esta ideia em mente, o projeto Goatbook foi criado, uma rede social para cabras, onde estas podem fazer posts, 
comentar posts, dar likes, seguir outras cabras, etc.

## Persona

A persona principal deste projeto é uma cabra jovem (Bob, 6 anos), que vive nas montanhas, e que tem um certo interesse em tecnologia e
quer comunicar com as outras cabras das redondezas através de imagens e textos.

![Persona](https://v1centebarros.pythonanywhere.com/media/default.png)

## Requisitos

### Autenticação

Como utilizador, quero:

- poder observar a *homepage* da aplicação sem estar autenticado.
- quero poder autenticar-me.
- quero poder registar-me.
- quero poder ver a minha página de perfil.
- quero poder editar a minha página de perfil.
- quero poder ver a página de perfil de outros utilizadores.
- quero poder seguir/deixar de seguir outros utilizadores.

### Posts

Como utilizador, quero:

- poder criar posts.
- poder editar posts.
- poder apagar posts.
- poder ver os posts de outros utilizadores.

### Comentários

Como utilizador, quero:

- poder comentar posts.
- poder editar comentários.
- poder apagar comentários indesejados nos meus posts.
- poder apagar os meus comentários.

### Likes

Como utilizador, quero:

- poder dar likes a posts.
- poder deixar de dar likes a posts.

### Pesquisa

Como utilizador, quero:

- poder pesquisar por utilizadores.
- ver o resultado da pesquisa.


## Modelo de Dados

### User

| Campo       | Tipo   | Descrição                             |
|-------------|--------|---------------------------------------|
| username    | string | Nome de utilizador                    |
| password    | string | Password do utilizador                |
| profile_pic | string | URL da imagem de perfil do utilizador |
| email       | string | Email do utilizador                   |
| bio         | string | Descrição do utilizador               |


### Follow

| Campo     | Tipo | Descrição               |
|-----------|------|-------------------------|
| user      | User | Utilizador que segue    |
| following | User | Utilizador que a seguir |

### Post

| Campo         | Tipo     | Descrição                   |
|---------------|----------|-----------------------------|
| user          | User     | Utilizador que criou o post |
| image         | string   | URL da imagem do post       |
| likes         | int      | Relacão m:m                 |
| like_count    | int      | Número de likes             |
| comment_count | int      | Número de comentários       |
| date          | datetime | Data de criação do post     |

### Comment

| Campo   | Tipo     | Descrição                         |
|---------|----------|-----------------------------------|
| user    | User     | Utilizador que criou o comentário |
| post    | Post     | Post que o comentário pertence    |
| comment | string   | Comentário                        |
| date    | datetime | Data de criação do comentário     |


## Aspetos relevantes

Com o desenvolvimento deste projeto, uma das maiores dificuldade que apareceu, foi como fazer a relação m:m entre os
users de maneira a não causar problemas de duplicação de dados. Para resolver este problema, foi criada uma tabela
intermédia, a tabela Follow, que contém os utilizadores que seguem e os utilizadores seguidos.

Posteriormente, outro grande desafio foi a implementação do sistema de likes sem forçar o utilizador a dar refresh na
página. Para isso, foi preciso ver como usar o AJAX, com os Django forms.

Por fim, um problema menor encontrado durante o desenvolvimento foi como o Django mostra a data e hora de um
post. Para resolver este problema, o Django tem um template filter que permite formatar a data e hora conforme
o que o utilizador desejar, neste caso a data relativamente ao dia atual.


## Deploy

Este projeto está disponível em: https://v1centebarros.pythonanywhere.com/ e o utilizador utilizado durante a apresentação
tem as seguintes credenciais:


**username**: user

**password**: 123

## Outras tecnologias

- [TailwindCSS](https://tailwindcss.com/)
- [Font Awesome](https://fontawesome.com/)
- [DaisyUI](https://daisyui.com/)
- [jQuery](https://jquery.com/)

## Créditos

- [Artur Correia, 102477](https://github.com/afarturc)
- [Mariana Andrade, 103823](https://github.com/MarianaAndrad)
- [Vicente Barros, 97787](https://github.com/v1centebarros)
