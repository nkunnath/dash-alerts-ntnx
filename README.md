# Alerts Dashboard for Nutanix

## Introduction
This app creates a dashboard to visualize all the alerts generated in your Nutanix cluster. You can filter out the alerts by severity levels and view them by the month as well as annually.
Currently, the app displays the alert stats for the year 2020. The data has been gathered using the Nutanix v2 API alerts endpoint. It is cleaned and structured using pandas and the visualization is created using Dash developed by Plotly, which is a open source Python framework.

## Screenshots

![Output sample](https://j.gifs.com/Qnz6EM.gif)

![Output sample](https://j.gifs.com/gZon0Z.gif)


## Requirements

It is always better to create a separate virtual environment running Python 3 for this app, and install all of the required dependencies there. 

Run in Terminal/Command Prompt:

```
git clone https://github.com/nkunnath/dash-alerts-ntnx.git
cd dash-alerts-ntnx/
python3 -m pip install virtualenv
python3 -m virtualenv venv
```
In UNIX system:

```source venv/bin/activate```

In Windows:

```venv\Scripts\activate```

To install all of the required packages to this environment, simply run:

```pip install -r requirements.txt```

and all of the required pip packages, will be installed, and the app will be able to run.


## How to use this app

You have to specify the Nutanix cluster that you wish to connect to before running the app.

To do so, open the `dash-alerts-ntnx/request.py` file using a common text editor like vim. An example is shown in the file as well. You will have to just replace the IP address of the cluster and the credentials you would use to login as well. Save and quit from the file.

After this you could run this app 

1) On the loopback address locally:

```python app.py```

Open http://127.0.0.1:8050/ in your browser, you should see the dashboard.



2) Expose it on the IP address of your machine so it is accessible over the LAN. 

The command in this case would be as below. Replace x.x.x.x with the correct IP address.


```perl -i -pe"s/debug=True/debug=True,host='x.x.x.x'/g" app.py```


Run the app

```python app.py```

Open http://x.x.x.x:8050/ in your browser, you should see the dashboard.

    Note: Later if you wish to expose it on the loopback address again, run the below to change it back to the default setting.

    perl -i -pe"s/debug=True,host='x.x.x.x'/debug=True/g" app.py


## License
[MIT](https://choosealicense.com/licenses/mit/)
