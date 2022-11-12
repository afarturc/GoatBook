[x]Home (alterar depois)
[x]login
[x]logout
[x]criar nova conta
[x]profile
[x]editar perfil

[x]adicionar post 
[x]editar post 
[x]remover post

[x]adicionar comment
[x]remover comment (quem fez o post e quem comentou)

[x]adicionar like post
[x]remover like post
[]adicionar like home
[]adicionar like home

[]search 

[x]colocar imagem default no perfil
[]pagina Erro
[]frontend


[]follow 
[]unfollow

[]limpar dados
[]limpar codigo
[]colocar novos dados 



## Redirecionamentos 
### sem login
/home
/logout --- redirecionado login
/signup
/login

/profile -- redirecionado login
/profile/username
/profile/username/edit -- redirecionado login

/post/:id
/post/:id/comment --- redirecionado login
/post/:id/like --- redirecionado login
/post/:id/delete --- redirecionado login
/post/:id/edit --- redirecionado login

like ??? feito por causa do ajax
post/:id/comment/:id/delete --- redirecionado login



### com login
/home
/logout 
/login -- redirecionado home
/signup -- redirecionado home

/profile
/profile/username 
/profile/username/edit -- se for do proprio user(redirecionado form editprofile)
[] /profile/username/edit -- se for de outro user(redirecionado profile/username)

/post/:id
/post/:id/comment -- redirecionado post
/post/:id/like -- redirecionado post
/post/:id/delete -- se feito pelo proprio user (redirecionado profile) 
[] /post/:id/delete -- se nao for feito pelo proprio user (redirecionado post)
/post/:id/edit -- se feito pelo proprio user (redirecionado profile)
[] /post/:id/edit -- se nao for feito pelo proprio user (redirecionado post)
like ??? feito por causa do ajax
post/:id/comment/:id/delete -- redirecionado post

