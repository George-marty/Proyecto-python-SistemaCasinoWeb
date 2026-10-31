-- =====================================================
-- Proyecto: Casino Virtual
-- Base: MySQL / MariaDB (sin "VISIBLE", compatible con ambos)
-- Basado en el export original de Workbench; se mantienen
-- los nombres de tablas y columnas del diagrama.
-- =====================================================

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema Casino_Virtual
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Casino_Virtual` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `Casino_Virtual`;

-- -----------------------------------------------------
-- Table `Usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Casino_Virtual`.`Usuario` (
  `idUsuario` INT NOT NULL AUTO_INCREMENT,
  `rol` ENUM('Jugador', 'Administrador') NOT NULL DEFAULT 'Jugador',
  `correo` VARCHAR(120) NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`idUsuario`),
  UNIQUE INDEX `correo_UNIQUE` (`correo`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Usuario_Detalle` (1:1 con Usuario)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Casino_Virtual`.`Usuario_Detalle` (
  `Usuario_idUsuario` INT NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  `telefono` VARCHAR(45) NOT NULL,
  `direccion` VARCHAR(45) NOT NULL,
  `fecha_nacimiento` DATE NOT NULL,
  PRIMARY KEY (`Usuario_idUsuario`),
  CONSTRAINT `fk_Usuario_Detalle_Usuario`
    FOREIGN KEY (`Usuario_idUsuario`)
    REFERENCES `Casino_Virtual`.`Usuario` (`idUsuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Billetera` (1:1 con Usuario)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Casino_Virtual`.`Billetera` (
  `idBilletera` INT NOT NULL AUTO_INCREMENT,
  `saldo_virtual` INT NOT NULL DEFAULT 0,
  `saldo_casual` INT NOT NULL DEFAULT 0,
  `ultima_actualizacion` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `Usuario_idUsuario` INT NOT NULL,
  PRIMARY KEY (`idBilletera`),
  UNIQUE INDEX `Usuario_idUsuario_UNIQUE` (`Usuario_idUsuario`),
  CONSTRAINT `fk_Billetera_Usuario1`
    FOREIGN KEY (`Usuario_idUsuario`)
    REFERENCES `Casino_Virtual`.`Usuario` (`idUsuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Tarjeta` (un usuario puede tener varias)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Casino_Virtual`.`Tarjeta` (
  `idTarjetas` INT NOT NULL AUTO_INCREMENT,
  `tipo` ENUM('VISA', 'MASTERCARD') NOT NULL,
  `numero_tarjeta` VARCHAR(16) NOT NULL,
  `fecha_vencimiento` DATE NOT NULL,
  `Usuario_idUsuario` INT NOT NULL,
  PRIMARY KEY (`idTarjetas`),
  INDEX `fk_Tarjeta_Usuario1_idx` (`Usuario_idUsuario`),
  CONSTRAINT `fk_Tarjeta_Usuario1`
    FOREIGN KEY (`Usuario_idUsuario`)
    REFERENCES `Casino_Virtual`.`Usuario` (`idUsuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Juego`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Casino_Virtual`.`Juego` (
  `idJuego` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `tipo` VARCHAR(45) NOT NULL,
  `apuesta_minima` INT NOT NULL DEFAULT 1,
  `activo` TINYINT NOT NULL DEFAULT 1,
  PRIMARY KEY (`idJuego`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Partida`
-- partida_finalizada es NULL mientras la partida sigue en curso
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Casino_Virtual`.`Partida` (
  `idPartidas` INT NOT NULL AUTO_INCREMENT,
  `inicio_partida` DATETIME NOT NULL,
  `partida_finalizada` DATETIME NULL,
  `Juego_idJuego` INT NOT NULL,
  PRIMARY KEY (`idPartidas`),
  INDEX `fk_Partida_Juego1_idx` (`Juego_idJuego`),
  CONSTRAINT `fk_Partida_Juego1`
    FOREIGN KEY (`Juego_idJuego`)
    REFERENCES `Casino_Virtual`.`Juego` (`idJuego`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Apuesta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Casino_Virtual`.`Apuesta` (
  `idApuesta` INT NOT NULL AUTO_INCREMENT,
  `monto_apostado` INT NOT NULL DEFAULT 0,
  `monto_apostado_casual` INT NOT NULL DEFAULT 0,
  `Usuario_idUsuario` INT NOT NULL,
  `Partidas_idPartidas` INT NOT NULL,
  PRIMARY KEY (`idApuesta`),
  INDEX `fk_Apuesta_Usuario1_idx` (`Usuario_idUsuario`),
  INDEX `fk_Apuesta_Partida1_idx` (`Partidas_idPartidas`),
  CONSTRAINT `fk_Apuesta_Usuario1`
    FOREIGN KEY (`Usuario_idUsuario`)
    REFERENCES `Casino_Virtual`.`Usuario` (`idUsuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Apuesta_Partida1`
    FOREIGN KEY (`Partidas_idPartidas`)
    REFERENCES `Casino_Virtual`.`Partida` (`idPartidas`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Resultado` (1:1 con Apuesta)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Casino_Virtual`.`Resultado` (
  `idResultado` INT NOT NULL AUTO_INCREMENT,
  `monto_ganado` INT NOT NULL DEFAULT 0,
  `monto_ganado_casual` INT NOT NULL DEFAULT 0,
  `Apuesta_idApuesta` INT NOT NULL,
  PRIMARY KEY (`idResultado`),
  UNIQUE INDEX `Apuesta_idApuesta_UNIQUE` (`Apuesta_idApuesta`),
  CONSTRAINT `fk_Resultado_Apuesta1`
    FOREIGN KEY (`Apuesta_idApuesta`)
    REFERENCES `Casino_Virtual`.`Apuesta` (`idApuesta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Transaccion_Financiera`
-- Tarjeta_idTarjetas es NULL cuando la transaccion no usa tarjeta
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Casino_Virtual`.`Transaccion_Financiera` (
  `idTransacciones_Financieras` INT NOT NULL AUTO_INCREMENT,
  `tipo` ENUM('RETIRO', 'DEPOSITO') NOT NULL,
  `monto` INT NOT NULL,
  `estado` ENUM('Finalizado', 'No Finalizado', 'Pendiente') NOT NULL,
  `fecha` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Billetera_idBilletera` INT NOT NULL,
  `Tarjeta_idTarjetas` INT NULL,
  PRIMARY KEY (`idTransacciones_Financieras`),
  INDEX `fk_Transaccion_Financiera_Billetera1_idx` (`Billetera_idBilletera`),
  INDEX `fk_Transaccion_Financiera_Tarjeta1_idx` (`Tarjeta_idTarjetas`),
  CONSTRAINT `fk_Transaccion_Financiera_Billetera1`
    FOREIGN KEY (`Billetera_idBilletera`)
    REFERENCES `Casino_Virtual`.`Billetera` (`idBilletera`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Transaccion_Financiera_Tarjeta1`
    FOREIGN KEY (`Tarjeta_idTarjetas`)
    REFERENCES `Casino_Virtual`.`Tarjeta` (`idTarjetas`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
