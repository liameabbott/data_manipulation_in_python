# si601_country_data_analysis

Country data analysis assignment for SI 601, Data Manipulation course with Professor Yuhang Wang at the University of Michigan, Winter 2015

See 'SI601_W15_Homework_1.pdf' file for complete assignment description.

'si601_country_data_analysis.py' Python script reads in economic indicators for various countries from the years 2000-2010 from the 'world_bank_indicators.txt' file and reads in regional classification data for countries from the 'world_bank_regions.txt' file.

The script writes three files:
  - Step 1: A tab-delimited .csv file ('si601_country_data_step1.csv') containing average values for certain indicators for each             country over the years 2000-2010.
  - Step 2: A tab-delimited .csv file ('si601_country_data_step2.csv') containing the same columns found in the Step 1 file, but             also an additional column giving the regional classification of each country.
  - Step 3: A tab-deliited .csv file ('si601_country_data_step3.csv') containing each region and the country in the region with             the highest average population in the years 2000-2010.

Also included in the repository is a plot ('si601_country_data_plot.pdf') showing the relationship between average birth rate and average urban population for the countries in the dataset.
