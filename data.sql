/*
SQLyog Enterprise - MySQL GUI v8.02 RC
MySQL - 5.5.5-10.4.17-MariaDB : Database - python
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`python` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `python`;

/*Table structure for table `admindata` */

DROP TABLE IF EXISTS `admindata`;

CREATE TABLE `admindata` (
  `name` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `admindata` */

insert  into `admindata`(`name`,`address`,`contact`,`email`) values ('Amit Sharma','123 Dadabari','9879879870','a@gmail.com'),('Rahul','33, Dadabari','908765432','r@gmail.com');

/*Table structure for table `doctordata` */

DROP TABLE IF EXISTS `doctordata`;

CREATE TABLE `doctordata` (
  `name` varchar(100) DEFAULT NULL,
  `speciality` varchar(100) DEFAULT NULL,
  `qualification` varchar(200) DEFAULT NULL,
  `t` varchar(100) DEFAULT NULL,
  `mon` varchar(20) DEFAULT NULL,
  `tue` varchar(20) DEFAULT NULL,
  `wed` varchar(20) DEFAULT NULL,
  `thu` varchar(20) DEFAULT NULL,
  `fri` varchar(20) DEFAULT NULL,
  `sat` varchar(20) DEFAULT NULL,
  `sun` varchar(20) DEFAULT NULL,
  `email_of_hospital` varchar(200) DEFAULT NULL,
  `photo` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `doctordata` */

insert  into `doctordata`(`name`,`speciality`,`qualification`,`t`,`mon`,`tue`,`wed`,`thu`,`fri`,`sat`,`sun`,`email_of_hospital`,`photo`) values ('Pankaj Jain','Gastroenterologist','MD','9am to 1pm','yes','no','yes','no','yes','no','no','tt@gmail.com','no'),('Dr Jahanvi Tiwary','Cardiologist','MBBS MD, MS (London)','7 AM tp 9 AM','yes','yes','yes','no','no','no','no','rakeshcal@rediffmail.com','no'),('K C Gupta','General Psychiatrist','MD','2pm to 8pm','yes','no','no','no','yes','yes','no','tt@gmail.com','no'),('Avinash Bansal','General Psychiatrist','MD','9am to 1pm','yes','no','yes','no','yes','no','no','bharat@gmail.com','no'),('K C Gupta','General Psychiatrist','MD','9am to 2pm','yes','yes','yes','yes','yes','yes','no','bharat@gmail.com','no'),('Amit Shignvi','Dentist','MD','8am to 12noon','no','yes','no','yes','no','yes','no','bharat@gmail.com','no');

/*Table structure for table `hospitals` */

DROP TABLE IF EXISTS `hospitals`;

CREATE TABLE `hospitals` (
  `hos_name` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `hospitals` */

insert  into `hospitals`(`hos_name`,`address`,`contact`,`email`,`photo`) values ('Bharat Vikas','Dadabari','1234567890','bharat@gmail.com','1545545959.jpg'),('Kedar Hospital','Sagar Darshan','9099991221','rakeshcal@rediffmail.com','no'),('TT','Talvandi','9876543210','tt@gmail.com','1545545968.jpg');

/*Table structure for table `logindata` */

DROP TABLE IF EXISTS `logindata`;

CREATE TABLE `logindata` (
  `email` varchar(100) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  `usertype` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `logindata` */

insert  into `logindata`(`email`,`password`,`usertype`) values ('a@gmail.com','aa','admin'),('bharat@gmail.com','u','hospital'),('r@gmail.com','r','admin'),('rakeshcal@rediffmail.com','neelam','hospital'),('tt@gmail.com','tt','hospital');

/*Table structure for table `photodata` */

DROP TABLE IF EXISTS `photodata`;

CREATE TABLE `photodata` (
  `email` varchar(100) NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `photodata` */

insert  into `photodata`(`email`,`photo`) values ('a@gmail.com','1543339559.png'),('r@gmail.com','1543324134.png');

/*Table structure for table `doctors` */

DROP TABLE IF EXISTS `doctors`;

/*!50001 DROP VIEW IF EXISTS `doctors` */;
/*!50001 DROP TABLE IF EXISTS `doctors` */;

/*!50001 CREATE TABLE `doctors` (
  `name` varchar(100) DEFAULT NULL,
  `speciality` varchar(100) DEFAULT NULL,
  `qualification` varchar(200) DEFAULT NULL,
  `t` varchar(100) DEFAULT NULL,
  `mon` varchar(20) DEFAULT NULL,
  `tue` varchar(20) DEFAULT NULL,
  `wed` varchar(20) DEFAULT NULL,
  `thu` varchar(20) DEFAULT NULL,
  `fri` varchar(20) DEFAULT NULL,
  `sat` varchar(20) DEFAULT NULL,
  `sun` varchar(20) DEFAULT NULL,
  `hos_name` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `photo` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 */;

/*View structure for view doctors */

/*!50001 DROP TABLE IF EXISTS `doctors` */;
/*!50001 DROP VIEW IF EXISTS `doctors` */;

/*!50001 CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `doctors` AS (select `doctordata`.`name` AS `name`,`doctordata`.`speciality` AS `speciality`,`doctordata`.`qualification` AS `qualification`,`doctordata`.`t` AS `t`,`doctordata`.`mon` AS `mon`,`doctordata`.`tue` AS `tue`,`doctordata`.`wed` AS `wed`,`doctordata`.`thu` AS `thu`,`doctordata`.`fri` AS `fri`,`doctordata`.`sat` AS `sat`,`doctordata`.`sun` AS `sun`,`hospitals`.`hos_name` AS `hos_name`,`hospitals`.`address` AS `address`,`hospitals`.`contact` AS `contact`,`hospitals`.`email` AS `email`,`hospitals`.`photo` AS `photo` from (`doctordata` join `hospitals`) where `doctordata`.`email_of_hospital` = `hospitals`.`email`) */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
