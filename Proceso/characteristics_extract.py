import pandas as pd
import numpy as np
import csv
import re
import json

class ReadWrite_Files: 

	def write_in_csv(path,df):
		df.to_csv(path, index=False,header= False)
	def read_csv(path):
		characteristicsArray = []
		with open(path, newline='') as File:
			reader = csv.reader(File)
			for row in reader:
				characteristicsArray.append(row)
		return characteristicsArray

class Get_Characteristics: 
	def get_csv_characteristics():
		CSV_PATH = "C:/Users/bryan/Documents/GitHub/Filogenia-Triatominae/filesData.csv"
		df_complete = pd.read_csv(CSV_PATH)
		df_ordered = df_complete.sort_values(by=['name'], ascending=True)
		df_ordered['name'] = df_ordered['name'].str.lstrip()
		df_ordered['name'] = df_ordered['name'].str.rstrip()
		df_ordered['name'] = df_ordered['name'].str.replace('  ', ' ')
		df_ordered = df_ordered.sort_values(by=['name'], ascending=True)
		df_cut = df_ordered.groupby([df_ordered.name]).agg({'0.txt':'sum', '1.txt':'sum', '2.txt':'sum', '3.txt':'sum', '4.txt':'sum', '5.txt':'sum', '6.txt':'sum', '7.txt':'sum', '8.txt':'sum', '9.txt':'sum', '10.txt':'sum', '11.txt':'sum', '12.txt':'sum', '13.txt':'sum', '14.txt':'sum', '15.txt':'sum', '16.txt':'sum', '17.txt':'sum', '18.txt':'sum', '19.txt':'sum', '20.txt':'sum', '21.txt':'sum', '22.txt':'sum', '23.txt':'sum', '24.txt':'sum', '25.txt':'sum', '26.txt':'sum', '27.txt':'sum', '28.txt':'sum', '29.txt':'sum', '30.txt':'sum', '31.txt':'sum', '32.txt':'sum', '33.txt':'sum', '34.txt':'sum', '35.txt':'sum', '36.txt':'sum', '37.txt':'sum', '38.txt':'sum', '39.txt':'sum', '40.txt':'sum', '41.txt':'sum', '42.txt':'sum', '43.txt':'sum', '44.txt':'sum', '45.txt':'sum', '46.txt':'sum', '47.txt':'sum', '48.txt':'sum', '49.txt':'sum', '50.txt':'sum', '51.txt':'sum', '52.txt':'sum', '53.txt':'sum', '54.txt':'sum', '55.txt':'sum', '56.txt':'sum', '57.txt':'sum', '58.txt':'sum', '59.txt':'sum', '60.txt':'sum', '61.txt':'sum', '62.txt':'sum', '63.txt':'sum', '64.txt':'sum', '65.txt':'sum', '66.txt':'sum', '67.txt':'sum', '68.txt':'sum', '69.txt':'sum', '70.txt':'sum', '71.txt':'sum', '72.txt':'sum', '73.txt':'sum', '74.txt':'sum', '75.txt':'sum', '76.txt':'sum', '77.txt':'sum', '78.txt':'sum', '79.txt':'sum', '80.txt':'sum', '81.txt':'sum', '82.txt':'sum', '83.txt':'sum', '84.txt':'sum', '85.txt':'sum', '86.txt':'sum', '87.txt':'sum', '88.txt':'sum', '89.txt':'sum', '90.txt':'sum', '91.txt':'sum', '92.txt':'sum', '93.txt':'sum', '94.txt':'sum', '95.txt':'sum', '96.txt':'sum', '97.txt':'sum', '98.txt':'sum', '99.txt':'sum', '100.txt':'sum', '101.txt':'sum', '102.txt':'sum', '103.txt':'sum', '104.txt':'sum', '105.txt':'sum', '106.txt':'sum', '107.txt':'sum', '108.txt':'sum', '109.txt':'sum', '110.txt':'sum', '111.txt':'sum', '112.txt':'sum', '113.txt':'sum', '114.txt':'sum', '115.txt':'sum', '116.txt':'sum', '117.txt':'sum', '118.txt':'sum', '119.txt':'sum', '120.txt':'sum', '121.txt':'sum', '122.txt':'sum', '123.txt':'sum', '124.txt':'sum', '125.txt':'sum', '126.txt':'sum', '127.txt':'sum', '128.txt':'sum', '129.txt':'sum', '130.txt':'sum'}).reset_index().reindex(columns=df_ordered.columns)
		df_cut['name'].replace(regex=True,inplace=True,to_replace=r'^[a-z][\d\w\W\D\s]+',value=r'nan')
		df_cut['name'].replace(regex=True,inplace=True,to_replace=r'^\s',value=r'nan')
		df_cut['name'].replace(regex=True,inplace=True,to_replace=r'',value=r'nan')
		df_cut = df_cut[df_cut.name != 'nan']
		df_sum = df_cut
		df_aux = df_sum._get_numeric_data()
		df_aux[df_aux > 1] = 1
		df_sum['sum'] = df_sum[:][df_sum.columns].sum(1)
		df_result = pd.DataFrame({'name': df_sum['name'],'sum':df_sum['sum']})
		df_condition = df_result[df_result['sum']>25 ]
		df_condition =df_condition[df_condition['sum']< 132 ]
		ReadWrite_Files.write_in_csv("Clasified_characteristics2.csv",df_condition)

	
	
def main():
	#Segunda fase
	Get_Characteristics.get_csv_characteristics()


	
if __name__ == "__main__":
    main()