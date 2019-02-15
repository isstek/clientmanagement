CREATE SCHEMA `clientmanagement` DEFAULT CHARACTER SET utf8;

  CREATE TABLE `clientmanagement`.`clientlist` (
    `idclientlist` INT NOT NULL AUTO_INCREMENT,
    `clientname` VARCHAR(55) NOT NULL,
    `adress` VARCHAR(70) NULL DEFAULT NULL,
    `phonenumber` VARCHAR(20) NULL DEFAULT NULL,
    `notes` TEXT(255) NULL DEFAULT NULL,
    PRIMARY KEY (`idclientlist`),
    INDEX `name` (`clientname` ASC) VISIBLE);

  CREATE TABLE `clientmanagement`.`people` (
    `idpeople` INT NOT NULL AUTO_INCREMENT,
    `firstname` VARCHAR(15) NOT NULL,
    `lastname` VARCHAR(15) NOT NULL,
    `email` VARCHAR(45) NOT NULL,
    `phonenumber` VARCHAR(20) NULL,
    `annoyance` TINYINT(1) UNSIGNED NULL,
    PRIMARY KEY (`idpeople`),
    INDEX `firstname` (`firstname` ASC, `lastname` ASC) VISIBLE,
    INDEX `lastname` (`lastname` ASC, `firstname` ASC) VISIBLE);

  CREATE TABLE `clientmanagement`.`entrygrouptypes` (
    `identrygrouptypes` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(45) NOT NULL,
    `ordernumber` TINYINT(1) NULL,
    PRIMARY KEY (`identrygrouptypes`),
    INDEX `name` (`name` ASC) VISIBLE,
    INDEX `order` (`ordernumber` ASC, `name` ASC) VISIBLE);

  CREATE TABLE `clientmanagement`.`entrygroups` (
    `identrygroups` INT NOT NULL AUTO_INCREMENT,
    `identrygrouptypes` INT NOT NULL,
    `idclientlist` INT NOT NULL,
    PRIMARY KEY (`identrygroups`),
    INDEX `idclientlist` (`idclientlist` ASC, `identrygroups` ASC) VISIBLE);

  CREATE TABLE `clientmanagement`.`entrytype` (
  `identrytype` INT NOT NULL AUTO_INCREMENT,
  `typename` VARCHAR(20) NOT NULL,
  `typetablename` VARCHAR(20) NOT NULL,
  `description` VARCHAR(150) NULL,
  PRIMARY KEY (`identrytype`),
  INDEX `typename` (`typename` ASC, `identrytype` ASC) VISIBLE);

  CREATE TABLE `datatypes` (
    `iddatatypes` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(20) NOT NULL,
    `sqlname` varchar(20) NOT NULL,
    `htmlentry` text NOT NULL,
    PRIMARY KEY (`iddatatypes`),
    KEY `type` (`name`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8;