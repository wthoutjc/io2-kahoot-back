USE `io-db`;

SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS `students` CASCADE;

CREATE TABLE `students`(
	`k_students` BIGINT NOT NULL,
	`n_nombre` LONGTEXT NOT NULL,
	`n_apellido` LONGTEXT NOT NULL,
	`q_correo` LONGTEXT NOT NULL
);

/* PRIMARY KEYS */

ALTER TABLE `students` ADD CONSTRAINT `PK_k_students` PRIMARY KEY (k_students);

/* CHECKS */

/* ALTER TABLE `users` ADD CONSTRAINT `CK_n_categoria` CHECK (n_categoria in ('Admin', 'Vendedor')); */

SET FOREIGN_KEY_CHECKS=1; 
	