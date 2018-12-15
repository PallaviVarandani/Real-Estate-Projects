#Creating a database
CREATE DATABASE Landis;
USE Landis;

#Creating the table 
CREATE TABLE Mecklenburg(
ListingUrl varchar(255),
ParcelID varchar(255),
AccountNo varchar(255),
LocationAddress varchar(255),
CurrentOwner1 varchar(255),
CurrentOwner2 varchar(255),
MailingAddress varchar(255),
LandUseCode varchar(255),
LandUseDesc varchar(255),
ExemptionOrDeferment varchar(255),
Neighborhood varchar(255),
LegalDescription varchar(255),
Land varchar(255),
LastSaleDate varchar(255),
LastSalePrice varchar(255),
LandValue varchar(255),
BuildingValue varchar(255),
Features varchar(255),
TotalAppraisedValue varchar(255),
HeatedArea varchar(255),
Heat varchar(255),
YearBuilt varchar(255),
Story varchar(255),
BuiltUseorStyle varchar(255),
Fuel varchar(255),
Foundation varchar(255),
ExternalWall varchar(255),
FirePlaces varchar(255),
HalfBaths varchar(255),
FullBaths varchar(255),
Bedrooms varchar(255),
TotalSqFt varchar(255),
Units varchar(255)
);
ALTER TABLE Mechkenbury RENAME TO Mecklenburg;