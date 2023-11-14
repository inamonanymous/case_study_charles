-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 15, 2023 at 12:14 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `farmerdata_charles`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('616bd7d182c1');

-- --------------------------------------------------------

--
-- Table structure for table `locations`
--

CREATE TABLE `locations` (
  `location_id` int(11) NOT NULL,
  `location_name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `locations`
--

INSERT INTO `locations` (`location_id`, `location_name`) VALUES
(1, 'Mamatid'),
(2, 'Baclaran'),
(3, 'Banay-banay'),
(4, 'Gulod'),
(5, 'San Isidro'),
(6, 'Pulo'),
(7, 'Marinig'),
(8, 'Butong'),
(9, 'Niugan'),
(10, 'Sa tago'),
(11, 'Sa bandang iyon');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `product_id` int(11) NOT NULL,
  `product_name` varchar(255) DEFAULT NULL,
  `product_description` varchar(255) DEFAULT NULL,
  `product_unit` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `product_name`, `product_description`, `product_unit`) VALUES
(1, 'Rice', NULL, 'kg'),
(2, 'Sugar', NULL, 'kg'),
(4, 'Vegetable', NULL, 'kg'),
(9, 'Shabs', '', 'g'),
(10, 'PIW', 'WIP', 'g'),
(11, 'Shabz', '', 'l');

-- --------------------------------------------------------

--
-- Table structure for table `sales_statistics`
--

CREATE TABLE `sales_statistics` (
  `stat_id` int(11) NOT NULL,
  `stat_year` varchar(4) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `location_id` int(11) DEFAULT NULL,
  `sales_volume` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sales_statistics`
--

INSERT INTO `sales_statistics` (`stat_id`, `stat_year`, `product_id`, `location_id`, `sales_volume`) VALUES
(2179, '2023', 4, 1, 12),
(2180, '2022', 1, 2, 50),
(2181, '2022', 2, 2, 70),
(2182, '2022', 4, 2, 200),
(2183, '2023', 1, 8, 15),
(2184, '2023', 2, 6, 417),
(2185, '2023', 9, 1, 1000);

-- --------------------------------------------------------

--
-- Table structure for table `trade_data`
--

CREATE TABLE `trade_data` (
  `trade_id` int(11) NOT NULL,
  `location_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `trade_year` varchar(4) DEFAULT NULL,
  `trade_quantity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `trade_data`
--

INSERT INTO `trade_data` (`trade_id`, `location_id`, `product_id`, `trade_year`, `trade_quantity`) VALUES
(4, 1, 4, '2023', 12),
(5, 2, 1, '2022', 50),
(6, 2, 2, '2022', 70),
(8, 2, 4, '2022', 200),
(9, 8, 1, '2023', 15),
(10, 6, 2, '2023', 417),
(11, NULL, 10, '2023', 500),
(12, 1, 9, '2023', 1000);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `surname` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `login_type` int(11) DEFAULT NULL COMMENT '4096 = admin | 128 = guest',
  `location_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password`, `firstname`, `surname`, `email`, `phone`, `login_type`, `location_id`) VALUES
(12, 'admin', 'password', 'Charles', 'De dios', 'cdedios@domain.com', '09572847182', 4096, 11),
(14, 'adminadmin', 'password', 'Stephen', 'Aguilar', 'stephenonline25@gmail.com', '09566036626', 128, 11);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `locations`
--
ALTER TABLE `locations`
  ADD PRIMARY KEY (`location_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `sales_statistics`
--
ALTER TABLE `sales_statistics`
  ADD PRIMARY KEY (`stat_id`),
  ADD KEY `location_id` (`location_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `trade_data`
--
ALTER TABLE `trade_data`
  ADD PRIMARY KEY (`trade_id`),
  ADD KEY `location_id` (`location_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD KEY `location_id` (`location_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `locations`
--
ALTER TABLE `locations`
  MODIFY `location_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `sales_statistics`
--
ALTER TABLE `sales_statistics`
  MODIFY `stat_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2186;

--
-- AUTO_INCREMENT for table `trade_data`
--
ALTER TABLE `trade_data`
  MODIFY `trade_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `sales_statistics`
--
ALTER TABLE `sales_statistics`
  ADD CONSTRAINT `sales_statistics_ibfk_1` FOREIGN KEY (`location_id`) REFERENCES `locations` (`location_id`),
  ADD CONSTRAINT `sales_statistics_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`);

--
-- Constraints for table `trade_data`
--
ALTER TABLE `trade_data`
  ADD CONSTRAINT `trade_data_ibfk_1` FOREIGN KEY (`location_id`) REFERENCES `locations` (`location_id`),
  ADD CONSTRAINT `trade_data_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`);

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`location_id`) REFERENCES `locations` (`location_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
