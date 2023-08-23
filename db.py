import mysql.connector

class DB:
    def __init__(self):
        # connect to the database
        try:
            self.conn = mysql.connector.connect(
                host= "127.0.0.1",
                user='root',
                password = "mysql",
                database = "temp"

            )
            self.mycursor = self.conn.cursor()
            print('Connection established')
        except:
            print('Connection error')

    def fetch_all_city(self):
        city = []
        self.mycursor.execute(""" 
        SELECT DISTINCT(Origin) FROM flight
        UNION 
        SELECT DISTINCT(Destination) FROM flight""")

        data = self.mycursor.fetchall()

        for item in data:
            city.append(item[0])

        return city

    def fetch_all_flights(self,source,destination):
        self.mycursor.execute("""
        SELECT * FROM flight
        WHERE Origin = '{}' AND Destination = '{}' """.format(source,destination))

        data = self.mycursor.fetchall()

        return data

    def airline_frequency(self):
        company = []
        freq = []
        self.mycursor.execute("""
        SELECT Company , COUNT(*) FROM flight 
        GROUP BY Company""")

        data = self.mycursor.fetchall()

        for item in data:
            company.append(item[0])
            freq.append(item[1])

        return company,freq

    def busy_airport(self):

        city =[]
        frequency = []
        self.mycursor.execute(""" 
        SELECT Origin , COUNT(*) FROM (SELECT Origin FROM flight 
                                       UNION ALL 
                                       SELECT Destination FROM flight ) t
        GROUP BY t.Origin 
        ORDER BY COUNT(*) DESC """)

        data = self.mycursor.fetchall()

        for item in data:
            city.append(item[0])
            frequency.append(item[1])

        return city , frequency

    def daily_average_flights(self):

        city =[]
        average_freq = []
        self.mycursor.execute(""" 
        SELECT Airport, round(AVG(Frequency)) AS AvgDailyFrequency
         FROM (SELECT Date, Origin AS Airport, COUNT(*) AS Frequency 
               FROM flight
               GROUP BY Date, Origin
               UNION ALL
               SELECT Date, Destination AS Airport, COUNT(*) AS Frequency 
               FROM flight
               GROUP BY Date, Destination) AS AllAirports
         GROUP BY Airport
         ORDER BY AvgDailyFrequency DESC; """)

        data = self.mycursor.fetchall()

        for item in data:
            city.append(item[0])
            average_freq.append(item[1])

        return city , average_freq


    def average_price_company(self):

        source_des =[]
        company = []
        avg_price =[]
        self.mycursor.execute(""" 
        SELECT Origin , Destination , Company , 
        round(AVG(CAST(REPLACE(`Flight Price`, ',', '') AS DECIMAL(10, 2)))) AS "average_price"
        FROM flight
        GROUP BY Origin, Destination , Company """)

        data = self.mycursor.fetchall()

        for item in data:
            source_des.append(item[0]+"-"+item[1])
            company.append(item[2])
            avg_price.append(item[3])

        return source_des , company ,avg_price




db = DB()
db.fetch_all_city()