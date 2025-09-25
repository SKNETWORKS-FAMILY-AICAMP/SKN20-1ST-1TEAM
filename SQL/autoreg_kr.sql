-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema autoreg_kr
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema autoreg_kr
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `autoreg_kr` DEFAULT CHARACTER SET utf8mb3 ;
USE `autoreg_kr` ;

-- -----------------------------------------------------
-- Table `autoreg_kr`.`car_reg_region`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `autoreg_kr`.`car_reg_region` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `ym` VARCHAR(45) NOT NULL,
  `region` VARCHAR(5) NOT NULL,
  `passenger_total` INT NULL DEFAULT NULL,
  `bus_total` INT NULL DEFAULT NULL,
  `truck_total` INT NULL DEFAULT NULL,
  `special_total` INT NULL DEFAULT NULL,
  `total_count` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 4081
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `autoreg_kr`.`faq`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `autoreg_kr`.`faq` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `question` VARCHAR(500) NOT NULL,
  `answer` LONGTEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uq_question` (`question` ASC) VISIBLE,
  UNIQUE INDEX `uq_page_question` (`question`(191) ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 59
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `autoreg_kr`.`fuel_car`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `autoreg_kr`.`fuel_car` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `ym` VARCHAR(45) NOT NULL,
  `car_type` VARCHAR(45) NOT NULL,
  `fuel_type` VARCHAR(45) NOT NULL,
  `car_count` INT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 7849
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `autoreg_kr`.`gender_age_car`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `autoreg_kr`.`gender_age_car` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `year` INT NULL DEFAULT NULL,
  `gender` VARCHAR(45) NOT NULL,
  `age_group` VARCHAR(45) NULL DEFAULT NULL,
  `car_count` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 191
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
