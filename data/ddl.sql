CREATE TABLE `taipei_day_trip`.`attraction` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `category` VARCHAR(45) NOT NULL,
  `description` TEXT NOT NULL,
  `address` TEXT NOT NULL,
  `transport` TEXT NULL DEFAULT NULL,
  `mrt` VARCHAR(255) NULL DEFAULT NULL,
  `latitude` DOUBLE NOT NULL,
  `longitude` DOUBLE NOT NULL,
  `images` JSON NOT NULL,
  PRIMARY KEY (`id`));
