CREATE TABLE `clients` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `share_ip` varchar(45) DEFAULT NULL,
  `view_ip` varchar(45) DEFAULT NULL,
  `password` varchar(45) NOT NULL,
  `port` varchar(45) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `port_UNIQUE` (`port`),
  UNIQUE KEY `password_UNIQUE` (`password`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;