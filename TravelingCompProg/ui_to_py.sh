#!/bin/bash
pyuic5 -x uis/MainForm.ui > forms/MainFormModule/MainForm.py
pyuic5 -x uis/DataChangeForm.ui > forms/DataChangeFormModule/DataChangeClass.py
pyuic5 -x uis/ToursForm.ui > forms/ToursFormModule/ToursFormClass.py
pyuic5 -x uis/NewTourForm.ui > forms/NewTourModule/NewTourClass.py
pyuic5 -x uis/PriceListsForm.ui > forms/PriceListsModule/PriceListsClass.py
pyuic5 -x uis/ChangePointsForm.ui > forms/ChangePointsModule/ChangePointsClass.py
pyuic5 -x uis/TourOrderForm.ui > forms/TourOrderModule/TourOrderClass.py