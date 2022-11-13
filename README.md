# TPW Project

## Análise de Requisitos
- Autenticação
	- Caso esteja autenticado o user vai ter uma home
	- Caso não esteja autenticado o utilizador consegue ver à msm a página default (home)
- Post
	- Caso esteja autenticado pode fzr um post
	- Caso contrário é redirecionado para a página do login
- Comentário (igual ao post)
- Like (igual ao post)
- Profile
	- Caso n esteja autenticado vai ser igual aos outros
	- Caso esteja vai ter estatísticas do utilizador

## Models

### User
- id
- email 
- usernome
- password
- about
- profile_pic
- followers (m-n)
- following (m-n)

### Post
- id
- data
- titulo
- descrição
- imagem 
- comentarios
- likes (1-m)
- user (m-1)

### Like
- id 
- post (1-1)
- user (1-1)

### Comentario
- id
- texto
- data_relativa
- user (1-1)
- (like)

## Routes
### /
	- logged: /home (following)
	- not logged: /home (popular)
### /login
	- success: /home
	- not succ: erro
### /signin
	- succ: login automático -> /home
	- not succ: erro
### /home
	- following
	- popular
### /perfil

### /post/:id
	- página para ver o post de um id

### GET /post/add
	- form para a pessoa adicionar um post

### POST /post/add
	- resposta do form do lado do servidor

### POST /comment/add
	- adicionar um comentário
