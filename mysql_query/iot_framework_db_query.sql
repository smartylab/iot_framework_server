-- phpMyAdmin SQL Dump
-- version 4.4.10
-- http://www.phpmyadmin.net
--
-- Host: localhost:8889
-- 생성 시간: 16-06-15 10:08
-- 서버 버전: 5.5.42
-- PHP 버전: 5.6.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 데이터베이스: `iot_framework`
--
CREATE DATABASE IF NOT EXISTS `iot_framework` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `iot_framework`;

-- --------------------------------------------------------

--
-- 테이블 구조 `agent`
--

DROP TABLE IF EXISTS `agent`;
CREATE TABLE `agent` (
  `agent_id` int(10) unsigned NOT NULL,
  `agent_name` varchar(255) DEFAULT NULL,
  `agent_address` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 테이블 구조 `context`
--

DROP TABLE IF EXISTS `context`;
CREATE TABLE `context` (
  `context_id` bigint(20) unsigned NOT NULL,
  `device_item_id` int(10) unsigned NOT NULL,
  `type` varchar(255) NOT NULL,
  `time` bigint(20) NOT NULL,
  `extra` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 테이블 구조 `context_data`
--

DROP TABLE IF EXISTS `context_data`;
CREATE TABLE `context_data` (
  `data_id` bigint(20) unsigned NOT NULL,
  `context_id` bigint(20) unsigned NOT NULL,
  `sub_type` varchar(255) DEFAULT NULL,
  `value` double NOT NULL,
  `unit` varchar(255) DEFAULT NULL,
  `time` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 테이블 구조 `device_item`
--

DROP TABLE IF EXISTS `device_item`;
CREATE TABLE `device_item` (
  `item_id` int(10) unsigned NOT NULL,
  `model_id` int(10) unsigned NOT NULL,
  `user_id` varchar(255) NOT NULL,
  `item_name` varchar(255) DEFAULT NULL,
  `item_address` varchar(255) NOT NULL,
  `connected` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 테이블 구조 `device_model`
--

DROP TABLE IF EXISTS `device_model`;
CREATE TABLE `device_model` (
  `model_id` int(10) unsigned NOT NULL,
  `model_name` varchar(255) NOT NULL,
  `model_network_protocol` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 테이블 구조 `series_context`
--

DROP TABLE IF EXISTS `series_context`;
CREATE TABLE `series_context` (
  `context_id` bigint(20) unsigned NOT NULL,
  `device_item_id` int(10) unsigned NOT NULL,
  `type` varchar(255) NOT NULL,
  `time_from` bigint(20) NOT NULL,
  `time_to` bigint(20) NOT NULL,
  `data` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 테이블 구조 `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `user_id` varchar(255) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 덤프된 테이블의 인덱스
--

--
-- 테이블의 인덱스 `agent`
--
ALTER TABLE `agent`
  ADD PRIMARY KEY (`agent_id`);

--
-- 테이블의 인덱스 `context`
--
ALTER TABLE `context`
  ADD PRIMARY KEY (`context_id`);

--
-- 테이블의 인덱스 `context_data`
--
ALTER TABLE `context_data`
  ADD PRIMARY KEY (`data_id`);

--
-- 테이블의 인덱스 `device_item`
--
ALTER TABLE `device_item`
  ADD PRIMARY KEY (`item_id`),
  ADD UNIQUE KEY `item_address_UNIQUE` (`item_address`);

--
-- 테이블의 인덱스 `device_model`
--
ALTER TABLE `device_model`
  ADD PRIMARY KEY (`model_id`);

--
-- 테이블의 인덱스 `series_context`
--
ALTER TABLE `series_context`
  ADD PRIMARY KEY (`context_id`);

--
-- 테이블의 인덱스 `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`);

--
-- 덤프된 테이블의 AUTO_INCREMENT
--

--
-- 테이블의 AUTO_INCREMENT `agent`
--
ALTER TABLE `agent`
  MODIFY `agent_id` int(10) unsigned NOT NULL AUTO_INCREMENT;
--
-- 테이블의 AUTO_INCREMENT `context`
--
ALTER TABLE `context`
  MODIFY `context_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT;
--
-- 테이블의 AUTO_INCREMENT `context_data`
--
ALTER TABLE `context_data`
  MODIFY `data_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT;
--
-- 테이블의 AUTO_INCREMENT `device_item`
--
ALTER TABLE `device_item`
  MODIFY `item_id` int(10) unsigned NOT NULL AUTO_INCREMENT;
--
-- 테이블의 AUTO_INCREMENT `device_model`
--
ALTER TABLE `device_model`
  MODIFY `model_id` int(10) unsigned NOT NULL AUTO_INCREMENT;
--
-- 테이블의 AUTO_INCREMENT `series_context`
--
ALTER TABLE `series_context`
  MODIFY `context_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
