SWGR v0.1

SWGR is open source, app for appraising new and aftermarket cars, based 
on a AI model.

The name SWGR comes from shortening the polish word “szwagier” which means 
“brother-in-law”. Who are oddly often chosen as advisors when it comes to 
purchasing a car. Everyone who has some experience with car sales knows 
exactly what I mean. :)

It is a early stage, evolving project aiming to assist in quick assessing the 
value of new and aftermarket cars in turbulent market. Currently SWGR works 
with the most popular, Polish car marketplace otomoto.pl but it is planed the 
expand its functionality to other platforms. 
The model, for its predictions takes such parameters as car’s model and 
version, production year, mileage, engine, transmission, gearbox type 
and many more. 

The project consists of three main components:
-Scraper for gathering and expanding the dataset needed to train the model.
-Linear regression AI model.
-End user GUI interface.

Disclaimer: The project is not intended for any other purpose than to give a 
rough approximation of a car’s value. And may not take into account some 
important factors. Any purchase or sale decisions are at the responsibility 
of the user.  It is not intended for commercial use.

The project uses the following technologies:
- Beautiful Soup 4 – For data scraping.
- Pandas – For processing acquired data.
- Numpy – For handling data for model training.
- Tensorflow – For creating AI model.
- Tkinter – For creating a user GUI.

Installation:
1.Create a virtual environment on your local machine.
2.Install the following libraries into to virtual environment
- Beautiful Soup 4
- Pandas
- Numpy
- Tensorflow
3.Download all the project files from the ‘main’ branch of the repository:
  https://github.com/GLamotBach/SWGR
4.Copy the files into the virtual environment directory.

The raw dataset file, due to its large size is not included in the repository. 
It is not necessary to run the application. 

To use SWGR:
1. Run “gui.py”.
2. Find an offer from “otomoto.pl” that you want to appraise.
3. Copy its URL into the input field.
4. Click “Wyceń” button.

Future development:
The project is in a very early phase of development and will be expanded over 
time. Plans for the future include but are not limited to:
- Growing the training dataset.
- Fine tuning the model.
- Include more features in the model. (Data is already being collected).
- Making the project compatible with other car market platforms.
- Allowing manually imputing all parameters of the vehicle.
- Best offer search tool.
- Features  for comparing interesting offers.
- Web app version.

Thank you for taking interest into my project. All feedback and/or 
contributions are welcomed and appreciated.   