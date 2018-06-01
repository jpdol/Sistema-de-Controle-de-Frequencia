CREATE SCHEMA `SCF` ;

CREATE TABLE `SCF`.`Laboratorio` (
  `IdLab` INT NOT NULL AUTO_INCREMENT,
  `Nome` VARCHAR(45) NOT NULL,
  `Sigla` VARCHAR(45) NOT NULL,
  UNIQUE INDEX `IdLab_UNIQUE` (`IdLab` ASC),
  PRIMARY KEY (`IdLab`));


CREATE TABLE `SCF`.`Colaborador` (
  `Matricula` INT NOT NULL,
  `Nome` VARCHAR(45) NOT NULL,
  `DtNasc` DATE NOT NULL,
  `CH` INT NOT NULL,
  `DtIngresso` DATE NOT NULL,
  `DtDesligamento` DATE NULL,
  `Status` VARCHAR(45) NOT NULL,
  `Senha` VARCHAR(45) NULL,
  `Funcao` VARCHAR(45) NOT NULL,
  `Instituicao` VARCHAR(45) NULL,
  `NivelAcademico` VARCHAR(45) NULL,
  `IdLab` INT NULL,
  PRIMARY KEY (`Matricula`),
  UNIQUE INDEX `Matricula_UNIQUE` (`Matricula` ASC),
  INDEX `IdLab_idx` (`IdLab` ASC),
  CONSTRAINT `IdLab`
    FOREIGN KEY (`IdLab`)
    REFERENCES `SCF`.`Laboratorio` (`IdLab`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


CREATE TABLE `SCF`.`Frequencias` (
  `DtEntrada` DATE NOT NULL,
  `HrEntrada` TIME NOT NULL,
  `Matricula` INT NOT NULL,
  `Dentro` INT NULL,
  `HrSaida` TIME NULL,
  PRIMARY KEY (`DtEntrada`, `HrEntrada`, `Matricula`),
  INDEX `Matricula_idx` (`Matricula` ASC),
  CONSTRAINT `Matricula`
    FOREIGN KEY (`Matricula`)
    REFERENCES `SCF`.`Colaborador` (`Matricula`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
