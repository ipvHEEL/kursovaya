CREATE DATABASE IF NOT EXISTS `authentication`;

-- Используем созданную базу данных
USE `authentication`;

CREATE TABLE IF NOT EXISTS `authentication_user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NOT NULL UNIQUE,
  `password` VARCHAR(255) NOT NULL,
  `is_admin` BOOLEAN DEFAULT 0,
  `participation_count` INT DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Вставляем данные пользователя admin
INSERT INTO `authentication_user` (`username`, `password`, `is_admin`) VALUES ('admin', 'admin_password', 1);

-- Создаем таблицу турниров
CREATE TABLE IF NOT EXISTS `tournament` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `tournament_name` VARCHAR(255) NOT NULL,
  `date` VARCHAR(255) NOT NULL,
  `prize` VARCHAR(255),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Вставляем данные о турнирах
INSERT INTO `tournament` (`tournament_name`, `date`, `prize`) VALUES
('Malta Vibes #3', '6 - 17 сен 2023', '$50,000'),
('BetBoom Dacha', '7 авг - 16 сен 2023', '$250,000'),
('The International 2023: Квалификации Юго-Восточной Азии', '27 - 31 авг 2023', 'Слот на The International 2023'),
('The International 2023: Квалификации Западной Европы', '27 - 31 авг 2023', 'Слот на The International 2023'),
('DreamLeague S23', '20 мая, 2024', '$1,000,000'),
('ESL One Europe 2024', '22 апреля, 2024', '$1,000,000'),
('DreamLeague S22', '25 февраля, 2024', '$1,000,000');

-- Создаем таблицу команд
CREATE TABLE IF NOT EXISTS `team` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `team_name` VARCHAR(255) NOT NULL,
  `player1` VARCHAR(255) NOT NULL,
  `player2` VARCHAR(255) NOT NULL,
  `player3` VARCHAR(255) NOT NULL,
  `player4` VARCHAR(255) NOT NULL,
  `player5` VARCHAR(255) NOT NULL,
  `tournament_id` INT,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`tournament_id`) REFERENCES `tournament`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
