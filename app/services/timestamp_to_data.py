class TimestampToDataService:
    def get_data(self, timestamp: int) -> dict:
        from datetime import datetime

        # Convert timestamp to datetime object
        dt = datetime.fromtimestamp(int(timestamp))

        # Return formatted date information
        return {
            "date": dt.strftime("%Y-%m-%d"),
            "time": dt.strftime("%H:%M:%S"),
            "year": dt.year,
            "month": dt.month,
            "day": dt.day,
            "hour": dt.hour,
            "minute": dt.minute,
            "second": dt.second,
            "weekday": dt.strftime("%A"),
            "iso_format": dt.isoformat(),
        }
