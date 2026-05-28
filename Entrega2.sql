DROP DATABASE IF EXISTS library_db;
CREATE DATABASE library_db;
USE library_db;

-- tabelas de entidades
CREATE TABLE Cartao_acesso(
	codigo_de_barras INT PRIMARY KEY,
    data_emissao DATE,
    esta_ativo TINYINT(1) -- 0 = não, 1 = sim.
);

CREATE TABLE Usuario(
	matricula INT PRIMARY KEY,
    nome VARCHAR(100),
    telefone VARCHAR(11),
    data_nasc DATE,
    cartao_acesso INT,
    CONSTRAINT FK_CARTAO FOREIGN KEY(cartao_acesso) REFERENCES Cartao_acesso(codigo_de_barras) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Emprestimo(
	id_emprestimo INT PRIMARY KEY AUTO_INCREMENT,
    data_retirada DATE,
    data_devolucao_prevista DATE,
    multa FLOAT,
    foi_devolvido TINYINT(1) DEFAULT 0,
    usuario INT,
    CONSTRAINT FK_USUARIO FOREIGN KEY(usuario) REFERENCES Usuario(matricula) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Livro(
	codigo_de_barras INT PRIMARY KEY,
    nome VARCHAR(60),
    publicacao DATE,
    valor_reposicao DOUBLE
);

CREATE TABLE Autor(
	id_autor INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100),
    nacionalidade VARCHAR(30),
    data_nasc DATE
);

-- tabelas de relacionamentos
CREATE TABLE Livro_has_Emprestimo(
	livro INT,
    emprestimo INT,
    PRIMARY KEY(livro, emprestimo),
    FOREIGN KEY(livro) REFERENCES Livro(codigo_de_barras),
    FOREIGN KEY(emprestimo) REFERENCES Emprestimo(id_emprestimo)
);

CREATE TABLE Autor_has_Livros(
	autor INT,
    livro INT,
    FOREIGN KEY(autor) REFERENCES Autor(id_autor),
    FOREIGN KEY(livro) REFERENCES Livro(codigo_de_barras)
);

-- inserindo os valores nas tabelas
INSERT INTO Cartao_acesso (codigo_de_barras, data_emissao, esta_ativo) VALUES
(1001, '2023-01-15', 1),
(1002, '2023-02-20', 1),
(1003, '2023-03-10', 1),
(1004, '2023-04-05', 1),
(1005, '2023-05-12', 1);

INSERT INTO Usuario (matricula, nome, telefone, data_nasc, cartao_acesso) VALUES
(2167, 'Kauan de Abreu Carvalho', '11988887777', '2002-04-12', 1001),
(2165, 'Julia Seixas Souza', '11977776666', '2001-08-25', 1002),
(502,  'Pedro Henrique dos Santos Araujo', '11966665555', '1999-11-05', 1003),
(2168, 'Ana Carolina Silva', '11955554444', '1995-02-28', 1004),
(2169, 'Carlos Eduardo Souza', '11944443333', '1998-07-16', 1005);

INSERT INTO Livro (codigo_de_barras, nome, publicacao, valor_reposicao) VALUES
(9001, 'Diário de um Banana', '2007-04-01', 39.90),
(9002, 'O Senhor dos Anéis', '1954-07-29', 150.00),
(9003, '1984', '1949-06-08', 35.50),
(9004, 'A Revolução dos Bichos', '1945-08-17', 25.90),
(9005, 'Dom Casmurro', '1899-01-01', 45.90);

INSERT INTO Autor (nome, nacionalidade, data_nasc) VALUES
('Jeff Kinney', 'Americana', '1971-02-19'),
('J.R.R. Tolkien', 'Britânica', '1892-01-03'),
('George Orwell', 'Britânica', '1903-06-25'),
('Machado de Assis', 'Brasileira', '1839-06-21'),
('Clarice Lispector', 'Brasileira', '1920-12-10');

INSERT INTO Emprestimo (data_retirada, data_devolucao_prevista, multa, foi_devolvido, usuario) VALUES
('2023-10-01', '2023-10-15', 0.0, 1, 2167),
('2023-10-05', '2023-10-20', 5.50, 1, 2165),
('2023-10-10', '2023-10-25', 0.0, 0, 502),
('2023-10-15', '2023-10-30', 0.0, 0, 2168),
('2023-10-20', '2023-11-04', 0.0, 0, 2169);

INSERT INTO Livro_has_Emprestimo (livro, emprestimo) VALUES
(9001, 1),
(9002, 2),
(9003, 3),
(9004, 4),
(9005, 5);

INSERT INTO Autor_has_Livros (autor, livro) VALUES
(1, 9001),
(2, 9002),
(3, 9003),
(3, 9004),
(4, 9005);

-- Criando a Role
CREATE ROLE 'bibliotecario';

GRANT SELECT, INSERT ON library_db.Livro TO 'bibliotecario';
GRANT SELECT, INSERT, UPDATE ON library_db.Emprestimo TO 'bibliotecario';

CREATE USER 'jose_alfredo'@'localhost' IDENTIFIED BY 'senha123';
CREATE USER 'maria_souza'@'localhost' IDENTIFIED BY '123senha';

GRANT 'bibliotecario' TO 'jose_alfredo'@'localhost';
GRANT 'bibliotecario' TO 'maria_souza'@'localhost';

SET DEFAULT ROLE 'bibliotecario' TO 'jose_alfredo'@'localhost', 'maria_souza'@'localhost';


-- objetos programáveis

CREATE VIEW emprestimos_atrasados AS
SELECT 
    u.nome AS Nome_Usuario, 
    l.nome AS Titulo_Livro, 
    e.data_devolucao_prevista
FROM Emprestimo e
JOIN Usuario u ON e.usuario = u.matricula
JOIN Livro_has_Emprestimo lhe ON e.id_emprestimo = lhe.emprestimo
JOIN Livro l ON lhe.livro = l.codigo_de_barras
WHERE e.foi_devolvido = 0 AND e.data_devolucao_prevista < CURDATE();

DELIMITER $$

CREATE PROCEDURE registrar_devolucao(IN p_id_emprestimo INT)
BEGIN
    UPDATE Emprestimo
    SET foi_devolvido = 1
    WHERE id_emprestimo = p_id_emprestimo;
END $$

DELIMITER ;

CREATE VIEW calculo_debitos AS
SELECT 
    u.matricula,
    u.nome AS Nome_Usuario,
    l.nome AS Titulo_Livro,
    e.data_devolucao_prevista,
    DATEDIFF(CURDATE(), e.data_devolucao_prevista) AS Dias_Atraso,
    (DATEDIFF(CURDATE(), e.data_devolucao_prevista) * 2.00) AS Valor_Multa_Calculada
FROM Emprestimo e
JOIN Usuario u ON e.usuario = u.matricula
JOIN Livro_has_Emprestimo lhe ON e.id_emprestimo = lhe.emprestimo
JOIN Livro l ON lhe.livro = l.codigo_de_barras
WHERE e.foi_devolvido = 0 AND CURDATE() > e.data_devolucao_prevista;

  
