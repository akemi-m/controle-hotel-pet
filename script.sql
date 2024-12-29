-- Esse script vale para o MySQL 8.x. Se seu MySQL for 5.x, precisa executar essa linha comentada:
-- CREATE DATABASE IF NOT EXISTS `hotel-pet`;
CREATE DATABASE IF NOT EXISTS `hotel-pet` DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_0900_ai_ci;

USE `hotel-pet`;

CREATE TABLE pets (
   id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
   nome_tutor varchar(50) NOT NULL,
   tipo_pet varchar(8) NOT NULL,
   nome_pet varchar(50) NOT NULL,
   raca_pet varchar(50) NOT NULL,
   porte_pet varchar(7) NOT NULL,
   hospedado varchar(3) NOT NULL,
   qtd_dias INT NOT NULL,
   historico_qtd_hospedagem INT NOT NULL,
   observacoes varchar(50) NOT NULL,
   UNIQUE KEY nome_UN (nome_tutor)
);