# Disney Reservation Checker
This is a tool used to check the availability of certain restaurants at Walt Disney World. If a spot is available, the script can send a notification to an AWS SNS topic.

## Command Line Usage
#### Setup
1) ```virtualenv venvs```

2) Linux/MacOS: ```source venvs/bin/activate``` or
Windows: ```venvs\Scripts\activate```

3) ```pip install -r requirements.txt```

#### Command Line Examples
```python disneyReservations.py --size 4 --time 'breakfast' --location "Cinderella's Royal Table" --date 02/05/2019```

```python disneyReservations.py --size 4,6 --time 'breakfast','lunch' --location "Cinderella's Royal Table","Chef Mickey's" --date 02/06/2019,02/07/2019,02/08/2019```

## Docker Usage
Local Github source: ```docker build -t dpreardon/disneyreservation .```

Docker Hub: ```docker pull dpreardon/disneyreservation```

```docker run dpreardon/disneyreservation:latest --size 4 --time 'breakfast' --location "Cinderella's Royal Table" --date 02/05/2019```

<pre>
Usage:
python disneyReservations.py --size 2 --time 'breakfast' --date 02/05/2019

Options:
  -h, --help  Show this help message and exit
  -t, --time  Currently supports a comma separated list of times
              including 'breakfast' 'lunch' 'dinner'
  -d, --date  A comma separated list of dates in the format
              mm/dd/yyyy
  -s, --size  A comma separated list of integers between 1 and 49
  -l, --location
              Currently supports a comma separated list of quoted
              string locations including "Cinderella's Royal Table"
              and "Chef Mickey's"
  -n, --notification
              SNS ARN for Notification Topic
  --debug DEBUG
              Set debug level logging
</pre>

### Defaults

* Time: 'dinner'
* Size: '2'
* Date: Today's date
* Location: Cinderella's Royal Table
* Notification: None

## Environment
This tool has been tested in Linux and MacOS environments with Python 3.6, but should work in other environments with the correct Chromedriver.