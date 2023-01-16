-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Янв 12 2023 г., 11:44
-- Версия сервера: 8.0.30
-- Версия PHP: 7.4.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `YP`
--

-- --------------------------------------------------------

--
-- Структура таблицы `Auto`
--

CREATE TABLE `Auto` (
  `Number` varchar(9) NOT NULL,
  `BodyID` varchar(17) NOT NULL,
  `EngineID` varchar(20) NOT NULL,
  `Brand` varchar(15) NOT NULL,
  `Model` varchar(15) NOT NULL,
  `Color` varchar(20) NOT NULL,
  `Volume` int NOT NULL,
  `Comment` varchar(100) DEFAULT NULL,
  `Helm` varchar(10) NOT NULL,
  `Drive` varchar(10) NOT NULL,
  `Year` date NOT NULL,
  `TypeBody` varchar(20) NOT NULL,
  `DrivingAway` varchar(3) NOT NULL,
  `DateAway` date DEFAULT NULL,
  `TOid` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `AutoOrg`
--

CREATE TABLE `AutoOrg` (
  `OrgINN` int NOT NULL,
  `OrgChief` varchar(60) NOT NULL,
  `OrgPhone` int NOT NULL,
  `OrgName` varchar(60) NOT NULL,
  `OrgAddress` varchar(100) NOT NULL,
  `AutoNumber` varchar(9) NOT NULL,
  `AutoBodyID` varchar(17) NOT NULL,
  `AutoEngineID` varchar(20) NOT NULL,
  `AutoTOid` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `AutoVladelca`
--

CREATE TABLE `AutoVladelca` (
  `OwnerID` int NOT NULL,
  `OwnerFIO` varchar(60) NOT NULL,
  `OwnerPhone` int NOT NULL,
  `OwnerAddress` varchar(100) NOT NULL,
  `AutoNumber` varchar(9) NOT NULL,
  `AutoBodyID` varchar(17) NOT NULL,
  `AutoEngineID` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `Inspector`
--

CREATE TABLE `Inspector` (
  `InspID` int NOT NULL,
  `InspFIO` varchar(60) NOT NULL,
  `InspDR` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `TOauto`
--

CREATE TABLE `TOauto` (
  `ToID` int NOT NULL,
  `DateSee` date NOT NULL,
  `InspID` varchar(60) NOT NULL,
  `YearTax` int NOT NULL,
  `TOtax` int NOT NULL,
  `Okey` varchar(15) NOT NULL,
  `Reason` varchar(100) DEFAULT NULL,
  `Inspector_InspID` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `ID` int NOT NULL,
  `Step` int NOT NULL,
  `Numberauto` varchar(9) NOT NULL,
  `BodyIDAuto` varchar(17) NOT NULL,
  `EngineIDauto` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `Auto`
--
ALTER TABLE `Auto`
  ADD PRIMARY KEY (`Number`,`BodyID`,`EngineID`,`TOid`),
  ADD KEY `fk_Auto_TOauto1_idx` (`TOid`);

--
-- Индексы таблицы `AutoOrg`
--
ALTER TABLE `AutoOrg`
  ADD PRIMARY KEY (`OrgINN`,`AutoNumber`,`AutoBodyID`,`AutoEngineID`,`AutoTOid`),
  ADD KEY `fk_AutoOrg_Auto1_idx` (`AutoNumber`,`AutoBodyID`,`AutoEngineID`,`AutoTOid`);

--
-- Индексы таблицы `AutoVladelca`
--
ALTER TABLE `AutoVladelca`
  ADD PRIMARY KEY (`OwnerID`,`AutoNumber`,`AutoBodyID`,`AutoEngineID`),
  ADD KEY `fk_AutoVladelca_Auto1_idx` (`AutoNumber`,`AutoBodyID`,`AutoEngineID`);

--
-- Индексы таблицы `Inspector`
--
ALTER TABLE `Inspector`
  ADD PRIMARY KEY (`InspID`);

--
-- Индексы таблицы `TOauto`
--
ALTER TABLE `TOauto`
  ADD PRIMARY KEY (`ToID`,`Inspector_InspID`),
  ADD KEY `fk_TOauto_Inspector1_idx` (`Inspector_InspID`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`ID`,`Numberauto`,`BodyIDAuto`,`EngineIDauto`),
  ADD KEY `fk_users_Auto_idx` (`Numberauto`,`BodyIDAuto`,`EngineIDauto`);

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `Auto`
--
ALTER TABLE `Auto`
  ADD CONSTRAINT `fk_Auto_TOauto1` FOREIGN KEY (`TOid`) REFERENCES `TOauto` (`ToID`);

--
-- Ограничения внешнего ключа таблицы `AutoOrg`
--
ALTER TABLE `AutoOrg`
  ADD CONSTRAINT `fk_AutoOrg_Auto1` FOREIGN KEY (`AutoNumber`,`AutoBodyID`,`AutoEngineID`,`AutoTOid`) REFERENCES `Auto` (`Number`, `BodyID`, `EngineID`, `TOid`);

--
-- Ограничения внешнего ключа таблицы `AutoVladelca`
--
ALTER TABLE `AutoVladelca`
  ADD CONSTRAINT `fk_AutoVladelca_Auto1` FOREIGN KEY (`AutoNumber`,`AutoBodyID`,`AutoEngineID`) REFERENCES `Auto` (`Number`, `BodyID`, `EngineID`);

--
-- Ограничения внешнего ключа таблицы `TOauto`
--
ALTER TABLE `TOauto`
  ADD CONSTRAINT `fk_TOauto_Inspector1` FOREIGN KEY (`Inspector_InspID`) REFERENCES `Inspector` (`InspID`);

--
-- Ограничения внешнего ключа таблицы `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `fk_users_Auto` FOREIGN KEY (`Numberauto`,`BodyIDAuto`,`EngineIDauto`) REFERENCES `Auto` (`Number`, `BodyID`, `EngineID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
