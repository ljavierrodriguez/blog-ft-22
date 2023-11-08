-- Active: 1699018851359@@127.0.0.1@5433@blogft22@public

INSERT INTO users (username, password) VALUES ('john.doe@gmail.com', '123456'), ('jane.doe@gmail.com', '123456');
INSERT INTO users (username, password) VALUES ('tommy.doe@gmail.com', '123456');
INSERT INTO followers (follower_id, followed_id) VALUES (1, 2), (2, 1);
INSERT INTO followers (follower_id, followed_id) VALUES (5, 1), (5, 2);


INSERT INTO categories (name) VALUES ('Sports'), ('Health'), ('International'), ('National');

INSERT INTO articles (title, slug, resume, content, published, users_id) 
VALUES ('Mi Primer Articulo', 'mi-primer-articulo', 's/n', 'Esto es el contenido', false, 1);

INSERT INTO articles (title, slug, resume, content, published, users_id) 
VALUES ('Mi Segundo Articulo', 'mi-segundo-articulo', 's/n', 'Esto es el contenido', false, 1);


INSERT INTO categories_articles (articles_id, categories_id) VALUES 
(1, 1), 
(1, 4), 
(2, 2), 
(2, 3);