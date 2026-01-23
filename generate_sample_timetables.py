"""
Generate sample timetable data for testing the route-finding algorithm.
This creates realistic timetable data for a subset of trains.
"""
import json
from datetime import datetime, timedelta

def generate_sample_timetables():
    """
    Generate sample timetables for testing.
    We'll create realistic schedules for various trains connecting major cities.
    """
    
    # Sample timetables with realistic data
    sample_timetables = {
        "12127": {
            "trainNo": 12127,
            "trainName": "Mumbai Pune Intercity",
            "fromStation": "Mumbai CSMT",
            "toStation": "Pune Junction",
            "timetable": [
                {"station_code": "CSMT", "station_name": "Mumbai CSMT", "arrival_time": "Source", "departure_time": "07:10", "distance_km": "0"},
                {"station_code": "KYN", "station_name": "Kalyan Junction", "arrival_time": "07:55", "departure_time": "08:00", "distance_km": "54"},
                {"station_code": "LNL", "station_name": "Lonavala", "arrival_time": "09:15", "departure_time": "09:20", "distance_km": "109"},
                {"station_code": "PUNE", "station_name": "Pune Junction", "arrival_time": "10:25", "departure_time": "Destination", "distance_km": "192"}
            ]
        },
        "12123": {
            "trainNo": 12123,
            "trainName": "Pune Nagpur SF Express",
            "fromStation": "Pune Junction",
            "toStation": "Nagpur Junction",
            "timetable": [
                {"station_code": "PUNE", "station_name": "Pune Junction", "arrival_time": "Source", "departure_time": "14:30", "distance_km": "0"},
                {"station_code": "DD", "station_name": "Daund Junction", "arrival_time": "15:40", "departure_time": "15:45", "distance_km": "72"},
                {"station_code": "ANG", "station_name": "Ahmadnagar", "arrival_time": "17:00", "departure_time": "17:05", "distance_km": "120"},
                {"station_code": "KPG", "station_name": "Kopargaon", "arrival_time": "18:20", "departure_time": "18:25", "distance_km": "180"},
                {"station_code": "MMR", "station_name": "Manmad Junction", "arrival_time": "19:40", "departure_time": "19:50", "distance_km": "254"},
                {"station_code": "JL", "station_name": "Jalgaon Junction", "arrival_time": "21:30", "departure_time": "21:35", "distance_km": "371"},
                {"station_code": "BSL", "station_name": "Bhusaval Junction", "arrival_time": "22:00", "departure_time": "22:10", "distance_km": "394"},
                {"station_code": "AK", "station_name": "Akola Junction", "arrival_time": "00:15", "departure_time": "00:20", "distance_km": "538"},
                {"station_code": "BD", "station_name": "Badnera Junction", "arrival_time": "02:00", "departure_time": "02:05", "distance_km": "631"},
                {"station_code": "NGP", "station_name": "Nagpur Junction", "arrival_time": "04:30", "departure_time": "Destination", "distance_km": "718"}
            ]
        },
        "18029": {
            "trainNo": 18029,
            "trainName": "Nagpur Bilaspur Express",
            "fromStation": "Nagpur Junction",
            "toStation": "Bilaspur Junction",
            "timetable": [
                {"station_code": "NGP", "station_name": "Nagpur Junction", "arrival_time": "Source", "departure_time": "06:00", "distance_km": "0"},
                {"station_code": "G", "station_name": "Gondia Junction", "arrival_time": "08:15", "departure_time": "08:20", "distance_km": "155"},
                {"station_code": "DURG", "station_name": "Durg Junction", "arrival_time": "11:30", "departure_time": "11:40", "distance_km": "326"},
                {"station_code": "R", "station_name": "Raipur Junction", "arrival_time": "12:20", "departure_time": "12:30", "distance_km": "362"},
                {"station_code": "BSP", "station_name": "Bilaspur Junction", "arrival_time": "15:00", "departure_time": "Destination", "distance_km": "495"}
            ]
        },
        "18109": {
            "trainNo": 18109,
            "trainName": "Bilaspur Tatanagar Express",
            "fromStation": "Bilaspur Junction",
            "toStation": "Tatanagar Junction",
            "timetable": [
                {"station_code": "BSP", "station_name": "Bilaspur Junction", "arrival_time": "Source", "departure_time": "16:30", "distance_km": "0"},
                {"station_code": "RIG", "station_name": "Raigarh", "arrival_time": "18:40", "departure_time": "18:45", "distance_km": "111"},
                {"station_code": "JSG", "station_name": "Jharsuguda Junction", "arrival_time": "20:10", "departure_time": "20:15", "distance_km": "197"},
                {"station_code": "ROU", "station_name": "Rourkela Junction", "arrival_time": "22:30", "departure_time": "22:40", "distance_km": "317"},
                {"station_code": "CKP", "station_name": "Chakradharpur", "arrival_time": "01:15", "departure_time": "01:20", "distance_km": "470"},
                {"station_code": "TATA", "station_name": "Tatanagar Junction", "arrival_time": "03:00", "departure_time": "Destination", "distance_km": "547"}
            ]
        },
        "18183": {
            "trainNo": 18183,
            "trainName": "Tatanagar Danapur Express",
            "fromStation": "Tatanagar Junction",
            "toStation": "Danapur Junction",
            "timetable": [
                {"station_code": "TATA", "station_name": "Tatanagar Junction", "arrival_time": "Source", "departure_time": "05:30", "departure_time": "05:30", "distance_km": "0"},
                {"station_code": "RNC", "station_name": "Ranchi Junction", "arrival_time": "07:45", "departure_time": "07:55", "distance_km": "140"},
                {"station_code": "MURI", "station_name": "Muri Junction", "arrival_time": "09:20", "departure_time": "09:25", "distance_km": "218"},
                {"station_code": "DHN", "station_name": "Dhanbad Junction", "arrival_time": "11:00", "departure_time": "11:10", "distance_km": "288"},
                {"station_code": "GAYA", "station_name": "Gaya Junction", "arrival_time": "13:30", "departure_time": "13:35", "distance_km": "428"},
                {"station_code": "DNR", "station_name": "Danapur Junction", "arrival_time": "16:00", "departure_time": "Destination", "distance_km": "545"}
            ]
        },
        "12875": {
            "trainNo": 12875,
            "trainName": "Pune Hatia SF Express",
            "fromStation": "Pune Junction",
            "toStation": "Hatia",
            "timetable": [
                {"station_code": "PUNE", "station_name": "Pune Junction", "arrival_time": "Source", "departure_time": "20:30", "distance_km": "0"},
                {"station_code": "DD", "station_name": "Daund Junction", "arrival_time": "21:50", "departure_time": "21:55", "distance_km": "72"},
                {"station_code": "ANG", "station_name": "Ahmadnagar", "arrival_time": "23:10", "departure_time": "23:15", "distance_km": "120"},
                {"station_code": "MMR", "station_name": "Manmad Junction", "arrival_time": "01:40", "departure_time": "01:50", "distance_km": "254"},
                {"station_code": "BSL", "station_name": "Bhusaval Junction", "arrival_time": "04:00", "departure_time": "04:10", "distance_km": "394"},
                {"station_code": "NGP", "station_name": "Nagpur Junction", "arrival_time": "10:30", "departure_time": "10:45", "distance_km": "718"},
                {"station_code": "DURG", "station_name": "Durg Junction", "arrival_time": "14:20", "departure_time": "14:25", "distance_km": "1044"},
                {"station_code": "R", "station_name": "Raipur Junction", "arrival_time": "15:00", "departure_time": "15:05", "distance_km": "1080"},
                {"station_code": "BSP", "station_name": "Bilaspur Junction", "arrival_time": "17:30", "departure_time": "17:40", "distance_km": "1213"},
                {"station_code": "ROU", "station_name": "Rourkela Junction", "arrival_time": "22:45", "departure_time": "22:55", "distance_km": "1530"},
                {"station_code": "CKP", "station_name": "Chakradharpur", "arrival_time": "01:30", "departure_time": "01:35", "distance_km": "1683"},
                {"station_code": "TATA", "station_name": "Tatanagar Junction", "arrival_time": "03:15", "departure_time": "03:25", "distance_km": "1760"},
                {"station_code": "RNC", "station_name": "Ranchi Junction", "arrival_time": "05:30", "departure_time": "05:40", "distance_km": "1900"},
                {"station_code": "HTE", "station_name": "Hatia", "arrival_time": "06:30", "departure_time": "Destination", "distance_km": "1940"}
            ]
        },
        "12290": {
            "trainNo": 12290,
            "trainName": "Nagpur Howrah Duronto",
            "fromStation": "Nagpur Junction",
            "toStation": "Howrah Junction",
            "timetable": [
                {"station_code": "NGP", "station_name": "Nagpur Junction", "arrival_time": "Source", "departure_time": "08:00", "distance_km": "0"},
                {"station_code": "DURG", "station_name": "Durg Junction", "arrival_time": "11:30", "departure_time": "11:35", "distance_km": "326"},
                {"station_code": "R", "station_name": "Raipur Junction", "arrival_time": "12:10", "departure_time": "12:15", "distance_km": "362"},
                {"station_code": "BSP", "station_name": "Bilaspur Junction", "arrival_time": "14:30", "departure_time": "14:35", "distance_km": "495"},
                {"station_code": "ROU", "station_name": "Rourkela Junction", "arrival_time": "19:30", "departure_time": "19:35", "distance_km": "812"},
                {"station_code": "TATA", "station_name": "Tatanagar Junction", "arrival_time": "22:00", "departure_time": "22:05", "distance_km": "1042"},
                {"station_code": "KGP", "station_name": "Kharagpur Junction", "arrival_time": "00:10", "departure_time": "00:15", "distance_km": "1187"},
                {"station_code": "HWH", "station_name": "Howrah Junction", "arrival_time": "02:30", "departure_time": "Destination", "distance_km": "1306"}
            ]
        },
        "12151": {
            "trainNo": 12151,
            "trainName": "Mumbai LTT Howrah SF Express",
            "fromStation": "Mumbai LTT",
            "toStation": "Howrah Junction",
            "timetable": [
                {"station_code": "LTT", "station_name": "Mumbai LTT", "arrival_time": "Source", "departure_time": "11:20", "distance_km": "0"},
                {"station_code": "KYN", "station_name": "Kalyan Junction", "arrival_time": "12:05", "departure_time": "12:08", "distance_km": "54"},
                {"station_code": "NK", "station_name": "Nashik Road", "arrival_time": "14:33", "departure_time": "14:35", "distance_km": "186"},
                {"station_code": "BSL", "station_name": "Bhusaval Junction", "arrival_time": "18:15", "departure_time": "18:25", "distance_km": "424"},
                {"station_code": "NGP", "station_name": "Nagpur Junction", "arrival_time": "01:00", "departure_time": "01:10", "distance_km": "748"},
                {"station_code": "DURG", "station_name": "Durg Junction", "arrival_time": "05:05", "departure_time": "05:10", "distance_km": "1074"},
                {"station_code": "R", "station_name": "Raipur Junction", "arrival_time": "05:50", "departure_time": "05:55", "distance_km": "1110"},
                {"station_code": "BSP", "station_name": "Bilaspur Junction", "arrival_time": "08:10", "departure_time": "08:20", "distance_km": "1243"},
                {"station_code": "JSG", "station_name": "Jharsuguda Junction", "arrival_time": "11:08", "departure_time": "11:10", "distance_km": "1440"},
                {"station_code": "ROU", "station_name": "Rourkela Junction", "arrival_time": "12:40", "departure_time": "12:50", "distance_km": "1560"},
                {"station_code": "TATA", "station_name": "Tatanagar Junction", "arrival_time": "15:25", "departure_time": "15:30", "distance_km": "1790"},
                {"station_code": "KGP", "station_name": "Kharagpur Junction", "arrival_time": "17:45", "departure_time": "17:50", "distance_km": "1935"},
                {"station_code": "HWH", "station_name": "Howrah Junction", "arrival_time": "20:05", "departure_time": "Destination", "distance_km": "2054"}
            ]
        }
    }
    
    # Save to JSON file
    with open('train_timetables.json', 'w') as f:
        json.dump(sample_timetables, f, indent=2)
    
    print(f"Generated {len(sample_timetables)} sample timetables")
    print("Saved to train_timetables.json")
    
    # Print summary
    print("\nSample trains:")
    for train_no, data in sample_timetables.items():
        print(f"{train_no}: {data['trainName']}")
        print(f"  Route: {data['fromStation']} → {data['toStation']}")
        print(f"  Stations: {len(data['timetable'])}")

if __name__ == "__main__":
    generate_sample_timetables()
