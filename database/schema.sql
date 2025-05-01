-- #####################################################
-- SQL-Skript zur Erstellung des PokeDB-Datenbankschemas
-- Dieses Skript erstellt Tabellen und setzt Beziehungen
-- für die Pokémon-Datenbank (PokeDB). Es umfasst Tabellen
-- für Pokémon, Fähigkeiten, Typen, Attacken und mehr.
-- #####################################################

-- Deaktivierung von Einschränkungen während der Erstellung (temporär)
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';


-- #####################################################
-- Schema PokeDB
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `PokeDB` DEFAULT CHARACTER SET utf8 ;
USE `PokeDB` ;


-- #####################################################
-- Tabelle: profilbild
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `PokeDB`.`profilbild` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `dateiname` VARCHAR(45) NOT NULL,
  `speicherpfad` VARCHAR(255) NULL,
  PRIMARY KEY (`id`)
)
ENGINE = InnoDB;


-- #####################################################
-- Tabelle: pokemon
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `PokeDB`.`pokemon` (
  `id` INT UNSIGNED NOT NULL,
  `profilbild_id` INT UNSIGNED NULL,
  `name` VARCHAR(45) NOT NULL,
  `groesse` DECIMAL(3,1) NULL,
  `gewicht` DECIMAL(5,1) NULL,
  `beschreibung` TEXT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_pokemon_profilbild`
    FOREIGN KEY (`profilbild_id`)
    REFERENCES `PokeDB`.`profilbild` (`id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE
)
ENGINE = InnoDB;


-- #####################################################
-- Table `PokeDB`.`faehigkeit`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `PokeDB`.`faehigkeit` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `beschreibung` TEXT NULL,
  PRIMARY KEY (`id`)
)
ENGINE = InnoDB;


-- #####################################################
-- Tabelle: pokemon_faehigkeit
-- -----------------------------------------------------
-- Diese Zuordnungstabelle speichert, welche Fähigkeiten 
-- einem Pokémon zugewiesen sind.
-- Ein Pokémon kann mehrere Fähigkeiten haben.
-- 'versteckt' kennzeichnet, ob es sich um eine versteckte Fähigkeit handelt.
-- #####################################################
CREATE TABLE IF NOT EXISTS `PokeDB`.`pokemon_faehigkeit` (
  `pokemon_id` INT UNSIGNED NOT NULL,
  `faehigkeit_id` INT UNSIGNED NOT NULL,
  `versteckt` TINYINT NULL DEFAULT 0,
  PRIMARY KEY (`pokemon_id`, `faehigkeit_id`),
  CONSTRAINT `fk_pokemon_faehigkeit_pokemon`
    FOREIGN KEY (`pokemon_id`)
    REFERENCES `PokeDB`.`pokemon` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_pokemon_faehigkeit_faehigkeit`
    FOREIGN KEY (`faehigkeit_id`)
    REFERENCES `PokeDB`.`faehigkeit` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB;


-- #####################################################
-- Tabelle: evolution
-- -----------------------------------------------------
-- Diese Tabelle speichert die Entwicklung von Pokémon.
-- 'basis_pokemon_id' ist das ursprüngliche Pokémon,
-- 'weiterentwicklung_id' ist das Pokémon, in das es sich entwickelt.
-- #####################################################
CREATE TABLE IF NOT EXISTS `PokeDB`.`evolution` (
  `basis_pokemon_id` INT UNSIGNED NOT NULL,
  `weiterentwicklung_id` INT UNSIGNED NOT NULL,
  `bemerkung` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`basis_pokemon_id`, `weiterentwicklung_id`),
  CONSTRAINT `fk_entwicklung_pokemon`
    FOREIGN KEY (`basis_pokemon_id`)
    REFERENCES `PokeDB`.`pokemon` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_evolution_pokemon`
    FOREIGN KEY (`weiterentwicklung_id`)
    REFERENCES `PokeDB`.`pokemon` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE = InnoDB;


-- #####################################################
-- Table `PokeDB`.`typ`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `PokeDB`.`typ` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `beschreibung` TEXT NULL,
  PRIMARY KEY (`id`)
)
ENGINE = InnoDB;


-- #####################################################
-- Table `PokeDB`.`pokemon_typ`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `PokeDB`.`pokemon_typ` (
  `pokemon_id` INT UNSIGNED NOT NULL,
  `typ_id` INT NOT NULL,
  PRIMARY KEY (`pokemon_id`, `typ_id`),
  CONSTRAINT `fk_pokemon_typ_pokemon`
    FOREIGN KEY (`pokemon_id`)
    REFERENCES `PokeDB`.`pokemon` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_pokemon_typ_referenz_typ`
    FOREIGN KEY (`typ_id`)
    REFERENCES `PokeDB`.`typ` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB;


-- #####################################################
-- Tabelle: wechselwirkung
-- -----------------------------------------------------
-- Diese Tabelle speichert die Wechselwirkungen zwischen Pokémon-Typen.
-- Der 'multiplikator' gibt an, wie stark der Typ-Angreifer gegen den Typ-Verteidiger ist.
-- #####################################################
CREATE TABLE IF NOT EXISTS `PokeDB`.`wechselwirkung` (
  `angreifer_typ_id` INT NOT NULL,
  `verteidiger_typ_id` INT NOT NULL,
  `multiplikator` DECIMAL(2,1) NOT NULL,
  PRIMARY KEY (`angreifer_typ_id`, `verteidiger_typ_id`),
  CONSTRAINT `fk_wechselwirkung_angreifer`
    FOREIGN KEY (`angreifer_typ_id`)
    REFERENCES `PokeDB`.`typ` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_wechselwirkung_verteidiger`
    FOREIGN KEY (`verteidiger_typ_id`)
    REFERENCES `PokeDB`.`typ` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB;


-- #####################################################
-- Table `PokeDB`.`attacke`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `PokeDB`.`attacke` (
  `id` SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `beschreibung` TEXT NULL,
  `effekt` VARCHAR(255) NULL,
  `staerke` SMALLINT UNSIGNED NULL,
  `genauigkeit` DECIMAL(2,1) NULL,
  `angriffspunkte` TINYINT UNSIGNED NULL,
  PRIMARY KEY (`id`)
)
ENGINE = InnoDB;


-- #####################################################
-- Table `PokeDB`.`pokemon_attacke`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `PokeDB`.`pokemon_attacke` (
  `pokemon_id` INT UNSIGNED NOT NULL,
  `attacke_id` SMALLINT UNSIGNED NOT NULL,
  PRIMARY KEY (`pokemon_id`, `attacke_id`),
  CONSTRAINT `fk_pokemon_attacke_pokemon`
    FOREIGN KEY (`pokemon_id`)
    REFERENCES `PokeDB`.`pokemon` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_pokemon_attacke_attacke`
    FOREIGN KEY (`attacke_id`)
    REFERENCES `PokeDB`.`attacke` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;