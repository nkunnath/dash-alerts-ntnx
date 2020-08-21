# Caveats

1) This app cannot be used for Prism Central but only for one cluster. The IP address configured in request.py should point to one of the CVM IP addresses or the cluster virtual IP. Prism Central does not support v2 API's used to obtain the data in the app.

1) The app does not auto-update. To see the updated stats, you will have to restart the app (Ctrl + C), as that will fetch the latest alert response and generates a new dataset.

1) Currently the app only shows data over 2020, ie from January 1, 2020 to December 31, 2020
